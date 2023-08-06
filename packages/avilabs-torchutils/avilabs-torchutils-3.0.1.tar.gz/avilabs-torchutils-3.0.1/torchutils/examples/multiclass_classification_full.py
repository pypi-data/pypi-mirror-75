import os.path as path
import pprint
import sys
import uuid
from dataclasses import dataclass
from typing import Callable, Tuple

import sklearn.datasets as skdata
import torch as t
from sklearn.metrics import accuracy_score
from torch.utils.data import DataLoader, Dataset, TensorDataset

from ..evaluator import evaluate
from ..hyperparams import Hyperparams, HyperparamsSpec
from ..ml_loggers.csv_logger import CsvMLExperiment
from ..ml_loggers.stdout_logger import StdoutMLExperiment
from ..trainer import Trainer, TrainerArgs
from ..tuner import Tuner

MetricFunc = Callable[[t.Tensor, t.Tensor], float]


class MulticlassClassifier(t.nn.Module):
    def __init__(self) -> None:
        super().__init__()
        self.fc1 = t.nn.Linear(20, 16)
        self.fc2 = t.nn.Linear(16, 8)
        self.fc3 = t.nn.Linear(8, 5)

    def forward(self, batch_x: t.Tensor) -> t.Tensor:
        x = t.nn.functional.relu(self.fc1(batch_x))
        x = t.nn.functional.relu(self.fc2(x))
        batch_y_hat = self.fc3(x)
        return batch_y_hat


@dataclass
class MyHyperparams(Hyperparams):
    batch_size: int
    n_epochs: int
    lr: float


def gen_datasets(n_samples: int) -> Tuple[Dataset, Dataset, Dataset]:
    X, y = skdata.make_classification(
        n_samples=n_samples,
        n_features=20,
        n_informative=10,
        n_redundant=7,
        n_repeated=3,
        n_classes=5,
        flip_y=0.05,  # larger values make the task hard
        class_sep=0.5,  # larger values makes the task easy
        random_state=10,
    )

    train_size = int(n_samples * 0.7)
    val_size = int(n_samples * 0.2)

    train_X = X[:train_size]
    train_y = y[:train_size]
    trainset = TensorDataset(t.from_numpy(train_X).to(t.float32), t.from_numpy(train_y).to(t.int64))

    val_X = X[train_size : train_size + val_size]
    val_y = y[train_size : train_size + val_size]
    valset = TensorDataset(t.from_numpy(val_X).to(t.float32), t.from_numpy(val_y).to(t.int64))

    test_X = X[train_size + val_size :]
    test_y = y[train_size + val_size :]
    testset = TensorDataset(t.from_numpy(test_X).to(t.float32), t.from_numpy(test_y).to(t.int64))

    return trainset, valset, testset


def accuracy(y_true: t.Tensor, y_hat: t.Tensor) -> float:
    y_pred = t.argmax(y_hat, dim=1)
    return accuracy_score(y_true, y_pred)


def build_trainer(hparams: MyHyperparams, trainset: Dataset, valset: Dataset,) -> TrainerArgs:
    run_name = "run-" + str(uuid.uuid4())[:8]
    print(f"\nStarting run {run_name}")
    model = MulticlassClassifier()
    optim = t.optim.Adam(model.parameters(), lr=hparams.lr)
    loss_fn = t.nn.CrossEntropyLoss()
    traindl = DataLoader(trainset, batch_size=hparams.batch_size, shuffle=True)
    valdl = DataLoader(valset, batch_size=1000)
    return TrainerArgs(
        run_name=run_name,
        model=model,
        optim=optim,
        loss_fn=loss_fn,
        trainloader=traindl,
        valloader=valdl,
        n_epochs=hparams.n_epochs,
    )


def train() -> None:
    hparams = MyHyperparams(batch_size=16, n_epochs=16, lr=0.003)
    trainset, valset, testset = gen_datasets(100_000)
    exp = CsvMLExperiment("multiclass-exp", "~/temp/experiments")
    trainer = Trainer(exp, trainset, valset, metric_functions=[accuracy])
    trainer.metrics_log_frequency = 1
    trainer.model_log_frequency = 5
    trainer.train(hparams, build_trainer)  # pyre-ignore

    print("Enter the path of the saved model:")
    model_path = input()
    if model_path and path.exists(model_path):
        model = t.load(model_path)
    else:
        print("Using trained model")
        model = trainer.model
    testdl = DataLoader(testset, batch_size=5000)
    test_metrics = evaluate(model, testdl, [accuracy])
    pprint.pprint(test_metrics)


def tune() -> None:
    exp = CsvMLExperiment("multiclass-exp-tune", "~/temp/experiments", stdout=False)
    trainset, valset, testset = gen_datasets(100_000)
    tuner = Tuner(exp, trainset, valset, accuracy)
    tuner.metrics_log_frequency = 1

    hparams_spec = HyperparamsSpec(
        factory=MyHyperparams,  # pyre-ignore
        spec=[
            {"name": "batch_size", "type": "choice", "value_type": "int", "values": [16, 32, 64]},
            {"name": "n_epochs", "type": "range", "value_type": "int", "bounds": [7, 23]},
            {"name": "lr", "type": "range", "bounds": [1e-4, 0.4], "log_scale": True},
        ],
    )
    # pyre-ignore
    best_params = tuner.tune(hparams_spec, build_trainer, total_trials=10)
    print(best_params)

    ans = input("Train using best params [Y/n]?")
    if ans.lower() != "n":
        exp = StdoutMLExperiment("best-model")
        trainer = Trainer(exp, trainset, valset, [accuracy])
        trainer.train(best_params, build_trainer)  # pyre-ignore
        best_model = trainer.model
        t.save(best_model, "best_model.pkl")
        print(trainer.final_metrics)


def main() -> None:
    if len(sys.argv) < 2 or sys.argv[1] not in ["train", "tune"]:
        print("Usage: python multiclass_classification_csv.py [train|tune]")
        sys.exit(1)

    if sys.argv[1] == "train":
        train()
    elif sys.argv[1] == "tune":
        tune()


if __name__ == "__main__":
    main()
