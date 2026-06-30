# Job Application Tracker API

REST API for tracking job applications, interview stages, vacancy search results and application statistics.

## Tech Stack

- Python
- FastAPI
- SQLite
- SQLAlchemy
- Pydantic
- Swagger / OpenAPI

## Features

### Applications

- Create job applications manually
- Get list of applications
- Get application by id
- Update application
- Delete application
- Filter applications by status, company and remote format
- Get summary statistics by application status

### Vacancy Search

- Search vacancies through a pluggable HTML provider
- Parse vacancy HTML into normalized vacancy items
- Filter vacancies by level:
  - intern
  - junior
  - middle
  - senior
  - lead
- Save vacancy search runs
- Store found vacancies in the database
- View previous search runs
- View vacancies found during a specific search run
- Create an application from a found vacancy
- Prevent duplicate applications for the same external vacancy

## Public HTML Provider

The public version of this project does not include provider-specific code for protected third-party websites.

Instead, the project uses a fixture-based HTML provider for demonstration purposes.

Fixture file:

```text
tests/fixtures/hh_search_sample.html
```

Example `.env` configuration:

```env
HTML_PROVIDER_MODE=fixture
HH_FIXTURE_PATH=tests/fixtures/hh_search_sample.html
```

This allows the vacancy search flow to work locally without external scraping infrastructure.

## Application Statuses

- draft
- applied
- screening
- interview
- offer
- rejected
- accepted

## Project Structure

```text
app/
  main.py
  database.py
  models.py
  schemas.py
  crud.py
  config.py

  applications/
    __init__.py
    router.py

  vacancies/
    __init__.py
    router.py
    schemas.py
    crud.py
    service.py
    filters.py

    fetchers/
      __init__.py
      base.py
      hh.py
      registry.py

    parsers/
      __init__.py
      hh.py
      registry.py

tests/
  fixtures/
    hh_search_sample.html
```