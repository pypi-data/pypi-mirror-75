import logging
import sys
from collections import namedtuple
from dataclasses import dataclass
from typing import Callable, Dict, Optional, Sequence, Tuple, cast

import numpy as np
import torch as t
from torch.optim import Optimizer
from torch.utils.data import DataLoader, Dataset

from .hyperparams import Hyperparams
from .ml_logger import MLExperiment

MetricFunc = Callable[[t.Tensor, t.Tensor], float]
logger = logging.getLogger(__name__)

Metric = namedtuple("Metric", ["name", "value"])


@dataclass
class TrainerArgs:
    run_name: str
    model: t.nn.Module
    optim: Optimizer
    loss_fn: Callable[[t.Tensor, t.Tensor], t.Tensor]
    trainloader: DataLoader
    valloader: DataLoader
    n_epochs: int
    grad_warning_threshold: float = 1000
    loss_warning_threshold: float = 10_000
    clip_grads: float = float("inf")


ArgsBuilderType = Callable[[Hyperparams, Dataset, Dataset], TrainerArgs]

DEVICE = t.device("cuda" if t.cuda.is_available() else "cpu")


class Trainer:
    def __init__(
        self,
        experiment: MLExperiment,
        trainset: Dataset,
        valset: Dataset,
        metric_functions: Sequence[MetricFunc],
    ) -> None:
        self._trainset = trainset
        self._valset = valset

        tempdl = DataLoader(self._trainset, batch_size=2)
        _, batch_target = next(iter(tempdl))
        self._target_dtype = batch_target.dtype

        self._metric_functions = metric_functions
        self._experiment = experiment
        self._args: Optional[TrainerArgs] = None

        self.metrics_log_frequency: int = 1
        self.model_log_frequency: int = sys.maxsize

        self.model: Optional[t.nn.Module] = None
        self.final_metrics: Dict[str, float] = {}

    def _train(self, calc_metrics: bool = False,) -> Tuple[float, Dict[str, float]]:
        args = cast(TrainerArgs, self._args)
        model = cast(t.nn.Module, self.model)

        traindl = args.trainloader
        optim = args.optim
        loss_fn = args.loss_fn
        clip_grads = args.clip_grads

        model.train()
        losses = []
        outputs = t.Tensor([])  # pyre-ignore
        targets = t.Tensor([]).to(self._target_dtype)  # pyre-ignore
        with t.enable_grad():
            for batch_inputs, batch_targets in traindl:
                batch_inputs = batch_inputs.to(DEVICE)
                batch_targets = batch_targets.to(DEVICE)

                optim.zero_grad()
                batch_outputs = model.forward(batch_inputs)
                loss = loss_fn(batch_outputs, batch_targets)
                loss.backward()

                if clip_grads < float("inf"):
                    t.nn.utils.clip_grad_value_(model.parameters(), clip_grads)

                optim.step()

                losses.append(loss.detach().item())

                if calc_metrics:
                    outputs = t.cat((outputs, batch_outputs.detach()))
                    targets = t.cat((targets, batch_targets))

        loss = np.mean(losses)

        metrics: Dict[str, float] = {}
        if calc_metrics:
            metrics["train_loss"] = loss
            for metric_func in self._metric_functions:
                metrics["train_" + metric_func.__name__] = metric_func(targets, outputs)

        return loss, metrics

    def _validate(self):
        args = cast(TrainerArgs, self._args)
        model = cast(t.nn.Module, self.model)

        valdl = args.valloader
        loss_fn = args.loss_fn

        model.eval()
        losses = []
        outputs = t.Tensor([])
        targets = t.Tensor([]).to(self._target_dtype)
        with t.no_grad():
            for batch_inputs, batch_targets in valdl:
                batch_inputs = batch_inputs.to(DEVICE)
                batch_targets = batch_targets.to(DEVICE)
                batch_outputs = model(batch_inputs)
                loss = loss_fn(batch_outputs, batch_targets)
                losses.append(loss.detach().item())
                outputs = t.cat((outputs, batch_outputs))
                targets = t.cat((targets, batch_targets))

        loss = np.mean(losses)

        metrics: Dict[str, float] = {}
        metrics["val_loss"] = loss
        for metric_func in self._metric_functions:
            metrics["val_" + metric_func.__name__] = metric_func(targets, outputs)

        return loss, metrics

    def train(self, hparams: Hyperparams, args_builder: ArgsBuilderType) -> None:
        args = args_builder(hparams, self._trainset, self._valset)
        model = args.model.to(DEVICE)

        self._args = args
        self.model = model

        with self._experiment.start_run(args.run_name) as run:
            for epoch in range(1, args.n_epochs + 1):
                train_loss: float = 0.0
                val_loss: float = 0.0
                if epoch % self.metrics_log_frequency == 0:
                    train_loss, metrics = self._train(calc_metrics=True)
                    val_loss, val_metrics = self._validate()
                    metrics.update(val_metrics)
                    for metric_name, metric_value in metrics.items():
                        run.log_metric(epoch, metric_name, metric_value)
                else:
                    train_loss, _ = self._train()

                # Warn about high loss values
                if train_loss > args.loss_warning_threshold:
                    logger.warning(f"Epoch {epoch}: Training loss {train_loss:.3f} is too high!")
                if val_loss > args.loss_warning_threshold:
                    logger.warning(f"Epoch {epoch}: Validation loss {val_loss:.3f} is too high!")

                # Warn about high gradients
                # pyre-ignore
                max_grad = t.max(t.Tensor([t.max(param) for param in self.model.parameters()]))
                if max_grad > args.grad_warning_threshold:
                    logger.warning(f"Epoch {epoch}: Gradient {max_grad:.3f} is too high!")

                # Checkpoint the model if needed
                if epoch % self.model_log_frequency == 0:
                    run.log_model(epoch, model)

            # Calculate the final metrics on the validation dataset and log them
            # as part of run summary along with the hyperparams
            _, self.final_metrics = self._validate()
            run.log_summary(hparams.to_dict(), self.final_metrics)
