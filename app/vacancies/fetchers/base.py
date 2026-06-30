from typing import Protocol

from app.vacancies.schemas import VacancySearchCriteria


class VacancyHtmlFetcher(Protocol):
    def fetch_html(self, criteria: VacancySearchCriteria) -> str:
        ...
