import os
from contextlib import contextmanager
from pprint import pprint
from typing import Any, Dict, Generator, List

import torch

from ..ml_logger import MLExperiment, MLRun


class StdoutMLRun(MLRun):
    def __init__(self, name: str) -> None:
        super().__init__(name)
        self._models_root: str = os.path.join(".", "models")
        os.makedirs(self._models_root, exist_ok=True)
        self._curr_step = 0
        self._buffer: List[str] = []

    def log_summary(self, hparams: Dict[str, Any], metrics: Dict[str, float]) -> None:
        summary = {"hyperparams": hparams, "evaluation_metrics": {}}
        for metric_name, metric_value in metrics.items():
            summary["evaluation_metrics"][metric_name] = round(metric_value, 3)
        print("\nSummary:")
        pprint(summary)

    def log_metric(self, step: int, name: str, val: float) -> None:
        if step == self._curr_step:
            self._buffer.append(f"{name} = {val:.3f}")
        else:
            self._print_buffer()
            self._buffer = [f"{name} = {val:.3f}"]
            self._curr_step = step

    def log_params(self, step: int, state: Dict[str, torch.Tensor]) -> None:
        print("[WARN] Stdout does not support logging parameters")

    def log_model(self, step: int, model: torch.nn.Module) -> None:
        model_filename = f"{self.name}-model-{step}.pkl"
        model_path = os.path.join(self._models_root, model_filename)
        print(f"\nStep {step}: Checkpointing model at {model_filename}")
        torch.save(model, model_path)

    def close(self):
        self._print_buffer()

    def _print_buffer(self):
        if self._buffer:
            print(f"\nStep {self._curr_step}")
        for buf in self._buffer:
            print(f"\t{buf}")


class StdoutMLExperiment(MLExperiment):
    def __init__(self, name: str) -> None:
        super().__init__(name)

    @contextmanager
    def start_run(self, name: str) -> Generator[MLRun, None, None]:
        run = StdoutMLRun(name)
        print(f"Starting run {name}")
        yield run
        run.close()
