from datetime import datetime
from pydantic import BaseModel, Field, ConfigDict
from typing import Literal


VacancyLevel = Literal[
        "intern",
        "junior",
        "middle",
        "senior",
        "lead",
    ]
ExperienceType = Literal[
        "noExperience",
        "between1And3",
        "between3And6",
        "moreThan6",
    ]


class VacancySearchCriteria(BaseModel):

    source: str = Field(
        default="hh",
        description="Vacancy source: hh, mock, etc.",
    )
    text: str | None = Field(
        default=None,
        min_length=1,
        description="Search text, for example: Python backend junior",
    )
    company: str | None = Field(default=None, min_length=1)

    area: int | None = Field(default=None, ge=1)
    salary_from: int | None = Field(default=None, ge=0)
    only_with_salary: bool = False

    page: int = Field(default=0, ge=0)
    per_page: int = Field(default=20, ge=1, le=100)

    experience: ExperienceType | None = None
    level: VacancyLevel | None = None

    include_keywords: list[str] = Field(default_factory=list)
    exclude_keywords: list[str] = Field(default_factory=list)


class VacancySearchItem(BaseModel):
    external_id: str
    source: str = "hh"

    title: str
    company: str | None = None
    location: str | None = None

    salary_min: int | None = Field(default=None, ge=0)
    salary_max: int | None = Field(default=None, ge=0)
    currency: str | None = None
    salary_gross: bool | None = None

    url: str | None = None
    published_at: datetime | None = None


class VacancySearchResponse(BaseModel):
    items: list[VacancySearchItem]
    found: int = 0
    page: int = 0
    per_page: int = 20


class VacancyHtmlParseRequest(BaseModel):
    source: str
    html: str
    page: int = Field(default=0, ge=0)
    per_page: int = Field(default=20, ge=1, le=100)


class FoundVacancyRead(BaseModel):
    id: int
    search_run_id: int

    external_id: str
    source: str

    title: str
    company: str | None = None
    location: str | None = None

    salary_min: int | None = None
    salary_max: int | None = None
    currency: str | None = None
    salary_gross: bool | None = None

    url: str | None = None
    published_at: datetime | None = None

    created_at: datetime

    model_config = {
        "from_attributes": True
    }


class VacancySearchRunRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: int

    source: str
    query_text: str | None = None
    company: str | None = None
    area: int | None = None
    salary_from: int | None = None
    only_with_salary: bool

    experience: str | None = None
    level: str | None = None

    found_count: int
    created_at: datetime


class VacancySearchSavedResponse(BaseModel):
    search_run: VacancySearchRunRead
    items: list[FoundVacancyRead]
    found: int
    page: int
    per_page: int
