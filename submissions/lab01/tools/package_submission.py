"""Build the exact four-item archive after real student details are supplied."""
import json
import re
import shutil
import subprocess
import sys
from pathlib import Path
from zipfile import ZIP_DEFLATED, ZipFile

ROOT = Path(__file__).resolve().parents[1]
LAB = ROOT.parents[1] / "lab01_eda"
sys.path.insert(0, str(LAB / "src"))
import lab01


def main():
    student_id, name = lab01.STUDENT_ID, lab01.STUDENT_NAME
    if not re.fullmatch(r"\d{8}", student_id) or student_id == "00000000":
        raise ValueError("A real eight-digit student ID is required.")
    if not re.fullmatch(r"[A-Za-z가-힣]+", name) or name == "None":
        raise ValueError("A real student name without spaces is required.")
    subprocess.run([sys.executable, "-B", "-X", "utf8", str(LAB / "src/lab01.py")], cwd=LAB, check=True)
    shutil.move(str(LAB / "results.json"), str(ROOT / "results.json"))
    subprocess.run([sys.executable, "-B", "-X", "utf8", str(ROOT / "tools/build_report.py")], cwd=ROOT, check=True)
    archive = ROOT / f"{student_id}_{name}_lab01.zip"
    members = {
        "src/lab01.py": LAB / "src/lab01.py",
        "report.pdf": ROOT / "report.pdf",
        "results.json": ROOT / "results.json",
        "README.md": ROOT / "README.md",
    }
    with ZipFile(archive, "w", ZIP_DEFLATED) as zipped:
        for relative, source in members.items():
            zipped.write(source, arcname=relative)
    with ZipFile(archive) as zipped:
        assert set(zipped.namelist()) == set(members)
        assert {p.split("/")[0] for p in zipped.namelist()} == {
            "src", "report.pdf", "results.json", "README.md"
        }
        assert all(info.file_size <= 10 * 2**20 for info in zipped.infolist())
        result = json.loads(zipped.read("results.json"))
        assert result["student_id"] == student_id and result["name"] == name
        assert result["lab"] == "lab01" and result["seed"] == 42
    subprocess.run([sys.executable, "-B", "-X", "utf8", str(LAB / "check_submission.py"), str(archive)], check=True)
    print(f"Submission: {archive}")


if __name__ == "__main__":
    main()
