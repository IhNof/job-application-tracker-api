from datetime import datetime

from pydantic import BaseModel, Field, model_validator

from app.models import ApplicationStatus


class ApplicationBase(BaseModel):
    company: str = Field(..., min_length=1, max_length=120)
    position: str = Field(..., min_length=1, max_length=150)
    status: ApplicationStatus = ApplicationStatus.draft

    source: str | None = Field(default=None, max_length=120)
    location: str | None = Field(default=None, max_length=120)
    remote: bool = False

    salary_min: int | None = Field(default=None, ge=0)
    salary_max: int | None = Field(default=None, ge=0)

    notes: str | None = None

    @model_validator(mode="after")
    def validate_salary_range(self):
        if (
            self.salary_min is not None
            and self.salary_max is not None
            and self.salary_min > self.salary_max
        ):
            raise ValueError("salary_min cannot be greater than salary_max")

        return self


class ApplicationCreate(ApplicationBase):
    pass


class ApplicationUpdate(BaseModel):
    company: str | None = Field(default=None, min_length=1, max_length=120)
    position: str | None = Field(default=None, min_length=1, max_length=150)
    status: ApplicationStatus | None = None

    source: str | None = Field(default=None, max_length=120)
    location: str | None = Field(default=None, max_length=120)
    remote: bool | None = None

    salary_min: int | None = Field(default=None, ge=0)
    salary_max: int | None = Field(default=None, ge=0)
    notes: str | None = None

    external_id: str | None = None
    vacancy_url: str | None = None
    found_vacancy_id: int | None = None
    currency: str | None = None
    salary_gross: bool | None = None


class ApplicationRead(ApplicationBase):
    id: int
    created_at: datetime
    updated_at: datetime

    external_id: str | None = None
    vacancy_url: str | None = None
    found_vacancy_id: int | None = None
    currency: str | None = None
    salary_gross: bool | None = None

    model_config = {
        "from_attributes": True
    }
