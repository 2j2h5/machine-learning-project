# Lab 6 — 20201068 이지호

## 재현 방법

Python 3.10, CPU만 사용. 과제 폴더(`data/cafe_daily.csv`, `requirements.txt`, `tests/`가 있는 곳)에 이 zip의 `src/lab06.py`를 덮어쓴 뒤, 과제 폴더 최상단에서 실행한다.

```bash
pip install -r requirements.txt   # numpy<2 고정을 그대로 따른다
python src/lab06.py               # results.json 생성 (CPU에서 약 9초)
python -m pytest tests/ -q        # 공개 테스트 6개
```

- 시드는 42로 고정되어 있고 `run_experiment` 맨 앞에서 `set_seed()`를 호출하므로, `results.json`은 `runtime_seconds`를 제외하고 매번 동일하다.
- 기대 결과(test 150 windows): persistence MAE 15.5067 / RMSE 20.0934 / MASE 0.9554, GRU MAE 9.4045 / RMSE 11.8727 / MASE 0.5794.
- 위 수치는 Windows 11, Python 3.10.22, numpy 1.26.4, torch 2.14.1+cpu에서 얻었다. PyTorch 버전이 다르면 GRU 수치가 소수 셋째 자리에서 달라질 수 있다(과제 README의 레퍼런스는 0.5725).
- `report.pdf`의 그림 1–3은 `notebooks/lab06_visualization.ipynb`의 그림 셀로 만들었다(노트북은 제출하지 않음).
