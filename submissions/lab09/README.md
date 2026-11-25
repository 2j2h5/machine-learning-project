# Lab 9 — how to reproduce

Python 3.10, CPU only. Copy `src/lab09.py` from this zip into the original lab folder. It needs the
handout's `data/`, `tests/` and `requirements.txt`. Then run everything from the lab folder root:

```bash
pip install -r requirements.txt   # numpy<2, torch<3 as pinned
python src/lab09.py               # writes results.json (about 20 s on CPU)
python -m pytest tests/ -q        # 6 public tests
```

Every value in `results.json` reproduces byte-for-byte except `runtime_seconds`, `gan_sample_seconds` and
`ddpm_sample_seconds`, which are wall-clock measurements.

Where the report numbers come from:

| Report item | Source |
|-------------|--------|
| Table 1, Figures 1–3 | `results.json` (seed 42); Figures 1–3 were drawn in the handout notebook `notebooks/lab09_visualization.ipynb` with its three plot cells filled in |
| Table 2 (RNG seeds 0–4) | `python -c "import sys, torch; sys.path.insert(0, 'src'); import lab09; d = lab09.load_data('data/lab09_ring.npz'); [print(s, (m := lab09.run_experiment(d, torch.Generator().manual_seed(s)))['coverage_gan'], m['hq_gan'], m['coverage_ddpm'], m['hq_ddpm']) for s in range(5)]"` (about 2 min) |
| Mean distances to the center, on-ring share of misses (§4) | nearest-center distances of `out["samples_gan"]` / `out["samples_ddpm"]` from `run_experiment(..., out=out)`, computed outside `src/` |

The notebook is a working tool and is not submitted, as instructed. No private helpers were added to
`src/lab09.py`.
