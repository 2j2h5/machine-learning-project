# machine-learning-project

중앙대학교 2026년 2학기(Fall) 머신러닝프로젝트(Machine Learning Project, 53744-01) 과목의 실습(lab) 레포지토리입니다.

## Lab 목록

| 폴더 | 주제 |
|------|------|
| [`lab00`](lab00) | Warm-up: 버전 관리(git)와 6가지 핵심 ML 수식 (sigmoid, softmax, entropy, cross-entropy, KL divergence, focal loss) |
| [`lab01`](lab01) | 환경 설정 및 pandas 데이터 처리 (EDA) |
| [`lab02`](lab02) | scikit-learn을 이용한 분류(Classification)와 회귀(Regression) |
| [`lab03`](lab03) | K-means, GMM, EM |

## 폴더 구조

```
lab0X/
├── README.md          # 과제 설명
├── requirements.txt   # 해당 lab의 의존성
├── src/lab0X.py       # 구현 코드
└── tests/             # 공개 테스트 (test_public.py)
```

- `lab01`~`lab03`에는 추가로 `data/`, `notebooks/`, `check_submission.py`, `report_template.md`, `lab0X_concepts.pdf`가 있습니다.
- `submissions/`: lab01~lab03 제출물(리포트, 그림, 결과 파일 등).

## 실행 환경

lab별로 `requirements.txt`가 따로 있으며, lab01 README 기준 Python 3.10.x입니다.

```bash
cd lab03
pip install -r requirements.txt
pytest tests
```

## 라이선스

MIT License ([LICENSE](LICENSE)).
