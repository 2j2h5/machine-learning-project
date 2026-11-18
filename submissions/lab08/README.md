# Lab 8 — how to reproduce

Python 3.10, CPU only. Copy `src/lab08.py` from this zip into the original lab folder (it needs the
handout's `data/`, `tests/` and `requirements.txt`), then run everything from the lab folder root:

```bash
pip install -r requirements.txt   # numpy<2, scipy<1.15 as pinned
python src/lab08.py               # writes results.json (about 1 s)
python -m pytest tests/ -q        # 6 public tests
```

Where the report numbers come from:

| Report item | Source |
|-------------|--------|
| Table 1, Figure 2 | `python -c "import sys; sys.path.insert(0, 'src'); import lab08; t = lab08.run_ablation(lab08.BASE_CONFIG, lab08.FACTORS); print(t.groupby('variant', sort=False)['f1'].agg(['mean', 'std']).round(4))"` |
| Table 2, Figure 1 | `python -c "import sys; sys.path.insert(0, 'src'); import lab08; print(lab08.error_analysis(*lab08.base_predictions()))"` |
| Figure 3, ranking | `results.json` (`ranking_*` keys), from `summarize` over base vs. challenger |
| Island under `features=with_region` (§4) | `python -c "import sys; sys.path.insert(0, 'src'); import lab08; r = lab08._slice_report({**lab08.BASE_CONFIG, 'features': 'with_region'}); print(r['worst_slice'], r['worst_gap'], r['slices']['island'])"` |

Figures 1–3 were exported from the handout notebook `notebooks/lab08_experiments.ipynb` with its three
plot cells filled in. As instructed, the notebook itself is not submitted.

`_slice_report` is a private helper added inside the Task 3 TODO block; `main()` does not call it.
