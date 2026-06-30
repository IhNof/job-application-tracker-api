from urllib.parse import urlparse
from bs4 import BeautifulSoup
from app.vacancies.schemas import VacancySearchItem


def _extract_external_id(url: str) -> str:
    path = urlparse(url).path
    parts = path.strip("/").split("/")

    if "vacancy" in parts:
        index = parts.index("vacancy")
        if index + 1 < len(parts):
            return parts[index + 1]

    return url


def is_vacancy_href(href: str | None) -> bool:
    return href is not None and "/vacancy/" in href


def parse_hh_vacancies_html(html: str) -> list[VacancySearchItem]:
    soup = BeautifulSoup(html, "html.parser")

    vacancy_cards = soup.select(
        "div.vacancy-serp-item, "
        "article.vacancy-serp-item, "
        "div[data-qa='vacancy-serp__vacancy']"
    )

    vacancies: list[VacancySearchItem] = []

    for card in vacancy_cards:
        title_tag = (
            card.find("a", {"data-qa": "serp-item__title"})
            or card.find("a", href=is_vacancy_href)
        )

        if title_tag is None:
            continue

        title = title_tag.get_text(strip=True)
        href = title_tag.get("href", "")

        if not title or not href:
            continue

        if not isinstance(href, str):
            continue

        url = href if href.startswith("http") else f"https://hh.ru{href}"

        company_tag = card.find(
            "a",
            {"data-qa": "vacancy-serp__vacancy-employer"},
        )
        company = company_tag.get_text(strip=True) if company_tag else None

        location_tag = card.find(
            "div",
            {"data-qa": "vacancy-serp__vacancy-address"},
        )
        location = location_tag.get_text(strip=True) if location_tag else None

        vacancies.append(
            VacancySearchItem(
                external_id=_extract_external_id(url),
                source="hh",
                title=title,
                company=company,
                location=location,
                salary_min=None,
                salary_max=None,
                currency=None,
                url=url,
                published_at=None,
            )
        )

    return vacancies
