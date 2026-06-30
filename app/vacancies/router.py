from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database import get_db
from app.vacancies.crud import (
    get_found_vacancies_by_search_run,
    get_search_runs,
)
from app.vacancies.schemas import (
    FoundVacancyRead,
    VacancyHtmlParseRequest,
    VacancySearchCriteria,
    VacancySearchResponse,
    VacancySearchRunRead,
    VacancySearchSavedResponse,
)
from app.vacancies.service import (
    parse_html_to_vacancies,
    search_and_save_vacancies,
    search_vacancies_by_criteria,
)


router = APIRouter(
    prefix="/vacancies",
    tags=["vacancies"],
)


@router.post("/parse-html", response_model=VacancySearchResponse)
def parse_vacancies_html_endpoint(
    payload: VacancyHtmlParseRequest,
):
    return parse_html_to_vacancies(payload)


@router.post("/search", response_model=VacancySearchResponse)
def search_vacancies_endpoint(
    criteria: VacancySearchCriteria,
):
    return search_vacancies_by_criteria(criteria)


@router.post("/search-and-save", response_model=VacancySearchSavedResponse)
def search_and_save_vacancies_endpoint(
    criteria: VacancySearchCriteria,
    db: Session = Depends(get_db),
):
    return search_and_save_vacancies(
        db=db,
        criteria=criteria,
    )


@router.get("/search-runs", response_model=list[VacancySearchRunRead])
def list_search_runs(
    db: Session = Depends(get_db),
):
    return get_search_runs(db)


@router.get(
    "/search-runs/{search_run_id}/items",
    response_model=list[FoundVacancyRead],
)
def list_found_vacancies(
    search_run_id: int,
    db: Session = Depends(get_db),
):
    return get_found_vacancies_by_search_run(
        db=db,
        search_run_id=search_run_id,
    )
