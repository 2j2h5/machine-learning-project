# Lab 2 - Reproduce the submitted results

Student: 20201068 / 이지호

Use Python 3.10.x and the instructor's original Lab 2 package. The datasets and
requirements.txt are deliberately excluded from this submission, as required.

1. Extract the instructor's original lab02_classification.zip into a working folder.
2. Extract this submission ZIP into that same folder, replacing src/lab02.py.
   Keep the original data/clinic_noshow.csv, data/clinic_wait.csv,
   requirements.txt, tests/, and check_submission.py. Run the commands below
   from that folder.

```text
python --version
python -m pip install -r requirements.txt
python src/lab02.py
python -m pytest tests/ -q
```

On Windows, if multiple Python versions are installed, create a Python 3.10
environment first, then use its interpreter explicitly:

```powershell
py -3.10 -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
.\.venv\Scripts\python.exe src/lab02.py
.\.venv\Scripts\python.exe -m pytest tests/ -q
```

The script generates results.json. Do not edit that file manually. Seed 42,
student details, and all metrics should match the submitted JSON; measured
runtime_seconds may differ between runs or machines. The expected public-test
result is 9 passed. Verified with Python 3.10.21, NumPy 2.2.6, pandas 2.3.3,
scikit-learn 1.7.2, Matplotlib 3.10.9, and pytest 9.1.1.

Validate the archive from the instructor's working folder before uploading:

```text
python -X utf8 check_submission.py 20201068_이지호_lab02.zip
```

Implementation notes: split_data stratifies on y with random_state=42; both
metric functions use numpy only and return 0.0 for every zero denominator;
every StandardScaler sits inside a Pipeline, so it is fitted on the training
split only. The regression split uses train_test_split without stratify.

The submitted report contains Figures 1-3 exported from the provided notebook
after completing its plot cells. The notebook and figure image files are not
submission deliverables. Report creation used additional local authoring tools
(ReportLab and PyMuPDF); they are not imported by src/lab02.py and are not
required to reproduce the numerical results.

AI use is disclosed in the report's usage table (Table 3).
