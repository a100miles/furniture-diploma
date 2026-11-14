"""Figures for the paper from the CSVs written by evaluate_baselines.

Run from backend/:
  python -m scripts.plot_evaluation ../docs/assets/eval
"""

import csv
import random
import statistics
import sys
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402

plt.rcParams.update({"font.family": "serif", "font.serif": ["Times New Roman", "Liberation Serif", "DejaVu Serif"], "font.size": 8})


def ci(values: list[float], rng: random.Random) -> tuple[float, float, float]:
    boot = sorted(statistics.mean(rng.choices(values, k=len(values))) for _ in range(5000))
    return statistics.mean(values), boot[125], boot[4874]


def bars(ax, groups: list[str], systems: list[tuple[str, str, str]], rows: list[dict], rng: random.Random, metric_keys: list[str]) -> None:
    width = 0.8 / len(systems)
    for s, (prefix, label, color) in enumerate(systems):
        means, lo, hi = [], [], []
        for key in metric_keys:
            vals = [float(r[f"{prefix}_{key}"]) for r in rows if r[f"{prefix}_{key}"] not in ("", None)]
            m, a, b = ci(vals, rng)
            means.append(m)
            lo.append(m - a)
            hi.append(b - m)
        xs = [i + (s - (len(systems) - 1) / 2) * width for i in range(len(metric_keys))]
        ax.bar(xs, means, width, yerr=[lo, hi], capsize=2, label=label, color=color, edgecolor="black", linewidth=0.4, error_kw={"linewidth": 0.6})
        for x, m, h in zip(xs, means, hi):
            ax.text(x, m + h + 0.015, f"{m:.2f}", ha="center", va="bottom", fontsize=6)
    ax.set_xticks(range(len(groups)), groups)
    ax.set_ylim(0, 1.2)
    ax.set_ylabel("Mean over scenarios (95% CI)")
    ax.grid(axis="y", linewidth=0.3, alpha=0.6)
    ax.set_axisbelow(True)
    ax.legend(frameon=False, ncol=len(systems), loc="upper center", bbox_to_anchor=(0.5, 1.14), fontsize=7)


def main() -> None:
    out = Path(sys.argv[1])
    rng = random.Random(42)
    rec = list(csv.DictReader((out / "h1_recommendation.csv").open(encoding="utf-8")))
    lay = list(csv.DictReader((out / "h2_layout.csv").open(encoding="utf-8")))

    fig, ax = plt.subplots(figsize=(3.4, 2.1))
    bars(ax, ["nDCG@5", "Precision@5", "Room-fit rate"],
         [("b1", "B1: price filter", "#d9d9d9"), ("b1s", "B1s: price + style", "#969696"), ("arca", "Arca ranker", "#252525")],
         rec, rng, ["ndcg", "p", "fit"])
    fig.tight_layout()
    fig.savefig(out / "fig_h1_recommendation.png", dpi=300)

    fig, ax = plt.subplots(figsize=(3.4, 2.1))
    bars(ax, ["Walkway", "Wall contact", "Relations", "Composite"],
         [("b2", "B2: random valid", "#bdbdbd"), ("arca", "Arca solver", "#252525")],
         lay, rng, ["walkway", "wall", "relations", "guideline"])
    fig.tight_layout()
    fig.savefig(out / "fig_h2_layout.png", dpi=300)


if __name__ == "__main__":
    main()
