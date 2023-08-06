import logging
import pprint
import uuid
from dataclasses import dataclass
from typing import Callable, Sequence, Tuple

import sklearn.datasets as skdata
import torch as t
from sklearn.metrics import accuracy_score
from torch.utils.data import DataLoader, Dataset, TensorDataset

from ..evaluator import evaluate
from ..hyperparams import Hyperparams
from ..ml_loggers.mlflow_logger import MLFlowMLExperiment
from ..trainer import Trainer, TrainerArgs

logging.basicConfig(level=logging.DEBUG)
MetricFunc = Callable[[t.Tensor, t.Tensor], float]


class BinaryClassifier(t.nn.Module):
    def __init__(self) -> None:
        super().__init__()
        self.fc1 = t.nn.Linear(20, 8)
        self.fc2 = t.nn.Linear(8, 1)

    def forward(self, batch_x: t.Tensor) -> t.Tensor:
        x = t.nn.functional.relu(self.fc1(batch_x))
        batch_y_hat = t.sigmoid(self.fc2(x))
        return t.squeeze(batch_y_hat, dim=1)


@dataclass
class MyHyperparams(Hyperparams):
    n_epochs: int
    batch_size: int
    lr: float
    true_cutoff: float


def gen_datasets(n_samples: int) -> Tuple[Dataset, Dataset, Dataset]:
    X, y = skdata.make_classification(
        n_samples=n_samples,
        n_features=20,
        n_informative=10,
        n_redundant=7,
        n_repeated=3,
        n_classes=2,
        flip_y=0.05,  # larger values make the task hard
        class_sep=0.5,  # larger values makes the task easy
        random_state=10,
    )

    train_size = int(n_samples * 0.7)
    val_size = int(n_samples * 0.2)

    train_X = X[:train_size]
    train_y = y[:train_size]
    trainset = TensorDataset(
        t.from_numpy(train_X).to(t.float32), t.from_numpy(train_y).to(t.float32)
    )

    val_X = X[train_size : train_size + val_size]
    val_y = y[train_size : train_size + val_size]
    valset = TensorDataset(t.from_numpy(val_X).to(t.float32), t.from_numpy(val_y).to(t.float32))

    test_X = X[train_size + val_size :]
    test_y = y[train_size + val_size :]
    testset = TensorDataset(t.from_numpy(test_X).to(t.float32), t.from_numpy(test_y).to(t.float32))

    return trainset, valset, testset


def build_accuracy(cutoff: float) -> Callable[[t.Tensor, t.Tensor], float]:
    def accuracy(y_true, y_hat):
        y_pred = (y_hat > cutoff).to(t.float32)
        return accuracy_score(y_true, y_pred)

    return accuracy


def build_trainer(hparams: MyHyperparams, trainset: Dataset, valset: Dataset) -> TrainerArgs:
    run_name = "run-" + str(uuid.uuid4())[:8]
    print(f"Starting run {run_name}")
    model = BinaryClassifier()
    optim = t.optim.Adam(model.parameters(), lr=hparams.lr)
    loss_fn = t.nn.BCELoss()
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
    # Do the following to start mlflow properly.
    # cd ~/temp/mlflow
    # mlflow ui
    # This will create a directory called mlruns under ~/temp/mlflow/mlruns and start the mlflow webserver on port 5000.
    # Now set the experiment dir to ~temp/mlflow/mlruns
    exp = MLFlowMLExperiment("binaryclass-exp", "~/temp/mlflow/mlruns")
    trainer = Trainer(exp, trainset, valset, metric_functions=metric_functions)
    trainer.metrics_log_frequency = 1
    trainer.model_log_frequency = 5
    trainer.train(hparams, build_trainer)  # pyre-ignore


def main() -> None:
    hparams = MyHyperparams(n_epochs=7, lr=0.005, batch_size=32, true_cutoff=0.5)
    trainset, valset, testset = gen_datasets(n_samples=100_000)
    accuracy = build_accuracy(cutoff=hparams.true_cutoff)
    train(hparams, trainset, valset, [accuracy])

    print("Enter the path of the saved model:")
    model_path = input()
    model = t.load(model_path)
    testdl = DataLoader(testset, batch_size=5000)
    test_metrics = evaluate(model, testdl, [accuracy])
    pprint.pprint(test_metrics)


if __name__ == "__main__":
    main()
