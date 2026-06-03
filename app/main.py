from fastapi import Depends, FastAPI, HTTPException, Query, status
from sqlalchemy.orm import Session

from app import crud, models, schemas
from app.database import Base, engine, get_db
from app.models import ApplicationStatus


Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Job Application Tracker API",
    description="REST API for tracking job applications and interview statuses.",
    version="0.1.0",
)


@app.get("/health", tags=["health"])
def health_check():
    return {"status": "ok"}


@app.post(
    "/applications",
    response_model=schemas.ApplicationRead,
    status_code=status.HTTP_201_CREATED,
    tags=["applications"],
)
def create_application(
    data: schemas.ApplicationCreate,
    db: Session = Depends(get_db),
):
    return crud.create_application(db=db, data=data)


@app.get(
    "/applications",
    response_model=list[schemas.ApplicationRead],
    tags=["applications"],
)
def list_applications(
    status: ApplicationStatus | None = None,
    company: str | None = None,
    remote: bool | None = None,
    limit: int = Query(default=20, ge=1, le=100),
    offset: int = Query(default=0, ge=0),
    db: Session = Depends(get_db),
):
    return crud.get_applications(
        db=db,
        status=status,
        company=company,
        remote=remote,
        limit=limit,
        offset=offset,
    )


@app.get(
    "/applications/{application_id}",
    response_model=schemas.ApplicationRead,
    tags=["applications"],
)
def get_application(
    application_id: int,
    db: Session = Depends(get_db),
):
    application = crud.get_application(db=db, application_id=application_id)

    if application is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Application not found",
        )

    return application


@app.patch(
    "/applications/{application_id}",
    response_model=schemas.ApplicationRead,
    tags=["applications"],
)
def update_application(
    application_id: int,
    data: schemas.ApplicationUpdate,
    db: Session = Depends(get_db),
):
    application = crud.get_application(db=db, application_id=application_id)

    if application is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Application not found",
        )

    return crud.update_application(
        db=db,
        application=application,
        data=data,
    )


@app.delete(
    "/applications/{application_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    tags=["applications"],
)
def delete_application(
    application_id: int,
    db: Session = Depends(get_db),
):
    application = crud.get_application(db=db, application_id=application_id)

    if application is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Application not found",
        )

    crud.delete_application(db=db, application=application)

    return None


@app.get("/stats/summary", tags=["stats"])
def get_summary(db: Session = Depends(get_db)):
    return crud.get_stats_summary(db=db)