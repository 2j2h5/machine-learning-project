# Lab 4-2 — 재현 방법

학번 20201068 / 이름 이지호

## 환경

- Python 3.10.x, CPU only, 실행 시간 수 초
- 시드: 42 (코드에 고정)
- `requirements.txt`가 고정한 버전(특히 `numpy<2`)을 그대로 설치한다.

## 명령어

제출 규정에 따라 이 폴더에는 `src/`, `report.pdf`, `results.json`, `README.md`만 있다. `requirements.txt`, `data/motor_health.csv`, `tests/`는 과제 배포본(`lab04_2_pytorch.zip`)에 있다. 다음 순서로 실행한다.

1. 배포본을 푼다.
2. 배포본의 `src/lab04_2.py`를 이 폴더의 `src/lab04_2.py`로 덮어쓴다.
3. 배포본 폴더 루트에서 아래 명령을 실행한다.

```bash
pip install -r requirements.txt
python src/lab04_2.py            # results.json 생성
python -m pytest tests/ -q       # 공개 테스트 6개
```

`python src/lab04_2.py`는 hidden size 2개 x learning rate 3개 그리드를 검증셋으로 비교하고, 선택된 설정을 테스트셋에서 한 번만 평가한다. 결과는 배포본 폴더 루트의 `results.json`에 쓴다. 두 번 실행해도 `runtime_seconds`를 제외한 값은 같고, 제출한 `results.json`과도 같다.

## 보고서의 그림

`report.pdf`의 Figure 1~3은 배포본의 `notebooks/lab04_2_visualization.ipynb`에서 플롯 셀 세 개를 직접 채워 만들었다. 제출 규정상 노트북은 포함하지 않으므로, 그림은 `report.pdf`에서 확인한다.
