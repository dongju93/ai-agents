# Warm-up 프로젝트

OpenAI API를 활용한 기초 AI 개발 실습 프로젝트입니다.

## 📋 개요

이 프로젝트는 AI Agent 개발을 시작하기 전 OpenAI API와 Python 환경에 익숙해지기 위한 워밍업 프로젝트입니다. 기본적인 OpenAI API 호출과 Jupyter 노트북을 활용한 실험을 포함합니다.

## 🛠 기술 스택

- **Python** 3.13+
- **OpenAI API** 1.102.0+
- **JupyterLab** 4.4.6+
- **uv** 패키지 매니저

## 🚀 설치 및 실행

### 1. 환경 설정

```bash
# 의존성 설치
uv sync

# 개발 도구 설치
uv sync --group dev
```

### 2. 환경 변수 설정

`.env` 파일을 생성하고 OpenAI API 키를 설정하세요:

```bash
OPENAI_API_KEY=your_openai_api_key_here
```

### 3. 실행

```bash
# Python 스크립트 실행
uv run python main.py

# Jupyter Lab 실행 (개발용)
uv run jupyter lab
```

## 📁 프로젝트 구조

```
warm-up/
├── main.py          # 메인 Python 스크립트
├── main.ipynb       # Jupyter 노트북
├── pyproject.toml   # 프로젝트 의존성 설정
├── .env             # 환경 변수 (API 키 등)
└── README.md        # 프로젝트 문서
```

## 📚 학습 내용

- OpenAI API 기본 사용법
- Python 환경 설정 및 의존성 관리
- Jupyter 노트북을 활용한 실험
- AI API 응답 처리 및 에러 핸들링
