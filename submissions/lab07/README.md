# Lab 7 — 20201068 이지호

## 재현 방법

Python 3.10, CPU만 사용. 과제 폴더(`data/machine_events.npz`, `requirements.txt`, `tests/`가 있는 곳)에 이 zip의 `src/lab07.py`를 덮어쓴 뒤 실행한다.

```bash
pip install -r requirements.txt
python src/lab07.py            # results.json 생성 (약 7초)
python -m pytest tests/ -q     # 공개 테스트 6개
```

- 시드는 42로 고정되어 있어 `results.json`은 `runtime_seconds`를 제외하고 매번 동일하다.
- 기대 결과: mean_pool 0.4750, encoder_nopos 0.4890, encoder_pos 0.9660 (pe_gap 0.4770).
  (torch 2.14.1+cpu, numpy 1.26.4에서 측정. PyTorch 버전이나 CPU에 따라 정확도가 0.01 정도 달라질 수 있음.)
- `report.pdf`의 그림 1–3은 `notebooks/lab07_visualization.ipynb`의 그림 셀로 만들었다(노트북은 제출하지 않음).
