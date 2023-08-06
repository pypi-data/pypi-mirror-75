import json
import os
import os.path as path
from typing import Any, Dict, Tuple

import numpy as np
import pandas as pd
from plotly.subplots import make_subplots
from termcolor import cprint


def _calc_layout(n: int) -> Tuple[int, int]:
    nrows = int(np.floor(np.sqrt(n)))
    ncols = int(np.ceil(np.sqrt(n)))
    assert nrows * ncols >= n
    return nrows, ncols


def analyze(*, exproot: str, run_name: str) -> None:
    exproot = path.expanduser(exproot)
    summary_file = path.join(exproot, run_name, "summary.json")
    summary: Dict[str, Any] = {}
    with open(summary_file, "rt") as f:
        summary = json.load(f)

    eval_metric_names = list(summary["evaluation_metrics"].keys())
    cprint("Evaluation Metrics", attrs=["bold"])
    width = max(len(name) for name in eval_metric_names) + 2
    for eval_metric_name in eval_metric_names:
        eval_metric_val = np.around(summary["evaluation_metrics"][eval_metric_name], 3)
        cprint(f"  {eval_metric_name: <{width}}: {eval_metric_val}")

    print("\n")
    hparam_names = list(summary["hyperparams"].keys())
    cprint("Hyper Parameters", attrs=["bold"])
    width = max(len(name) for name in hparam_names) + 2
    for hparam_name in hparam_names:
        if isinstance(summary["hyperparams"][hparam_name], float):
            hparam_val = np.around(summary["hyperparams"][hparam_name], 3)
        else:
            hparam_val = summary["hyperparams"][hparam_name]
        cprint(f"  {hparam_name: <{width}}: {hparam_val}")

    metrics_file = path.join(exproot, run_name, "metrics.csv")
    metrics_df = pd.read_csv(metrics_file, parse_dates=["timestamp"])
    metric_names = [name.replace("val_", "") for name in eval_metric_names]

    nrows, ncols = _calc_layout(len(metric_names))
    fig = make_subplots(rows=nrows, cols=ncols, subplot_titles=metric_names)

    row, col = 1, 0
    for metric_name in metric_names:
        if col > ncols:
            row += 1
            col = 1
        else:
            col += 1

        name = "train_" + metric_name
        train_metric = metrics_df[metrics_df.name == name]
        fig.add_scatter(
            x=train_metric.step.values,
            y=train_metric.value.values,
            name=name,
            row=row,
            col=col,
            line_color="red",
        )

        name = "val_" + metric_name
        val_metric = metrics_df[metrics_df.name == name]
        fig.add_scatter(
            x=val_metric.step.values,
            y=val_metric.value.values,
            name=name,
            row=row,
            col=col,
            line_color="blue",
        )

    fig.show()


def compare(exproot: str) -> pd.DataFrame:
    run_names = os.listdir(exproot)
    summary_file = path.join(exproot, run_names[0], "summary.json")
    summary = {}
    with open(summary_file, "rt") as f:
        summary = json.load(f)

    eval_metric_names = list(summary["evaluation_metrics"].keys())
    hparam_names = list(summary["hyperparams"].keys())

    data = {"run_names": []}
    for eval_metric_name in eval_metric_names:
        data[eval_metric_name] = []
    for hparam_name in hparam_names:
        data[hparam_name] = []

    for run_name in run_names:
        summary_file = path.join(exproot, run_name, "summary.json")
        if not path.exists(summary_file):
            cprint(f"Ignoring empty run {run_name}.", "yellow")
        with open(summary_file, "rt") as f:
            summary = json.load(f)
        data["run_names"].append(run_name)

        for eval_metric_name in eval_metric_names:
            eval_metric_val = summary["evaluation_metrics"][eval_metric_name]
            data[eval_metric_name].append(eval_metric_val)

        for hparam_name in hparam_names:
            hparam_val = summary["hyperparams"][hparam_name]
            data[hparam_name].append(hparam_val)

    disp_metric_name = eval_metric_names[0].replace("val_", "").capitalize()
    cprint("To plot using this dataframe:", attrs=["bold"])
    cprint(
        f"fig = go.Figure(layout_title_text='{disp_metric_name}', layout_xaxis_title='Runs'", "blue"
    )
    cprint(f"fig.add_bar(x=summary.run_names, y=summary.{eval_metric_names[0]})\n", "blue")
    return pd.DataFrame(data)
