import pprint
import uuid
from dataclasses import dataclass
from typing import Callable, Sequence, Tuple

import sklearn.datasets as skdata
import torch as t
from sklearn.metrics import mean_absolute_error
from torch.utils.data import DataLoader, Dataset, TensorDataset

from ..evaluator import evaluate
from ..hyperparams import Hyperparams
from ..ml_loggers.stdout_logger import StdoutMLExperiment
from ..trainer import Trainer, TrainerArgs

MetricFunc = Callable[[t.Tensor, t.Tensor], float]


class Regressor(t.nn.Module):
    def __init__(self) -> None:
        super().__init__()
        self.fc1 = t.nn.Linear(5, 3)
        self.fc2 = t.nn.Linear(3, 1)

    def forward(self, batch_x: t.Tensor) -> t.Tensor:
        x = t.nn.functional.relu(self.fc1(batch_x))
        batch_y_hat = self.fc2(x)
        return t.squeeze(batch_y_hat, dim=1)


@dataclass
class MyHyperparams(Hyperparams):
    batch_size: int
    n_epochs: int
    lr: float


def gen_datasets(n_samples: int) -> Tuple[Dataset, Dataset, Dataset]:
    all_X, all_y = skdata.make_regression(n_samples=n_samples, n_features=5, noise=0.5)

    train_size = int(n_samples * 0.7)
    val_size = int(n_samples * 0.2)

    train_X = all_X[:train_size]
    train_y = all_y[:train_size]
    trainset = TensorDataset(
        t.from_numpy(train_X).to(t.float32), t.from_numpy(train_y).to(t.float32)
    )

    val_X = all_X[train_size : train_size + val_size]
    val_y = all_y[train_size : train_size + val_size]
    valset = TensorDataset(t.from_numpy(val_X).to(t.float32), t.from_numpy(val_y).to(t.float32))

    test_X = all_X[train_size + val_size :]
    test_y = all_y[train_size + val_size :]
    testset = TensorDataset(t.from_numpy(test_X).to(t.float32), t.from_numpy(test_y).to(t.float32))

    return trainset, valset, testset


def build_trainer(hparams: MyHyperparams, trainset: Dataset, valset: Dataset) -> TrainerArgs:
    run_name = "run-" + str(uuid.uuid4())[:8]
    model = Regressor()
    optim = t.optim.Adam(model.parameters(), lr=hparams.lr)
    loss_fn = t.nn.MSELoss(reduction="mean")
    traindl = DataLoader(trainset, batch_size=hparams.batch_size, shuffle=True)
    valdl = DataLoader(valset, batch_size=5000)
    return TrainerArgs(
        run_name=run_name,
        model=model,
        optim=optim,
        loss_fn=loss_fn,
        trainloader=traindl,
        valloader=valdl,
        n_epochs=hparams.n_epochs,
    )


def train(
    hparams: MyHyperparams,
    trainset: Dataset,
    valset: Dataset,
    metric_functions: Sequence[MetricFunc],
) -> None:
    exp = StdoutMLExperiment("regress-exp")
    trainer = Trainer(exp, trainset, valset, metric_functions=metric_functions)
    trainer.metrics_log_frequency = 1
    trainer.model_log_frequency = 5
    trainer.train(hparams, build_trainer)  # pyre-ignore


def main() -> None:
    hparams = MyHyperparams(batch_size=16, n_epochs=10, lr=0.03)
    trainset, valset, testset = gen_datasets(n_samples=100_000)
    train(hparams, trainset, valset, [mean_absolute_error])

    print("Enter the path of the saved model:")
    model_path = input()
    model = t.load(model_path)
    testdl = DataLoader(testset, batch_size=5000)
    test_metrics = evaluate(model, testdl, [mean_absolute_error])
    pprint.pprint(test_metrics)


if __name__ == "__main__":
    main()
