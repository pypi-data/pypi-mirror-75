import logging
import sys
from typing import Any, Callable, Dict, Optional, Tuple, cast

import torch as t
from ax.service.managed_loop import optimize
from torch.utils.data import Dataset

from .hyperparams import Hyperparams, HyperparamsSpec
from .ml_logger import MLExperiment
from .trainer import Trainer, TrainerArgs

ArgsBuilderType = Callable[[Hyperparams, Dataset, Dataset], TrainerArgs]
MetricFunc = Callable[[t.Tensor, t.Tensor], float]
HparamsFactory = Callable[[Dict[str, Any]], Hyperparams]

logger: logging.Logger = logging.getLogger(__name__)


class Tuner:
    def __init__(
        self,
        experiment: MLExperiment,
        trainset: Dataset,
        valset: Dataset,
        obj_metric: MetricFunc,
        minimize: bool = False,
    ) -> None:
        self._obj_metric: MetricFunc = obj_metric
        self._trainer = Trainer(experiment, trainset, valset, [obj_metric])
        self._trainer.metrics_log_frequency = sys.maxsize
        self._model_log_frequency: int = sys.maxsize
        self._minimize = minimize

        self._hparams_factory: Optional[HparamsFactory] = None
        self._args_builder: Optional[ArgsBuilderType] = None

    @property
    def metrics_log_frequency(self) -> int:
        return self._trainer.metrics_log_frequency

    @metrics_log_frequency.setter
    def metrics_log_frequency(self, freq: int) -> None:
        self._trainer.metrics_log_frequency = freq

    def _train_eval(self, hyper_params: Dict[str, Any]) -> Dict[str, Tuple[float, float]]:
        hparams_factory = cast(HparamsFactory, self._hparams_factory)
        hparams: Hyperparams = hparams_factory(**hyper_params)

        args_builder = cast(ArgsBuilderType, self._args_builder)
        self._trainer.train(hparams, args_builder)
        obj_name = self._obj_metric.__name__
        obj_val: Tuple[float, float] = (self._trainer.final_metrics["val_" + obj_name], 0.0)
        return {obj_name: obj_val}

    def tune(
        self, hparams_spec: HyperparamsSpec, args_builder: ArgsBuilderType, total_trials: int = 20
    ) -> Hyperparams:
        self._hparams_factory = hparams_spec.factory
        self._args_builder = args_builder

        best_params, values, _, _ = optimize(
            hparams_spec.spec,
            evaluation_function=self._train_eval,  # pyre-ignore
            objective_name=self._obj_metric.__name__,
            total_trials=total_trials,
            minimize=self._minimize,
        )

        logger.info(f"best_params={best_params} values={values}")
        return hparams_spec.factory(**best_params)  # pyre-ignore
