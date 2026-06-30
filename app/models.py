import enum
from datetime import datetime
from sqlalchemy import (
    Boolean,
    Column,
    DateTime,
    ForeignKey,
    Integer,
    String,
    UniqueConstraint,
    Enum,
    Text,
    func
)
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database import Base


class ApplicationStatus(str, enum.Enum):
    draft = "draft"
    applied = "applied"
    screening = "screening"
    interview = "interview"
    offer = "offer"
    rejected = "rejected"
    accepted = "accepted"


class Application(Base):
    __tablename__ = "applications"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)

    company: Mapped[str] = mapped_column(
        String(120),
        nullable=False,
        index=True,
    )
    position: Mapped[str] = mapped_column(String(150), nullable=False)

    status: Mapped[ApplicationStatus] = mapped_column(
        Enum(ApplicationStatus),
        default=ApplicationStatus.draft,
        nullable=False,
        index=True,
    )

    source: Mapped[str | None] = mapped_column(String(120), nullable=True)

    external_id: Mapped[str | None] = mapped_column(
        String(120),
        nullable=True,
        index=True,
    )

    vacancy_url: Mapped[str | None] = mapped_column(
        String(500),
        nullable=True,
    )

    found_vacancy_id: Mapped[int | None] = mapped_column(
        Integer,
        ForeignKey("found_vacancies.id", ondelete="SET NULL"),
        nullable=True,
        index=True,
    )

    location: Mapped[str | None] = mapped_column(String(120), nullable=True)

    remote: Mapped[bool] = mapped_column(
        Boolean,
        default=False,
        nullable=False,
    )

    salary_min: Mapped[int | None] = mapped_column(Integer, nullable=True)
    salary_max: Mapped[int | None] = mapped_column(Integer, nullable=True)
    currency: Mapped[str | None] = mapped_column(String(10), nullable=True)
    salary_gross: Mapped[bool | None] = mapped_column(Boolean, nullable=True)

    notes: Mapped[str | None] = mapped_column(Text, nullable=True)

    created_at: Mapped[datetime] = mapped_column(
        DateTime,
        server_default=func.now(),
        nullable=False,
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime,
        server_default=func.now(),
        onupdate=func.now(),
        nullable=False,
    )

    found_vacancy = relationship("FoundVacancy")

    __table_args__ = (
        UniqueConstraint(
            "source",
            "external_id",
            name="uq_application_source_external_id",
        ),
    )


class VacancySearchRun(Base):
    __tablename__ = "vacancy_search_runs"

    id = Column(Integer, primary_key=True, index=True)

    source = Column(String, nullable=False, index=True)
    query_text = Column(String, nullable=True)
    company = Column(String, nullable=True)
    area = Column(Integer, nullable=True)
    salary_from = Column(Integer, nullable=True)
    only_with_salary = Column(Boolean, default=False, nullable=False)

    found_count = Column(Integer, default=0, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)

    experience = Column(String, nullable=True)
    level = Column(String, nullable=True)

    vacancies = relationship(
        "FoundVacancy",
        back_populates="search_run",
        cascade="all, delete-orphan",
    )


class FoundVacancy(Base):
    __tablename__ = "found_vacancies"

    id = Column(Integer, primary_key=True, index=True)

    search_run_id = Column(
        Integer,
        ForeignKey("vacancy_search_runs.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )

    external_id = Column(String, nullable=False, index=True)
    source = Column(String, nullable=False, index=True)

    title = Column(String, nullable=False)
    company = Column(String, nullable=True)
    location = Column(String, nullable=True)

    salary_min = Column(Integer, nullable=True)
    salary_max = Column(Integer, nullable=True)
    currency = Column(String, nullable=True)
    salary_gross = Column(Boolean, nullable=True)

    url = Column(String, nullable=True)
    published_at = Column(DateTime, nullable=True)

    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)

    search_run = relationship(
        "VacancySearchRun",
        back_populates="vacancies",
    )

    __table_args__ = (
        UniqueConstraint(
            "search_run_id",
            "source",
            "external_id",
            name="uq_found_vacancy_per_search_run",
        ),
    )
