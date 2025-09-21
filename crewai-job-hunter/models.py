from datetime import date
from typing import Annotated

from pydantic import BaseModel, Field


class Job(BaseModel):
    # 기본 정보
    job_title: Annotated[str, Field(description="직무 제목")]
    company_name: Annotated[str, Field(description="회사 이름")]
    company_location: Annotated[str, Field(description="회사 위치")]
    job_posting_url: Annotated[str, Field(description="직무 공고 URL")]
    job_summary: Annotated[str, Field(description="직무 요약")]

    # 근무 조건
    is_remote_friendly: Annotated[
        bool | None, Field(description="원격 근무 가능 여부")
    ] = None
    employment_type: Annotated[
        str | None, Field(description="Full-time, Part-time, Contract")
    ] = None
    compensation: Annotated[str | None, Field(description="보상 정보")] = None

    # 자격 요건
    key_qualifications: Annotated[
        list[str] | None, Field(description="주요 자격 요건")
    ] = None
    job_responsibilities: Annotated[
        list[str] | None, Field(description="직무 책임")
    ] = None
    required_technologies: Annotated[
        list[str] | None, Field(description="필요한 기술")
    ] = None
    role_seniority_level: Annotated[
        str | None, Field(description="Junior, Intermediate, Senior")
    ] = None

    years_of_experience_required: Annotated[
        str | None, Field(description="필요한 경력 연수")
    ] = None
    minimum_education: Annotated[str | None, Field(description="최소 학력 요건")] = None

    # 매칭 분석
    match_score: Annotated[
        int | None,
        Field(ge=0, le=100, description="이력서와의 매칭 점수 (0-100)"),
    ] = None
    skill_match_percentage: Annotated[
        int | None, Field(ge=0, le=100, description="보유 기술과의 일치율")
    ] = None
    missing_skills: Annotated[
        list[str] | None, Field(description="부족한 기술/스킬")
    ] = None
    matching_technologies: Annotated[
        list[str] | None, Field(description="보유 기술과 일치하는 요구사항")
    ] = None

    # 성장 및 기회
    growth_opportunities: Annotated[
        list[str] | None, Field(description="예상되는 성장 기회")
    ] = None
    learning_opportunities: Annotated[
        list[str] | None, Field(description="학습 가능한 새로운 기술")
    ] = None
    career_progression_path: Annotated[
        str | None, Field(description="경력 발전 경로")
    ] = None

    # 회사 및 팀 정보
    hiring_company_size: Annotated[
        str | None, Field(description="Startup, Mid-size, Large")
    ] = None
    hiring_industry: Annotated[str | None, Field(description="채용 산업")] = None
    team_size: Annotated[str | None, Field(description="팀 규모 (예: 5-10명)")] = None
    tech_stack: Annotated[
        list[str] | None, Field(description="회사에서 사용하는 기술 스택")
    ] = None

    # 혜택 및 조건
    job_benefits: Annotated[list[str] | None, Field(description="직무 혜택")] = None
    includes_equity: Annotated[
        bool | None, Field(description="주식 보상 포함 여부")
    ] = None
    offers_visa_sponsorship: Annotated[
        bool | None, Field(description="비자 스폰서십 제공 여부")
    ] = None
    work_life_balance_indicators: Annotated[
        list[str] | None, Field(description="워라밸 관련 정보")
    ] = None

    # 지원 관련 정보
    application_deadline: Annotated[date | None, Field(description="지원 마감일")] = (
        None
    )
    estimated_interview_process: Annotated[
        str | None, Field(description="예상 면접 프로세스")
    ] = None
    urgency_level: Annotated[
        str | None, Field(description="채용 긴급도 (High/Medium/Low)")
    ] = None

    # 메타데이터
    date_listed: Annotated[date | None, Field(description="공고 등록 날짜")] = None
    date_scraped: Annotated[date | None, Field(description="수집된 날짜")] = None

    # 추가 분석
    fit_reasoning: Annotated[
        str | None, Field(description="왜 이 포지션이 적합한지에 대한 설명")
    ] = None
    potential_concerns: Annotated[
        list[str] | None, Field(description="잠재적 우려사항")
    ] = None
    recommendation_priority: Annotated[
        str | None, Field(description="추천 우선순위 (High/Medium/Low)")
    ] = None


class JobList(BaseModel):
    jobs: list[Job]


class RankedJob(BaseModel):
    job: Job
    match_score: int
    reason: str


class RankedJobList(BaseModel):
    ranked_jobs: list[RankedJob]


class ChosenJob(BaseModel):
    job: Job
    selected: bool
    reason: str
