from pathlib import Path
from typing import Any, List

from langchain_core.tools import tool

from core.config import settings
from utils.json import pretty_json


SKILLS_DIR = Path(settings.SKILL_PATH).resolve()
_SKILL_INDEX: list[dict[str, Any]] | None = None

def _parse_skill_frontmatter(file_path: Path) -> dict[str, Any] | None:
    """
    Parse only the first frontmatter block from a skill markdown file.
    """
    try:
        text = file_path.read_text(encoding="utf-8")
    except OSError:
        return None

    lines = text.splitlines()
    if not lines or lines[0].strip() != "---":
        return None

    header_lines = []
    for line in lines[1:]:
        if line.strip() == "---":
            break
        header_lines.append(line)
    else:
        return None

    meta: dict[str, Any] = {"path": str(file_path), "raw_header": "\n".join(header_lines)}
    for line in header_lines:
        if ":" not in line:
            continue
        key, value = line.split(":", 1)
        meta[key.strip().lower()] = value.strip()
    return meta


def _get_skill_index() -> list[dict[str, Any]]:
    global _SKILL_INDEX
    if _SKILL_INDEX is not None:
        return _SKILL_INDEX

    skills: list[dict[str, Any]] = []
    if SKILLS_DIR.exists():
        for file_path in sorted(SKILLS_DIR.glob("*.md")):
            skill = _parse_skill_frontmatter(file_path)
            if skill:
                skills.append(skill)

    _SKILL_INDEX = skills
    return skills


@tool
def search_skills(keywords: List[str]) -> str:
    """
    Search skill markdown frontmatter in src/skills using multiple keywords.
    """
    normalized_keywords = [kw.strip().lower() for kw in keywords if kw and kw.strip()]
    if not normalized_keywords:
        return "No keywords provided."

    matches = []
    for skill in _get_skill_index():
        searchable_text = " ".join(
            str(skill.get(field, ""))
            for field in ("id", "name", "description", "version", "raw_header")
        ).lower()

        hit_count = sum(1 for kw in normalized_keywords if kw in searchable_text)
        if hit_count == 0:
            continue

        matches.append(
            {
                "score": hit_count,
                "id": skill.get("id"),
                "name": skill.get("name"),
                "description": skill.get("description"),
                "version": skill.get("version"),
                "path": skill.get("path"),
                "raw_header": skill.get("raw_header"),
            }
        )

    matches.sort(key=lambda item: (-item["score"], str(item.get("name", "")).lower()))
    return pretty_json(matches) if matches else "No matching skills found."
