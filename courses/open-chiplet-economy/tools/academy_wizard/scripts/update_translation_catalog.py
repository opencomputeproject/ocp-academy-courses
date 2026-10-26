#!/usr/bin/env python3
"""Refresh the root README Translations table from locale course sources."""

from __future__ import annotations

import argparse
import json
import re
import sys
from dataclasses import dataclass
from pathlib import Path


START_MARKER = "<!-- translations-table:start -->"
END_MARKER = "<!-- translations-table:end -->"
TRANSLATED_LEARNING_URL = (
    "https://academy.opencompute.org/pages/25/ocp-academy-translated-learning"
)

LOCALE_LABEL_OVERRIDES = {
    "es-419": "Spanish (LATAM)",
    "pt-BR": "Portuguese (Brazil)",
    "vi-VN": "Vietnamese",
    "zh-CN": "Chinese (Simplified)",
    "zh-HK": "Chinese (Traditional, Hong Kong)",
    "zh-SG": "Chinese (Simplified)",
    "zh-TW": "Chinese (Traditional)",
}

SERIES_TITLE_OVERRIDES = {
    "intro-to-ocp": "Intro to OCP",
    "open-rack-v3": "Open Rack",
    "optics": "Optics",
}

SLUG_ACRONYMS = {
    "ai": "AI",
    "ocp": "OCP",
}

SLUG_LOWERCASE_WORDS = {"and", "for", "in", "of", "the", "to"}


@dataclass(frozen=True)
class Translation:
    course_path: Path
    course_title: str
    language_label: str
    locale: str
    locale_path: Path


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Refresh the root README Translations table from locale course.json files."
    )
    parser.add_argument(
        "--repo-root",
        type=Path,
        help="Repository root. Defaults to the nearest parent containing README.md and courses/.",
    )
    parser.add_argument(
        "--check",
        action="store_true",
        help="Exit non-zero when the README table is stale instead of updating it.",
    )
    return parser.parse_args()


def find_repo_root(start: Path) -> Path:
    current = start.resolve()
    for candidate in (current, *current.parents):
        if (candidate / "README.md").is_file() and (candidate / "courses").is_dir():
            return candidate
    raise SystemExit("Could not find a repository root containing README.md and courses/.")


def load_json(path: Path) -> dict:
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        raise SystemExit(f"Could not read {path}: {exc}") from exc


def course_title(course_root: Path, canonical: dict) -> str:
    title = ""
    readme = course_root / "README.md"
    if readme.is_file():
        for line in readme.read_text(encoding="utf-8").splitlines():
            if line.startswith("# "):
                title = line[2:].strip()
                break
    if not title:
        title = str(canonical.get("course_title") or course_root.name)
    return title


def repository_layout_series_folders(readme: str) -> set[str]:
    match = re.search(
        r"^## Repository layout\s*$\n(.*?)(?=^##\s|\Z)",
        readme,
        flags=re.MULTILINE | re.DOTALL,
    )
    if not match:
        raise SystemExit("README.md must contain a Repository layout section.")
    child_counts: dict[str, int] = {}
    current_folder: str | None = None
    for line in match.group(1).splitlines():
        top_level = re.fullmatch(r"  ([A-Za-z0-9][A-Za-z0-9._-]*)/\s*", line)
        if top_level:
            current_folder = top_level.group(1)
            child_counts.setdefault(current_folder, 0)
            continue
        if re.fullmatch(r"    [^/\s][^/]*/\s*", line) and current_folder:
            child_counts[current_folder] += 1
    return {folder for folder, count in child_counts.items() if count > 1}


def title_from_slug(slug: str) -> str:
    if slug in SERIES_TITLE_OVERRIDES:
        return SERIES_TITLE_OVERRIDES[slug]
    words = []
    for index, token in enumerate(slug.split("-")):
        lower = token.casefold()
        if lower in SLUG_ACRONYMS:
            words.append(SLUG_ACRONYMS[lower])
        elif index and lower in SLUG_LOWERCASE_WORDS:
            words.append(lower)
        else:
            words.append(token.capitalize())
    return " ".join(words)


def series_titles(repo_root: Path, translations: list[Translation]) -> dict[str, str]:
    readme = (repo_root / "README.md").read_text(encoding="utf-8")
    layout_series = repository_layout_series_folders(readme)
    represented_folders = set()
    for item in translations:
        parts = item.course_path.parts
        if len(parts) >= 3 and parts[0] == "courses":
            represented_folders.add(parts[1])
    return {
        folder: title_from_slug(folder)
        for folder in represented_folders
        if folder in layout_series
    }


def add_series_titles(
    repo_root: Path, translations: list[Translation]
) -> list[Translation]:
    prefixes = series_titles(repo_root, translations)
    result = []
    for item in translations:
        parts = item.course_path.parts
        series = prefixes.get(parts[1]) if len(parts) >= 3 else None
        title = item.course_title
        if series and not title.casefold().startswith(f"{series}: ".casefold()):
            title = f"{series}: {title}"
        result.append(
            Translation(
                course_path=item.course_path,
                course_title=title,
                language_label=item.language_label,
                locale=item.locale,
                locale_path=item.locale_path,
            )
        )
    return result


def language_label(locale: str, localized: dict) -> str:
    if locale in LOCALE_LABEL_OVERRIDES:
        return LOCALE_LABEL_OVERRIDES[locale]
    label = str(localized.get("metadata_language_name") or locale).strip()
    return re.sub(r"\s+-\s+LATAM$", " (LATAM)", label, flags=re.IGNORECASE)


def escape_cell(value: str) -> str:
    return value.replace("|", "\\|")


def collect_translations(repo_root: Path) -> list[Translation]:
    translations: list[Translation] = []
    for locale_json in sorted((repo_root / "courses").glob("**/locales/*/course.json")):
        locale_root = locale_json.parent
        locale = locale_root.name
        localized = load_json(locale_json)
        language = str(localized.get("language") or locale)
        if language.lower() == "en" or language.lower().startswith("en-"):
            continue

        course_root = locale_root.parent.parent
        canonical_json = course_root / "course.json"
        if not canonical_json.is_file():
            raise SystemExit(f"Missing canonical course.json for {locale_json}")
        canonical = load_json(canonical_json)

        translations.append(
            Translation(
                course_path=course_root.relative_to(repo_root),
                course_title=course_title(course_root, canonical),
                language_label=language_label(locale, localized),
                locale=locale,
                locale_path=locale_root.relative_to(repo_root),
            )
        )
    return add_series_titles(repo_root, translations)


def render_table(translations: list[Translation]) -> str:
    labels = sorted({item.language_label for item in translations}, key=str.casefold)
    courses: dict[tuple[str, str], dict[str, list[Translation]]] = {}
    for item in translations:
        key = (item.course_title, item.course_path.as_posix())
        courses.setdefault(key, {}).setdefault(item.language_label, []).append(item)

    header = "| Course" + " |".join(["", *(f" {escape_cell(label)}" for label in labels)]) + " |"
    divider = "|---|" + "---|" * len(labels)
    rows = [header, divider]
    for (title, course_path), editions in sorted(
        courses.items(), key=lambda pair: pair[0][0].casefold()
    ):
        cells = [f"[{escape_cell(title)}]({course_path}/)"]
        for label in labels:
            variants = sorted(editions.get(label, []), key=lambda edition: edition.locale)
            cells.append(
                ", ".join(
                    f"[`{edition.locale}`]({edition.locale_path}/)" for edition in variants
                )
                if variants
                else "—"
            )
        rows.append("| " + " | ".join(cells) + " |")
    return "\n".join(rows)


def replace_table(readme: str, table: str) -> str:
    if readme.count(START_MARKER) != 1 or readme.count(END_MARKER) != 1:
        raise SystemExit(
            f"README.md must contain exactly one {START_MARKER} and one {END_MARKER}."
        )
    if readme.index(START_MARKER) > readme.index(END_MARKER):
        raise SystemExit(f"{START_MARKER} must appear before {END_MARKER}.")
    if TRANSLATED_LEARNING_URL not in readme.split(START_MARKER, 1)[0]:
        raise SystemExit(
            "README.md must link to the OCP Academy Translated Learning page above "
            "the Translations table."
        )
    before, remainder = readme.split(START_MARKER, 1)
    _, after = remainder.split(END_MARKER, 1)
    return f"{before}{START_MARKER}\n{table}\n{END_MARKER}{after}"


def main() -> int:
    args = parse_args()
    repo_root = args.repo_root.resolve() if args.repo_root else find_repo_root(Path.cwd())
    readme_path = repo_root / "README.md"
    original = readme_path.read_text(encoding="utf-8")
    updated = replace_table(original, render_table(collect_translations(repo_root)))

    if updated == original:
        print("README Translations table is current.")
        return 0
    if args.check:
        print(
            "README Translations table is stale. Run update_translation_catalog.py.",
            file=sys.stderr,
        )
        return 1

    readme_path.write_text(updated, encoding="utf-8")
    print(f"Updated {readme_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
