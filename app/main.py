from fastapi import Depends, FastAPI
from sqlalchemy.orm import Session
from app.applications.router import router as applications_router
from app.vacancies.router import router as vacancies_router
from app import crud
from app.database import Base, engine, get_db


Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Job Application Tracker API",
    description=(
        "REST API for tracking job applications "
        "and interview statuses."
    ),
    version="0.1.0",
)

app.include_router(applications_router)
app.include_router(vacancies_router)


@app.get("/health", tags=["health"])
def health_check():
    return {"status": "ok"}


@app.get("/stats/summary", tags=["stats"])
def get_summary(db: Session = Depends(get_db)):
    return crud.get_stats_summary(db=db)
