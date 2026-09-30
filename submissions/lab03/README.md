# Lab 3 - Reproduce the submitted results

Student: 20201068 / 이지호

Use Python 3.10.x and the instructor's original Lab 3 package. The dataset and
requirements.txt are deliberately excluded from this submission, as required.

1. Extract the instructor's original lab03 package into a working folder.
2. Extract this submission ZIP into that same folder, replacing src/lab03.py.
   Keep the original data/lab03_scene.npz, requirements.txt, tests/, and
   check_submission.py. Run the commands below from that folder.

```text
python --version
python -m pip install -r requirements.txt
python src/lab03.py
python -m pytest tests/ -q
```

The script generates results.json (seed 42, about 1 second). Do not edit that
file manually. The expected public-test result is 6 passed.

Validate the archive from the working folder before uploading:

```text
python -X utf8 check_submission.py 20201068_이지호_lab03.zip
```

Implementation notes: one np.random.Generator (seed 42) is threaded through
kmeans, gmm_em and select_k in the docstring order; the GMM E-step is in log
space with log-sum-exp, and the log-density uses a Cholesky factorization
(helpers _sq_dists and _log_gauss).

The submitted report contains Figures 1-3 exported from the provided notebook.
The notebook and figure image files are not submission deliverables.
report_template.md is the filled-in source text of report.pdf.

AI use is disclosed in the report's usage table.
