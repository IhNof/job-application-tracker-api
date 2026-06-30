from sqlalchemy.orm import Session
from typing import cast
from app.vacancies.crud import (
    create_found_vacancies,
    create_search_run,
)
from app.vacancies.fetchers.registry import fetch_vacancies_html
from app.vacancies.parsers.registry import parse_vacancies_html
from app.vacancies.schemas import (
    VacancyHtmlParseRequest,
    VacancySearchCriteria,
    VacancySearchResponse,
    VacancySearchSavedResponse,
    VacancySearchRunRead,
    FoundVacancyRead,
    VacancySearchItem
)
from app.vacancies.filters import filter_by_level


def parse_html_to_vacancies(
    payload: VacancyHtmlParseRequest,
) -> VacancySearchResponse:
    items = parse_vacancies_html(
        source=payload.source,
        html=payload.html,
    )

    return VacancySearchResponse(
        items=items[: payload.per_page],
        found=len(items),
        page=payload.page,
        per_page=payload.per_page,
    )


def _search_and_filter_vacancies(
    criteria: VacancySearchCriteria,
) -> list[VacancySearchItem]:
    html = fetch_vacancies_html(criteria)

    items = parse_vacancies_html(
        source=criteria.source,
        html=html,
    )

    items = filter_by_level(
        vacancies=items,
        level=criteria.level,
    )

    return items


def search_vacancies_by_criteria(
    criteria: VacancySearchCriteria,
) -> VacancySearchResponse:
    items = _search_and_filter_vacancies(criteria)

    return VacancySearchResponse(
        items=items[: criteria.per_page],
        found=len(items),
        page=criteria.page,
        per_page=criteria.per_page,
    )


def search_and_save_vacancies(
    db: Session,
    criteria: VacancySearchCriteria,
) -> VacancySearchSavedResponse:
    items = _search_and_filter_vacancies(criteria)

    visible_items = items[: criteria.per_page]

    search_run = create_search_run(
        db=db,
        criteria=criteria,
        found_count=len(items),
    )

    search_run_id = cast(int, search_run.id)

    saved_vacancies = create_found_vacancies(
        db=db,
        search_run_id=search_run_id,
        vacancies=visible_items,
    )

    return VacancySearchSavedResponse(
            search_run=VacancySearchRunRead.model_validate(search_run),
            items=[
                FoundVacancyRead.model_validate(vacancy)
                for vacancy in saved_vacancies
            ],
            found=len(items),
            page=criteria.page,
            per_page=criteria.per_page,
        )
