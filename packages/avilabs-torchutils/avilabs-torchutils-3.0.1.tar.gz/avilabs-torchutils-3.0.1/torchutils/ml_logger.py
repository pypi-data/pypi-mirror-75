from abc import ABC, abstractmethod
from contextlib import contextmanager
from typing import Any, Dict, Generator

import torch


class MLRun(ABC):
    def __init__(self, name: str) -> None:
        self.name = name

    @abstractmethod
    def log_summary(self, hparams: Dict[str, Any], metrics: Dict[str, float]) -> None:
        raise NotImplementedError("Subclass must implement!")

    @abstractmethod
    def log_metric(self, step: int, name: str, val: float) -> None:
        raise NotImplementedError("Subclass must implement!")

    @abstractmethod
    def log_params(self, step: int, state: Dict[str, torch.Tensor]) -> None:
        raise NotImplementedError("Subclass must implement!")

    @abstractmethod
    def log_model(self, step, model) -> None:
        raise NotImplementedError("Subclass must implement!")


class MLExperiment(ABC):
    def __init__(self, name: str) -> None:
        self.name = name

    @abstractmethod
    @contextmanager
    def start_run(self, name: str) -> Generator[MLRun, None, None]:
        pass
