# Lab 5 — 20201068 이지호

## 재현 방법

Python 3.10, CPU만 사용. 과제 폴더(`data/parts_shapes.npz`, `data/backbone_shapes6.pt`, `requirements.txt`가 있는 곳)에 이 zip의 `src/lab05.py`를 덮어쓴 뒤 실행한다.

```bash
pip install -r requirements.txt
python src/lab05.py            # results.json 생성 (약 2초)
python -m pytest tests/ -q     # 공개 테스트 6개
```

- 시드는 42로 고정되어 있어 `results.json`은 `runtime_seconds`를 제외하고 매번 동일하다.
- 기대 결과: baseline 0.2573, scratch 0.8240(학습 파라미터 7,940), transfer 0.9469(학습 파라미터 2,052).
- `report.pdf`의 그림 1–3은 `notebooks/lab05_visualization.ipynb`의 그림 셀로 만들었다(노트북은 제출하지 않음).
