"""Verify the actual ZIP in isolation; local verification tool, not submitted."""
import io
import argparse
import json
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path
from zipfile import ZipFile

from pypdf import PdfReader

ROOT = Path(__file__).resolve().parents[1]
LAB = ROOT.parents[1] / "lab01_eda"
sys.path.insert(0, str(LAB / "src"))
import lab01


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--python", default=sys.executable, help="Interpreter used to reproduce results")
    args = parser.parse_args()
    archive = ROOT / f"{lab01.STUDENT_ID}_{lab01.STUDENT_NAME}_lab01.zip"
    with ZipFile(archive) as zipped:
        expected_names = {"src/lab01.py", "report.pdf", "results.json", "README.md"}
        assert set(zipped.namelist()) == expected_names
        assert len(zipped.namelist()) == len(expected_names)
        assert all(info.file_size <= 10 * 2**20 for info in zipped.infolist())
        expected = json.loads(zipped.read("results.json"))
        assert expected["student_id"] == lab01.STUDENT_ID and expected["name"] == lab01.STUDENT_NAME
        assert expected["seed"] == 42 and expected["lab"] == "lab01"
        pdf = PdfReader(io.BytesIO(zipped.read("report.pdf")))
        assert 1 <= len(pdf.pages) <= 3
        assert sum(len(page.images) for page in pdf.pages) == 3
        text = "\n".join(page.extract_text() for page in pdf.pages)
        assert lab01.STUDENT_ID in text and lab01.STUDENT_NAME in text
        assert "PREVIEW" not in text and "pending" not in text
        for required in ("Figure 1", "Figure 2", "Figure 3", "Table 1", "Table 2",
                         "Interpretation", "Limitations", "AI & external-code usage"):
            assert required in text, required
        with tempfile.TemporaryDirectory(prefix="lab01-zip-check-") as temp:
            work = Path(temp)
            zipped.extractall(work)
            shutil.copytree(LAB / "data", work / "data")
            shutil.copytree(LAB / "tests", work / "tests")
            shutil.copy2(LAB / "requirements.txt", work / "requirements.txt")
            subprocess.run([args.python, "-I", "-B", "-X", "utf8", "src/lab01.py"],
                           cwd=work, check=True)
            subprocess.run([args.python, "-I", "-B", "-X", "utf8", "-m", "pytest", "tests/", "-q", "-p", "no:cacheprovider"],
                           cwd=work, check=True)
            actual = json.loads((work / "results.json").read_text(encoding="utf-8"))
            for key in ("lab", "student_id", "name", "seed", "metrics"):
                assert actual[key] == expected[key], key
    print("PASS: exact archive contents, size limits, identity, seed, selectable PDF text,")
    print("three embedded figures, and identical metrics using the selected interpreter.")


if __name__ == "__main__":
    main()
