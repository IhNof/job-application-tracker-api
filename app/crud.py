from sqlalchemy import select, func
from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from app.models import Application, ApplicationStatus, FoundVacancy
from app.schemas import ApplicationCreate, ApplicationUpdate


def create_application(db: Session, data: ApplicationCreate) -> Application:
    application = Application(**data.model_dump())

    db.add(application)
    db.commit()
    db.refresh(application)

    return application


def create_application_from_found_vacancy(
    db: Session,
    found_vacancy_id: int,
) -> Application:
    found_vacancy = (
        db.query(FoundVacancy)
        .filter(FoundVacancy.id == found_vacancy_id)
        .first()
    )

    if found_vacancy is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Found vacancy not found",
        )

    existing_application = (
        db.query(Application)
        .filter(
            Application.source == found_vacancy.source,
            Application.external_id == found_vacancy.external_id,
        )
        .first()
    )

    if existing_application is not None:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Application already exists for this vacancy",
        )

    application = Application(
        company=found_vacancy.company or "Unknown company",
        position=found_vacancy.title,
        status=ApplicationStatus.draft,

        source=found_vacancy.source,
        external_id=found_vacancy.external_id,
        vacancy_url=found_vacancy.url,
        found_vacancy_id=found_vacancy.id,

        location=found_vacancy.location,

        salary_min=found_vacancy.salary_min,
        salary_max=found_vacancy.salary_max,
        currency=found_vacancy.currency,
        salary_gross=found_vacancy.salary_gross,
    )

    db.add(application)
    db.commit()
    db.refresh(application)

    return application


def get_application(db: Session, application_id: int) -> Application | None:
    return db.get(Application, application_id)


def get_applications(
    db: Session,
    status: ApplicationStatus | None = None,
    company: str | None = None,
    remote: bool | None = None,
    limit: int = 20,
    offset: int = 0,
) -> list[Application]:
    stmt = select(Application)

    if status is not None:
        stmt = stmt.where(Application.status == status)

    if company is not None:
        stmt = stmt.where(Application.company.ilike(f"%{company}%"))

    if remote is not None:
        stmt = stmt.where(Application.remote == remote)

    stmt = stmt.order_by(Application.created_at.desc())
    stmt = stmt.limit(limit).offset(offset)

    return list(db.scalars(stmt).all())


def update_application(
    db: Session,
    application: Application,
    data: ApplicationUpdate,
) -> Application:
    update_data = data.model_dump(exclude_unset=True)

    for field, value in update_data.items():
        setattr(application, field, value)

    db.commit()
    db.refresh(application)

    return application


def delete_application(db: Session, application: Application) -> None:
    db.delete(application)
    db.commit()


def get_stats_summary(db: Session) -> dict:
    total = db.scalar(select(func.count(Application.id)))

    rows = db.execute(
        select(Application.status, func.count(Application.id))
        .group_by(Application.status)
    ).all()

    return {
        "total": total,
        "by_status": {
            status.value: count
            for status, count in rows
        },
    }
