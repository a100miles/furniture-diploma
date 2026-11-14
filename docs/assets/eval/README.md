# Baseline evaluation results

Outputs of `backend/scripts/evaluate_baselines.py` (seed 42) on `pipeline/data/mebel_kz.json` (4,084 items). The RMT final paper (`docs/submissions/rmt-final/`) reports these numbers.

| File | Content |
|------|---------|
| `h1_recommendation.csv` | 60 scenarios: nDCG@5, Precision@5 and room-fit rate for Arca, B1 (price filter) and B1s (price + style filter) |
| `h2_layout.csv` | 30 rooms: walkway, wall contact, relations and composite scores for the Arca solver and B2 (random valid placement, mean of 20 runs) |
| `summary.json` | Paired Wilcoxon tests, rank-biserial r and 95% bootstrap CIs |
| `fig_h1_recommendation.png`, `fig_h2_layout.png` | Paper figures 2 and 3 |
| `fig_architecture.png` | Paper figure 1 |

## Reproduce

```bash
cd backend
pip install -r requirements-dev.txt
python -m scripts.evaluate_baselines --data ../pipeline/data/mebel_kz.json --out ../docs/assets/eval
python -m scripts.plot_evaluation ../docs/assets/eval
```

The run takes about 20 s. Every CSV value and test statistic is deterministic; only `latency_s` and `runtime_s` change between machines.
