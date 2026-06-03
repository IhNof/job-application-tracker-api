# Job Application Tracker API

REST API for tracking job applications, interview stages and application statistics.

## Tech Stack

- Python
- FastAPI
- SQLite
- SQLAlchemy
- Pydantic
- Swagger / OpenAPI

## Features

- Create job applications
- Get list of applications
- Get application by id
- Update application
- Delete application
- Filter by status, company and remote format
- Get summary statistics by application status
- Interactive API documentation with Swagger

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