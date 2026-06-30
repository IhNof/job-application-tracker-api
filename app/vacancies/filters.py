import re

from app.vacancies.schemas import VacancyLevel, VacancySearchItem


LEVEL_MARKERS: dict[VacancyLevel, tuple[str, ...]] = {
    "intern": (
        "intern",
        "internship",
        "trainee",
        "стажер",
        "стажёр",
        "практикант",
    ),
    "junior": (
        "junior",
        "джуниор",
        "джун",
        "младший",
    ),
    "middle": (
        "middle",
        "middle+",
        "mid",
        "мидл",
    ),
    "senior": (
        "senior",
        "senior+",
        "сеньор",
        "старший",
        "ведущий",
    ),
    "lead": (
        "lead",
        "tech lead",
        "team lead",
        "тимлид",
        "техлид",
        "лид",
        "head",
        "principal",
        "staff",
        "architect",
        "руководитель",
        "архитектор",
    ),
}


def _normalize_text(text: str) -> str:
    return text.lower().replace("ё", "е")


def _make_search_text(vacancy: VacancySearchItem) -> str:
    parts = [
        vacancy.title,
        vacancy.company or "",
        vacancy.location or "",
    ]

    return _normalize_text(" ".join(parts))


def _contains_marker(text: str, marker: str) -> bool:
    marker = _normalize_text(marker)

    if " " in marker:
        return marker in text

    pattern = rf"(?<![a-zа-я0-9]){re.escape(marker)}(?![a-zа-я0-9])"

    return re.search(pattern, text, re.IGNORECASE) is not None


def _contains_any_marker(text: str, markers: tuple[str, ...]) -> bool:
    return any(
        _contains_marker(text, marker)
        for marker in markers
    )


def filter_by_level(
    vacancies: list[VacancySearchItem],
    level: VacancyLevel | None,
) -> list[VacancySearchItem]:
    if level is None:
        return vacancies

    target_markers = LEVEL_MARKERS[level]

    other_markers: list[str] = []

    for current_level, markers in LEVEL_MARKERS.items():
        if current_level != level:
            other_markers.extend(markers)

    filtered: list[VacancySearchItem] = []

    for vacancy in vacancies:
        text = _make_search_text(vacancy)

        has_target_level = _contains_any_marker(
            text=text,
            markers=target_markers,
        )

        has_other_level = _contains_any_marker(
            text=text,
            markers=tuple(other_markers),
        )

        if not has_target_level:
            continue

        if has_other_level:
            continue

        filtered.append(vacancy)

    return filtered
