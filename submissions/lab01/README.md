# Lab 1 - Reproduce the submitted results

Student: 20201068 / 이지호

Use Python 3.10.x and the instructor's original Lab 1 package. The dataset and
requirements.txt are deliberately excluded from this submission, as required.

1. Extract the instructor's original lab01_eda.zip into a working folder.
2. Extract this submission ZIP into that same folder, replacing src/lab01.py.
   Keep the original data/cafe_sales.csv, requirements.txt, tests/, and
   check_submission.py. Run the commands below from that folder.

```text
python --version
python -m pip install -r requirements.txt
python src/lab01.py
python -m pytest tests/ -q
```

On Windows, if multiple Python versions are installed, create a Python 3.10
environment first, then use its interpreter explicitly:

```powershell
py -3.10 -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
.\.venv\Scripts\python.exe src/lab01.py
.\.venv\Scripts\python.exe -m pytest tests/ -q
```

The script generates results.json. Do not edit that file manually. Seed 42,
student details, and all metrics should match the submitted JSON; measured
runtime_seconds may differ between runs or machines. The expected public-test
result is 6 passed. Verified with Python 3.10.20, NumPy 2.2.6, pandas 2.3.3,
Matplotlib 3.10.9, and pytest 9.1.1.

Validate the archive from the instructor's working folder before uploading:

```text
python -X utf8 check_submission.py 20201068_이지호_lab01.zip
```

Cleaning removes exact duplicates before imputation, strips commas from unit
prices, fills quantities with the deduplicated median and casts them to int,
reconstructs only missing totals, and fills missing ratings with the rounded
deduplicated mean. Quantity outliers are flagged using k=1.5, not removed.

The submitted report contains Figures 1-3 exported from the provided notebook
after completing its plot cells. The notebook and figure image files are not
submission deliverables. Report creation used additional local authoring tools
(ReportLab and PyMuPDF); they are not imported by src/lab01.py and are not
required to reproduce the numerical results.

I used ChatGPT for consultation on the assignment requirements and implementation
approach, report design, and refactoring. I completed the remaining work myself,
including the initial implementation, plots, analysis, report text, testing, and
submission preparation. The report's usage table records this division of work.
