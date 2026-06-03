from sqlalchemy import select, func
from sqlalchemy.orm import Session

from app.models import Application, ApplicationStatus
from app.schemas import ApplicationCreate, ApplicationUpdate


def create_application(db: Session, data: ApplicationCreate) -> Application:
    application = Application(**data.model_dump())

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