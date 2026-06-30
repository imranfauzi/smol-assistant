from pathlib import Path

from langchain_core.tools import tool

from core.config import settings


SKILLS_DIR = Path(settings.SKILL_PATH).resolve()


@tool
def read_skill(skill_name: str) -> str:
    """
    Read the full markdown content of a skill file from src/skills.

    Accepts either a skill filename (with or without .md) or a skill id/name.
    """
    query = skill_name.strip()
    if not query:
        return "No skill name provided."

    candidate_names = []
    if query.lower().endswith(".md"):
        candidate_names.append(query)
    else:
        candidate_names.append(f"{query}.md")
        candidate_names.append(query)

    resolved_path = None
    for candidate in candidate_names:
        path = (SKILLS_DIR / candidate).resolve()
        if path.is_file() and path.is_relative_to(SKILLS_DIR):
            resolved_path = path
            break

    if resolved_path is None:
        for path in sorted(SKILLS_DIR.glob("*.md")):
            try:
                text = path.read_text(encoding="utf-8")
            except OSError:
                continue

            if f"ID: {query}" in text or f"NAME: {query}" in text:
                resolved_path = path
                break

    if resolved_path is None:
        return f"Skill not found: {skill_name}"

    try:
        return resolved_path.read_text(encoding="utf-8")
    except OSError as exc:
        return f"Failed to read skill file: {exc}"
