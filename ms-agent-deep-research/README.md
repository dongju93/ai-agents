# MS Agent Deep Research (Microsoft Agent Framework를 활용한 심층 리서치 및 이메일 최적화 에이전트)

Microsoft의 새로운 **Agent Framework**를 사용하여 두 가지의 독립적인 멀티 에이전트 시스템을 구현한 프로젝트입니다. 하나는 주어진 주제에 대해 심층적인 자율 리서치를 수행하고 보고서를 생성하며, 다른 하나는 전문가 에이전트들의 협업을 통해 이메일 초안을 반복적으로 개선합니다.

> **Note**: 이 프로젝트는 AutoGen 기반의 [autogen-deep-research](../autogen-deep-research/)에서 Microsoft Agent Framework로 마이그레이션된 버전입니다. AutoGen은 더 이상 새로운 기능이 추가되지 않으며, Microsoft Agent Framework가 공식 후속 프레임워크입니다.

## 🚀 핵심 프로젝트

이 저장소는 두 개의 주요 노트북 파일로 구성됩니다.

### 1. 심층 리서치 에이전트 (`deep-research.ipynb`)

- **목표**: 사용자가 입력한 주제에 대해 계획, 리서치, 분석, 검토의 전 과정을 자동화하여 고품질의 리서치 보고서를 생성합니다.
- **핵심 기능**:
  - **그래프 기반 워크플로우**: Agent Framework의 `Workflow` API를 사용하여 데이터 플로우 기반의 결정론적 워크플로우를 구현합니다.
  - **스트리밍 및 체크포인팅**: 중간 상태를 저장하고 필요 시 재개할 수 있는 체크포인트 기능을 활용합니다.
  - **자동 리서치 및 강화**: 리서치 계획을 수립하고 웹 검색을 수행한 후, 결과물의 허점을 파악하여 추가 리서치를 진행하는 `Enhancer` 에이전트가 포함됩니다.
  - **보고서 생성 및 저장**: 분석가 에이전트가 종합 보고서를 작성하면, 품질 검토 에이전트가 이를 평가하고 최종 결과물을 `.md` 파일로 저장합니다.
  - **Human-in-the-Loop**: 최종 승인 단계에서 사용자가 개입하여 결과물을 검토하거나 추가 작업을 요청할 수 있습니다.
  - **관찰성(Observability)**: OpenTelemetry 통합을 통해 에이전트 실행 과정을 추적하고 디버깅할 수 있습니다.

### 2. 이메일 최적화 에이전트 (`email-optimizer.ipynb`)

- **목표**: 간단한 이메일 초안을 명료성, 어조, 설득력 측면에서 전문가 에이전트들이 순차적으로 개선하여 최종 결과물을 완성합니다.
- **핵심 기능**:
  - **워크플로우 기반 협업**: 그래프 기반 워크플로우를 사용하여 '명료성 → 어조 → 설득력 → 종합 → 평가'의 데이터 플로우를 구현합니다.
  - **전문가 역할 분담**: 각 에이전트는 명료성(Clarity), 어조(Tone), 설득력(Persuasion) 등 하나의 전문 분야에만 집중하여 초안을 수정합니다.
  - **반복적 품질 개선**: 최종 평가를 담당하는 `CriticAgent`가 결과물이 기준에 미달한다고 판단하면, 개선점을 제시하며 워크플로우를 재실행합니다. 기준을 통과하면 프로세스를 종료합니다.
  - **미들웨어 통합**: 예외 처리, 로깅, 요청/응답 변환을 위한 커스텀 미들웨어를 활용합니다.

## 🤖 워크플로우

각 프로젝트는 Microsoft Agent Framework의 그래프 기반 워크플로우를 활용합니다.

### Deep Research 워크플로우 (Graph-based Workflow)

```mermaid
graph TD
    A[Start: User Task] --> B[research_planer];
    B --> C[research_agent];
    C --> D[research_enhancer];
    D -- "Gaps found" --> C;
    D -- "Sufficient" --> E[research_analyst];
    E -- "REPORT_COMPLETE" --> F[quality_reviewer];
    F -- "Save report" --> G[user_proxy];
    G -- "APPROVED" --> H[End];

    style A fill:#e1f5ff
    style H fill:#d4edda
    style G fill:#fff3cd
```

### Email Optimizer 워크플로우 (Sequential Workflow)

```mermaid
graph TD
    A[Start: Email Draft] --> B[ClarityAgent];
    B --> C[ToneAgent];
    C --> D[PersuasionAgent];
    D --> E[SynthesizerAgent];
    E --> F{CriticAgent};
    F -- "Needs improvement" --> B;
    F -- "Meets standards" --> G[End: Complete];

    style A fill:#e1f5ff
    style G fill:#d4edda
    style F fill:#f8d7da
```

## 🛠 기술 스택 및 주요 구현

- **Microsoft Agent Framework**: 멀티 에이전트 워크플로우 및 오케스트레이션을 위한 차세대 프레임워크 (AutoGen의 공식 후속)
  - **Graph-based Workflows**: 데이터 플로우 기반의 결정론적 워크플로우로 에이전트들을 연결합니다.
  - **Middleware System**: 요청/응답 처리, 예외 핸들링, 커스텀 파이프라인 구현을 위한 미들웨어를 제공합니다.
  - **Streaming & Checkpointing**: 실시간 스트리밍과 상태 저장/복원 기능을 지원합니다.
  - **OpenTelemetry Integration**: 내장된 관찰성 기능으로 에이전트 실행을 모니터링합니다.
- **LLM**: OpenAI `gpt-4o`, `gpt-4o-mini` 또는 Azure OpenAI Service
- **Tools Integration**: 웹 검색, 파일 I/O 등의 도구를 에이전트에 연결할 수 있습니다.
- **JupyterLab**: 노트북 환경에서 에이전트 시스템을 개발하고 실행합니다.

## 🔄 AutoGen에서의 주요 변경 사항

Microsoft Agent Framework로 마이그레이션하면서 다음과 같은 주요 변경이 이루어졌습니다:

| 항목                  | AutoGen                                                  | Microsoft Agent Framework                 |
| --------------------- | -------------------------------------------------------- | ----------------------------------------- |
| **워크플로우 패턴**   | `SelectorGroupChat`, `RoundRobinGroupChat` (이벤트 기반) | Graph-based Workflow (데이터 플로우 기반) |
| **에이전트 선택**     | LLM 기반 동적 선택                                       | 명시적 그래프 라우팅 + 조건부 분기        |
| **미들웨어**          | 없음                                                     | 내장 미들웨어 시스템 제공                 |
| **관찰성**            | 기본 로깅                                                | OpenTelemetry 통합                        |
| **체크포인팅**        | 제한적                                                   | 네이티브 지원 (상태 저장/복원)            |
| **Human-in-the-Loop** | `UserProxyAgent`                                         | Workflow interruption + approval nodes    |
| **엔터프라이즈 기능** | 실험적                                                   | 프로덕션 준비 완료 (CI/CD, 컨테이너 배포) |

**마이그레이션 이점**:

- 더 예측 가능하고 디버깅이 쉬운 워크플로우
- 엔터프라이즈 환경에 적합한 관찰성 및 모니터링
- 클라우드 네이티브 배포 지원 (Kubernetes, Docker, Serverless)
- Microsoft의 장기 지원 및 새로운 기능 추가

## 🤖 에이전트 구성

### Deep Research 에이전트

- **`research_planer`**: 복잡한 질문을 하위 리서치 작업으로 분해하고 구체적인 검색 쿼리를 생성합니다.
- **`research_agent`**: 생성된 쿼리를 사용하여 웹 검색을 수행하고 정보를 추출합니다.
- **`research_enhancer`**: 리서치 결과의 중대한 허점을 식별하고 필요한 경우 추가 검색을 제안합니다.
- **`research_analyst`**: 수집된 정보를 바탕으로 체계적인 종합 보고서를 작성합니다.
- **`quality_reviewer`**: 보고서의 완성도와 정확성을 평가하고, 기준 충족 시 파일로 저장합니다.
- **`user_proxy`**: 최종 결과물을 검토하고 승인하는 인간 사용자의 역할을 대리합니다.

### Email Optimizer 에이전트

- **`ClarityAgent`**: 모호함과 군더더기를 제거하여 메시지를 명확하고 간결하게 만듭니다.
- **`ToneAgent`**: 이메일의 어조를 청중에게 맞게 따뜻하고 전문적으로 다듬습니다.
- **`PersuasionAgent`**: 행동 유도(CTA)를 강화하고 논리를 보강하여 설득력을 높입니다.
- **`SynthesizerAgent`**: 이전 에이전트들의 제안을 종합하여 통일성 있는 최종 초안을 작성합니다.
- **`CriticAgent`**: 최종 초안의 품질을 평가하고, 기준에 미치지 못하면 수정을 지시하고, 만족하면 프로세스를 종료합니다.

## 🚀 설치 및 실행

### 1. 환경 설정

```bash
# 저장소 복제 및 이동
git clone https://github.com/your-username/ms-agent-deep-research.git
cd ms-agent-deep-research

# 가상 환경 생성 및 의존성 설치 (uv 사용 권장)
uv venv
uv sync
```

### 2. Microsoft Agent Framework 설치

```bash
# Python 환경에 Agent Framework 설치
uv pip install agent-framework --pre

# 또는 pip 사용
pip install agent-framework --pre
```

### 3. 환경 변수 설정

`.env` 파일을 생성하고 필요한 API 키를 설정하세요:

```bash
# OpenAI API (또는 Azure OpenAI Service)
OPENAI_API_KEY="your_openai_api_key_here"

# 웹 검색 도구 (선택사항)
FIRECRAWL_API_KEY="your_firecrawl_api_key_here"

# Azure OpenAI를 사용하는 경우
# AZURE_OPENAI_API_KEY="your_azure_openai_key"
# AZURE_OPENAI_ENDPOINT="https://your-resource.openai.azure.com/"
# AZURE_OPENAI_DEPLOYMENT_NAME="gpt-4o"
```

### 4. 실행

JupyterLab을 실행하고, 각 `.ipynb` 파일을 열어 셀을 순차적으로 실행합니다.

```bash
# JupyterLab 실행
uv run jupyter lab
```

- **`deep-research.ipynb`**: 마지막 셀의 `task` 변수에 리서치할 주제를 입력하고 실행합니다.
- **`email-optimizer.ipynb`**: 마지막 셀의 `task` 변수에 최적화할 이메일 초안을 입력하고 실행합니다.

## 📁 프로젝트 구조

```
ms-agent-deep-research/
├── deep-research.ipynb     # 심층 리서치 에이전트 워크플로우
├── email-optimizer.ipynb   # 이메일 최적화 에이전트 워크플로우
├── agents/                 # 에이전트 정의 모듈
│   ├── research_agents.py  # 리서치 관련 에이전트들
│   └── email_agents.py     # 이메일 최적화 에이전트들
├── workflows/              # 워크플로우 정의
│   ├── research_workflow.py
│   └── email_workflow.py
├── tools/                  # 에이전트 도구
│   ├── web_search.py       # 웹 검색 도구
│   └── file_operations.py  # 파일 저장 도구
├── middleware/             # 커스텀 미들웨어
│   └── logging_middleware.py
├── report.md               # [생성됨] 리서치 결과 보고서
├── pyproject.toml          # 프로젝트 의존성
├── .env                    # 환경 변수
└── README.md
```

## 💻 최종 결과물

- **`deep-research.ipynb`**: 실행이 완료되면 프로젝트 루트 디렉토리에 `report.md` 파일이 생성됩니다.
- **`email-optimizer.ipynb`**: 최종적으로 개선된 이메일 텍스트가 콘솔에 출력됩니다.

## 📚 참고 자료

- [Microsoft Agent Framework 공식 문서](https://learn.microsoft.com/en-us/agent-framework/)
- [AutoGen에서 마이그레이션 가이드](https://learn.microsoft.com/en-us/agent-framework/migration-guide/from-autogen/)
- [Agent Framework GitHub 저장소](https://github.com/microsoft/agent-framework)
- [원본 AutoGen 프로젝트](../autogen-deep-research/)

## 🔍 주요 특징

### 1. 프로덕션 준비 완료

- OpenTelemetry를 통한 내장 관찰성
- 미들웨어 시스템을 통한 예외 처리 및 로깅
- 체크포인팅을 통한 장애 복구

### 2. 엔터프라이즈 친화적

- 클라우드 네이티브 배포 지원 (Docker, Kubernetes)
- CI/CD 파이프라인 통합 가능
- Azure, AWS, GCP 등 다양한 클라우드 플랫폼 지원

### 3. 개발자 경험

- DevUI를 통한 대화형 개발 및 디버깅
- 그래프 기반 워크플로우로 직관적인 시각화
- Python과 .NET 모두 지원

## ⚠️ 알려진 제한 사항

- Microsoft Agent Framework는 현재 프리뷰 단계이므로 API가 변경될 수 있습니다.
- 일부 AutoGen의 고급 기능(예: 동적 그룹 채팅)은 명시적 워크플로우 그래프로 재구현해야 합니다.
- 프로덕션 배포 시 OpenTelemetry 백엔드(Jaeger, Zipkin 등) 설정이 권장됩니다.

## 📝 라이선스

이 프로젝트는 MIT 라이선스 하에 배포됩니다.

---

**Note**: AutoGen은 Microsoft에 의해 유지보수 모드로 전환되었으며, 버그 수정 및 보안 패치만 제공됩니다. 새로운 프로젝트는 Microsoft Agent Framework를 사용하는 것이 권장됩니다.
