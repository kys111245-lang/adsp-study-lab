# ADsP Study Lab

**학습 로드맵, 개념 정리, 공식 계산, 플래시카드와 모의문제를 한 화면에서 사용하는 학습 웹앱입니다.**

[웹앱 실행하기](https://kys111245-lang.github.io/adsp-study-lab/) · [검증 기록](docs/VERIFICATION.md)

## 목적

학습 중 개념을 읽고, 암기하고, 문제로 확인하는 흐름을 짧은 동선으로 구성한 개인 학습용 프로젝트입니다. 생성형 AI의 도움을 받아 만든 결과물을 학습 목적에 맞게 활용한 사례입니다.

## 기능

- 학습 순서를 정리한 로드맵
- 핵심 개념과 공식 계산
- 뒤집어 보는 플래시카드와 OX 확인
- 모의문제와 결과 확인
- 손글씨 학습용 PDF 다운로드·인쇄

## 기술과 구조

| 파일 | 역할 |
| --- | --- |
| `index.html` | HTML·CSS·JavaScript 화면과 학습 상호작용 |
| `run_app.py` | Python 표준 라이브러리 로컬 서버 |
| `generate_pdf.py` | ReportLab 기반 워크북 생성 |
| `adsp_handwriting_workbook.pdf` | 다운로드 가능한 학습용 워크북 |

Tailwind CSS, KaTeX, Font Awesome을 CDN으로 불러옵니다. 인터넷 연결이 있어야 외부 스타일·수식 기능이 완전히 표시됩니다.

## 실행

설치 없이 로컬 서버로 실행:

```sh
python -m http.server 8000 --bind 127.0.0.1
```

브라우저에서 `http://127.0.0.1:8000`을 엽니다.

Windows에서 PDF를 다시 생성할 경우:

```sh
python -m pip install -r requirements.txt
python generate_pdf.py
```

PDF 생성기는 Windows의 맑은 고딕 폰트 경로를 사용합니다. 다른 운영체제에서는 코드의 폰트 경로를 변경해야 합니다.

## 범위

개인 학습을 위한 비공식 자료입니다. 화면의 학습 계획과 문항은 공식 시험 출제·합격을 보장하지 않습니다. 교육기관의 원본 교재·시험지는 포함하지 않았습니다.

## 다음 개선

학습 데이터와 화면 코드 분리, 오답 저장, 내용 검토 이력 관리가 다음 개선 과제입니다.
