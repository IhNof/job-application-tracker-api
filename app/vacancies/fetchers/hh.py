import logging
from pathlib import Path
from urllib.parse import urlencode
from fastapi import HTTPException, status
from app.config import settings
from app.vacancies.schemas import VacancySearchCriteria


logger = logging.getLogger(__name__)


class HHHtmlFetcher:
    def fetch_html(self, criteria: VacancySearchCriteria) -> str:
        search_url = self._build_search_url(criteria)
        html = self._get_html(search_url)

        if not isinstance(html, str) or not html.strip():
            raise HTTPException(
                status_code=status.HTTP_502_BAD_GATEWAY,
                detail={
                    "message": "HTML provider returned empty response",
                    "source": "hh",
                },
            )

        return html.strip()

    def _get_html(self, search_url: str) -> str:
        logger.info("HH search URL was built: %s", search_url)

        if settings.html_provider_mode == "fixture":
            return self._get_html_from_fixture()

        raise HTTPException(
            status_code=status.HTTP_501_NOT_IMPLEMENTED,
            detail={
                "message": (
                    "HTML provider is not configured in the public version. "
                    "Use fixture mode or /vacancies/parse-html."
                ),
                "source": "hh",
            },
        )

    def _get_html_from_fixture(self) -> str:
        path = Path(settings.hh_fixture_path)

        if not path.exists():
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail={
                    "message": (
                        f"Fixture file not found: {settings.hh_fixture_path}"
                    ),
                    "source": "hh",
                },
            )

        return path.read_text(encoding="utf-8")

    def _build_search_url(self, criteria: VacancySearchCriteria) -> str:
        base_url = "https://hh.ru/search/vacancy"

        params: dict[str, str | int] = {
            "page": criteria.page,
        }

        if criteria.text:
            params["text"] = criteria.text

        if criteria.area is not None:
            params["area"] = criteria.area

        if criteria.salary_from is not None and criteria.salary_from > 0:
            params["salary"] = criteria.salary_from

        if criteria.only_with_salary:
            params["only_with_salary"] = "true"

        if criteria.experience:
            params["experience"] = criteria.experience

        return f"{base_url}?{urlencode(params)}"
