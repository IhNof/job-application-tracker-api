from fastapi import HTTPException, status

from app.vacancies.fetchers.hh import HHHtmlFetcher
from app.vacancies.schemas import VacancySearchCriteria


def fetch_vacancies_html(criteria: VacancySearchCriteria) -> str:
    if criteria.source == "hh":
        fetcher = HHHtmlFetcher()
        return fetcher.fetch_html(criteria)

    raise HTTPException(
        status_code=status.HTTP_400_BAD_REQUEST,
        detail=f"Unsupported vacancy source: {criteria.source}",
    )
