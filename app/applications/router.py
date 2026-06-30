from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session
from app import crud, schemas
from app.database import get_db
from app.models import ApplicationStatus


router = APIRouter(
    prefix="/applications",
    tags=["applications"],
)


@router.post(
    "",
    response_model=schemas.ApplicationRead,
    status_code=status.HTTP_201_CREATED,
)
def create_application(
    data: schemas.ApplicationCreate,
    db: Session = Depends(get_db),
):
    return crud.create_application(db=db, data=data)


@router.post(
    "/from-vacancy/{found_vacancy_id}",
    response_model=schemas.ApplicationRead,
    status_code=status.HTTP_201_CREATED,
)
def create_application_from_vacancy(
    found_vacancy_id: int,
    db: Session = Depends(get_db),
):
    return crud.create_application_from_found_vacancy(
        db=db,
        found_vacancy_id=found_vacancy_id,
    )


@router.get(
    "",
    response_model=list[schemas.ApplicationRead],
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


@router.get(
    "/{application_id}",
    response_model=schemas.ApplicationRead,
)
def get_application(
    application_id: int,
    db: Session = Depends(get_db),
):
    application = crud.get_application(
        db=db,
        application_id=application_id,
    )

    if application is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Application not found",
        )

    return application


@router.patch(
    "/{application_id}",
    response_model=schemas.ApplicationRead,
)
def update_application(
    application_id: int,
    data: schemas.ApplicationUpdate,
    db: Session = Depends(get_db),
):
    application = crud.get_application(
        db=db,
        application_id=application_id,
    )

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


@router.delete(
    "/{application_id}",
    status_code=status.HTTP_204_NO_CONTENT,
)
def delete_application(
    application_id: int,
    db: Session = Depends(get_db),
):
    application = crud.get_application(
        db=db,
        application_id=application_id,
    )

    if application is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Application not found",
        )

    crud.delete_application(db=db, application=application)

    return None
