from sqlalchemy.orm import Session
from app import models
from app.vacancies.schemas import (
    VacancySearchCriteria,
    VacancySearchItem,
)


def create_search_run(
    db: Session,
    criteria: VacancySearchCriteria,
    found_count: int,
) -> models.VacancySearchRun:
    search_run = models.VacancySearchRun(
        source=criteria.source,
        query_text=criteria.text,
        company=criteria.company,
        area=criteria.area,
        salary_from=criteria.salary_from,
        only_with_salary=criteria.only_with_salary,
        experience=criteria.experience,
        level=criteria.level,
        found_count=found_count,
    )

    db.add(search_run)
    db.commit()
    db.refresh(search_run)

    return search_run


def create_found_vacancies(
    db: Session,
    search_run_id: int,
    vacancies: list[VacancySearchItem],
) -> list[models.FoundVacancy]:
    db_vacancies: list[models.FoundVacancy] = []

    for vacancy in vacancies:
        db_vacancy = models.FoundVacancy(
            search_run_id=search_run_id,
            external_id=vacancy.external_id,
            source=vacancy.source,
            title=vacancy.title,
            company=vacancy.company,
            location=vacancy.location,
            salary_min=vacancy.salary_min,
            salary_max=vacancy.salary_max,
            currency=vacancy.currency,
            salary_gross=vacancy.salary_gross,
            url=vacancy.url,
            published_at=vacancy.published_at,
        )

        db.add(db_vacancy)
        db_vacancies.append(db_vacancy)

    db.commit()

    for db_vacancy in db_vacancies:
        db.refresh(db_vacancy)

    return db_vacancies


def get_search_runs(db: Session) -> list[models.VacancySearchRun]:
    return (
        db.query(models.VacancySearchRun)
        .order_by(models.VacancySearchRun.created_at.desc())
        .all()
    )


def get_found_vacancies_by_search_run(
    db: Session,
    search_run_id: int,
) -> list[models.FoundVacancy]:
    return (
        db.query(models.FoundVacancy)
        .filter(models.FoundVacancy.search_run_id == search_run_id)
        .all()
    )
