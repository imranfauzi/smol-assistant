import json

from tools import read_skill as read_skill_module
from tools import search_skills as search_skills_module
from tools.read_skill import read_skill
from tools.search_skills import _parse_skill_frontmatter, search_skills


def test_read_skill_reads_markdown_file_by_name(tmp_path, monkeypatch):
    skill_file = tmp_path / "python.md"
    skill_file.write_text("# Python Skill\n\nUse Python well.", encoding="utf-8")
    monkeypatch.setattr(read_skill_module, "SKILLS_DIR", tmp_path.resolve())

    result = read_skill.invoke({"skill_name": "python"})

    assert result == "# Python Skill\n\nUse Python well."


def test_read_skill_reads_markdown_file_by_frontmatter_id(tmp_path, monkeypatch):
    skill_file = tmp_path / "backend.md"
    skill_file.write_text(
        "---\nID: api-helper\nNAME: API Helper\n---\n\nBuild APIs.",
        encoding="utf-8",
    )
    monkeypatch.setattr(read_skill_module, "SKILLS_DIR", tmp_path.resolve())

    result = read_skill.invoke({"skill_name": "api-helper"})

    assert result == "---\nID: api-helper\nNAME: API Helper\n---\n\nBuild APIs."


def test_read_skill_rejects_empty_name():
    result = read_skill.invoke({"skill_name": "   "})

    assert result == "No skill name provided."


def test_read_skill_returns_not_found_for_missing_skill(tmp_path, monkeypatch):
    monkeypatch.setattr(read_skill_module, "SKILLS_DIR", tmp_path.resolve())

    result = read_skill.invoke({"skill_name": "missing"})

    assert result == "Skill not found: missing"


def test_parse_skill_frontmatter_returns_metadata(tmp_path):
    skill_file = tmp_path / "planner.md"
    skill_file.write_text(
        "---\n"
        "ID: planner\n"
        "NAME: Planner\n"
        "DESCRIPTION: Break work into steps\n"
        "VERSION: 1.0\n"
        "---\n"
        "\n"
        "# Body\n",
        encoding="utf-8",
    )

    result = _parse_skill_frontmatter(skill_file)

    assert result["id"] == "planner"
    assert result["name"] == "Planner"
    assert result["description"] == "Break work into steps"
    assert result["version"] == "1.0"
    assert result["path"] == str(skill_file)
    assert "ID: planner" in result["raw_header"]


def test_parse_skill_frontmatter_ignores_files_without_header(tmp_path):
    skill_file = tmp_path / "plain.md"
    skill_file.write_text("# Plain Skill", encoding="utf-8")

    result = _parse_skill_frontmatter(skill_file)

    assert result is None


def test_search_skills_returns_ranked_matches(tmp_path, monkeypatch):
    api_skill = tmp_path / "api.md"
    api_skill.write_text(
        "---\n"
        "ID: api-helper\n"
        "NAME: API Helper\n"
        "DESCRIPTION: Build HTTP APIs and clients\n"
        "VERSION: 1.0\n"
        "---\n",
        encoding="utf-8",
    )
    docs_skill = tmp_path / "docs.md"
    docs_skill.write_text(
        "---\n"
        "ID: docs\n"
        "NAME: Documentation\n"
        "DESCRIPTION: Write user guides\n"
        "VERSION: 1.0\n"
        "---\n",
        encoding="utf-8",
    )
    monkeypatch.setattr(search_skills_module, "SKILLS_DIR", tmp_path.resolve())
    monkeypatch.setattr(search_skills_module, "_SKILL_INDEX", None)

    result = search_skills.invoke({"keywords": ["api", "http"]})
    matches = json.loads(result)

    assert [match["id"] for match in matches] == ["api-helper"]
    assert matches[0]["score"] == 2
    assert matches[0]["name"] == "API Helper"
    assert matches[0]["path"] == str(api_skill)


def test_search_skills_rejects_empty_keywords():
    result = search_skills.invoke({"keywords": [" ", ""]})

    assert result == "No keywords provided."


def test_search_skills_returns_message_when_no_match(tmp_path, monkeypatch):
    skill_file = tmp_path / "docs.md"
    skill_file.write_text(
        "---\nID: docs\nNAME: Documentation\nDESCRIPTION: Write docs\n---\n",
        encoding="utf-8",
    )
    monkeypatch.setattr(search_skills_module, "SKILLS_DIR", tmp_path.resolve())
    monkeypatch.setattr(search_skills_module, "_SKILL_INDEX", None)

    result = search_skills.invoke({"keywords": ["database"]})

    assert result == "No matching skills found."
