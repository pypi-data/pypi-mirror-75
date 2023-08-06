from typing import Callable, Dict, Sequence, Union

import torch as t
from torch.utils.data import DataLoader

MetricFunc = Callable[[t.Tensor, t.Tensor], float]
DEVICE = t.device("cuda" if t.cuda.is_available() else "cpu")


def evaluate(
    model: t.nn.Module, dataloader: DataLoader, metric_functions: Sequence[MetricFunc]
) -> Dict[str, Union[float, t.Tensor]]:
    model.eval()

    _, tmp = next(iter(dataloader))
    target_dtype = tmp.dtype

    outputs = t.Tensor([])  # pyre-ignore
    targets = t.Tensor([]).to(target_dtype)  # pyre-ignore

    with t.no_grad():
        for batch_inputs, batch_targets in dataloader:
            batch_inputs = batch_inputs.to(DEVICE)
            batch_targets = batch_targets.to(DEVICE)

            batch_outputs = model(batch_inputs)
            outputs = t.cat((outputs, batch_outputs))
            targets = t.cat((targets, batch_targets))

    metrics: Dict[str, Union[float, t.Tensor]] = {}
    for metric_func in metric_functions:
        metrics[metric_func.__name__] = metric_func(targets, outputs)

    metrics["outputs"] = outputs
    metrics["targets"] = targets

    return metrics
