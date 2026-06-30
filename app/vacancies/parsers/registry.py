from fastapi import HTTPException, status
from app.vacancies.parsers.hh import parse_hh_vacancies_html
from app.vacancies.schemas import VacancySearchItem


def parse_vacancies_html(
    source: str,
    html: str,
) -> list[VacancySearchItem]:
    if source == "hh":
        return parse_hh_vacancies_html(html)

    raise HTTPException(
        status_code=status.HTTP_400_BAD_REQUEST,
        detail=f"Unsupported vacancy parser source: {source}",
    )
