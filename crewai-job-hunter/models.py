from typing import Annotated

from pydantic import BaseModel, Field


class Job(BaseModel):
    """Simplified Job model with only essential fields typically available in job postings"""

    # Required basic information - always available in job postings
    job_title: Annotated[str, Field(description="Job title")]
    company_name: Annotated[str, Field(description="Company name")]
    job_posting_url: Annotated[str, Field(description="Job posting URL")]
    job_summary: Annotated[str, Field(description="Job description/summary")]

    # Optional but commonly available information
    company_location: Annotated[str | None, Field(description="Company location")] = (
        None
    )
    employment_type: Annotated[
        str | None, Field(description="Full-time, Part-time, Contract")
    ] = None
    compensation: Annotated[
        str | None, Field(description="Salary/compensation information")
    ] = None
    is_remote_friendly: Annotated[
        bool | None, Field(description="Remote work availability")
    ] = None

    # Qualification requirements - often available
    required_technologies: Annotated[
        list[str] | None, Field(description="Required technical skills")
    ] = None
    years_of_experience_required: Annotated[
        str | None, Field(description="Required years of experience")
    ] = None
    role_seniority_level: Annotated[
        str | None, Field(description="Junior, Intermediate, Senior")
    ] = None


class JobList(BaseModel):
    jobs: list[Job]


class RankedJob(BaseModel):
    job: Job
    match_score: Annotated[int, Field(ge=1, le=5, description="Match score from 1 (poor fit) to 5 (perfect fit)")]
    reason: str


class RankedJobList(BaseModel):
    ranked_jobs: list[RankedJob]


class ChosenJob(BaseModel):
    job: Job
    selected: bool
    reason: str
