#!/usr/bin/env python3
"""Validate ElevenLabs text-to-speech model/language compatibility.

The TTS endpoint can ignore an unsupported ``language_code`` instead of
rejecting the request, so callers must run this check before sending billable
text. Live ``GET /v1/models`` metadata is authoritative when available. The
bundled table is a fail-safe snapshot of the official ElevenLabs model table for
the maintained models and lets known combinations be checked when model-list
access is unavailable.
"""

from __future__ import annotations

import argparse
import json
import os
import re
import sys
import urllib.request


MODELS_URL = "https://api.elevenlabs.io/v1/models"
MODEL_DOCS_URL = "https://elevenlabs.io/docs/overview/models"

MULTILINGUAL_V2_LANGUAGES = frozenset(
    {
        "ar",
        "bg",
        "cs",
        "da",
        "de",
        "el",
        "en",
        "es",
        "fi",
        "fil",
        "fr",
        "hi",
        "hr",
        "id",
        "it",
        "ja",
        "ko",
        "ms",
        "nl",
        "pl",
        "pt",
        "ro",
        "ru",
        "sk",
        "sv",
        "ta",
        "tr",
        "uk",
        "zh",
    }
)

FLASH_V2_5_LANGUAGES = MULTILINGUAL_V2_LANGUAGES | {"hu", "no", "vi"}

V3_LANGUAGES = frozenset(
    {
        "af",
        "ar",
        "as",
        "az",
        "be",
        "bg",
        "bn",
        "bs",
        "ca",
        "ceb",
        "cs",
        "cy",
        "da",
        "de",
        "el",
        "en",
        "es",
        "et",
        "fa",
        "fi",
        "fil",
        "fr",
        "ga",
        "gl",
        "gu",
        "ha",
        "he",
        "hi",
        "hr",
        "hu",
        "hy",
        "id",
        "is",
        "it",
        "ja",
        "jv",
        "ka",
        "kk",
        "kn",
        "ko",
        "ky",
        "lb",
        "ln",
        "lt",
        "lv",
        "mk",
        "ml",
        "mr",
        "ms",
        "ne",
        "nl",
        "no",
        "ny",
        "pa",
        "pl",
        "ps",
        "pt",
        "ro",
        "ru",
        "sd",
        "sk",
        "sl",
        "so",
        "sr",
        "sv",
        "sw",
        "ta",
        "te",
        "th",
        "tr",
        "uk",
        "ur",
        "vi",
        "zh",
    }
)

DOCUMENTED_MODEL_LANGUAGES = {
    "eleven_multilingual_v2": MULTILINGUAL_V2_LANGUAGES,
    "eleven_flash_v2_5": FLASH_V2_5_LANGUAGES,
    "eleven_turbo_v2_5": FLASH_V2_5_LANGUAGES,
    "eleven_flash_v2": frozenset({"en"}),
    "eleven_turbo_v2": frozenset({"en"}),
    "eleven_v3": V3_LANGUAGES,
}

# ElevenLabs documents language-code enforcement for the 2.5 Flash/Turbo
# models. Multilingual v2 explicitly does not support the request parameter.
LANGUAGE_CODE_MODELS = frozenset(
    {"eleven_flash_v2_5", "eleven_turbo_v2_5"}
)

ISO_639_3_TO_PRIMARY = {
    "afr": "af",
    "ara": "ar",
    "asm": "as",
    "aze": "az",
    "bel": "be",
    "ben": "bn",
    "bos": "bs",
    "bul": "bg",
    "cat": "ca",
    "ces": "cs",
    "cmn": "zh",
    "cym": "cy",
    "dan": "da",
    "deu": "de",
    "ell": "el",
    "eng": "en",
    "est": "et",
    "fas": "fa",
    "fin": "fi",
    "fra": "fr",
    "gle": "ga",
    "glg": "gl",
    "guj": "gu",
    "hau": "ha",
    "heb": "he",
    "hin": "hi",
    "hrv": "hr",
    "hun": "hu",
    "hye": "hy",
    "ind": "id",
    "isl": "is",
    "ita": "it",
    "jav": "jv",
    "jpn": "ja",
    "kan": "kn",
    "kat": "ka",
    "kaz": "kk",
    "kir": "ky",
    "kor": "ko",
    "lav": "lv",
    "lin": "ln",
    "lit": "lt",
    "ltz": "lb",
    "mal": "ml",
    "mar": "mr",
    "mkd": "mk",
    "msa": "ms",
    "nep": "ne",
    "nld": "nl",
    "nor": "no",
    "nya": "ny",
    "pan": "pa",
    "pol": "pl",
    "por": "pt",
    "pus": "ps",
    "ron": "ro",
    "rus": "ru",
    "sin": "si",
    "slk": "sk",
    "slv": "sl",
    "snd": "sd",
    "som": "so",
    "spa": "es",
    "srp": "sr",
    "swa": "sw",
    "swe": "sv",
    "tam": "ta",
    "tel": "te",
    "tha": "th",
    "tur": "tr",
    "ukr": "uk",
    "urd": "ur",
    "vie": "vi",
}


def primary_language_code(language_tag: str | None) -> str:
    raw = str(language_tag or "en").strip().replace("_", "-")
    primary = raw.split("-", 1)[0].lower()
    if not re.fullmatch(r"[a-z]{2,3}", primary):
        raise ValueError(f"Invalid BCP 47 language tag: {language_tag!r}")
    return ISO_639_3_TO_PRIMARY.get(primary, primary)


def documented_languages(model_id: str) -> frozenset[str] | None:
    return DOCUMENTED_MODEL_LANGUAGES.get(str(model_id or "").strip())


def default_model_for_language(language_tag: str | None) -> str:
    language = primary_language_code(language_tag)
    if language in MULTILINGUAL_V2_LANGUAGES:
        return "eleven_multilingual_v2"
    if language in FLASH_V2_5_LANGUAGES:
        return "eleven_flash_v2_5"
    raise ValueError(
        f"No verified default ElevenLabs model for language {language!r}. "
        "Set narration.model_id to a model that explicitly supports it; "
        "the live preflight will verify the combination before synthesis."
    )


def fetch_model_catalog(api_key: str, timeout: int = 30) -> list[dict]:
    req = urllib.request.Request(
        MODELS_URL,
        headers={
            "xi-api-key": api_key,
            "accept": "application/json",
            "user-agent": "AcademyWizard/ElevenLabs-model-preflight",
        },
    )
    with urllib.request.urlopen(req, timeout=timeout) as response:
        payload = json.loads(response.read().decode("utf-8"))
    if not isinstance(payload, list):
        raise RuntimeError("ElevenLabs model catalog returned a non-list response.")
    return payload


def _catalog_model(catalog: list[dict], model_id: str) -> dict | None:
    for model in catalog:
        if str(model.get("model_id") or "") == model_id:
            return model
    return None


def _catalog_languages(model: dict) -> frozenset[str]:
    values: set[str] = set()
    for item in model.get("languages") or []:
        if not isinstance(item, dict):
            continue
        language_id = str(item.get("language_id") or "").strip()
        if language_id:
            values.add(primary_language_code(language_id))
    return frozenset(values)


def validate_model_language(
    model_id: str,
    language_tag: str | None,
    *,
    api_key: str | None = None,
    catalog: list[dict] | None = None,
) -> str:
    """Return the validation source or raise before any billable TTS request."""

    model_id = str(model_id or "").strip()
    if not model_id:
        raise ValueError("An ElevenLabs model_id is required.")
    language = primary_language_code(language_tag)

    live_error: Exception | None = None
    live_catalog = catalog
    if live_catalog is None and api_key:
        try:
            live_catalog = fetch_model_catalog(api_key)
        except Exception as error:
            live_error = error

    if live_catalog is not None:
        model = _catalog_model(live_catalog, model_id)
        if model is None:
            raise RuntimeError(
                f"ElevenLabs model compatibility check blocked synthesis: "
                f"{model_id!r} is not present in the live model catalog."
            )
        if not bool(model.get("can_do_text_to_speech")):
            raise RuntimeError(
                f"ElevenLabs model compatibility check blocked synthesis: "
                f"{model_id!r} is not a text-to-speech model."
            )
        supported = _catalog_languages(model)
        source = "ElevenLabs live /v1/models catalog"
        if not supported:
            raise RuntimeError(
                f"ElevenLabs model compatibility check blocked synthesis: "
                f"the live catalog reports no languages for {model_id!r}."
            )
    else:
        supported = documented_languages(model_id)
        if supported is None:
            detail = f" ({live_error})" if live_error else ""
            raise RuntimeError(
                f"ElevenLabs model compatibility check blocked synthesis: "
                f"support for {model_id!r} could not be verified{detail}. "
                f"Review {MODEL_DOCS_URL} or allow access to {MODELS_URL}."
            )
        source = "bundled ElevenLabs documentation snapshot"
        if live_error:
            source += f" (live catalog unavailable: {type(live_error).__name__})"

    if language not in supported:
        alternatives = sorted(
            candidate
            for candidate, languages in DOCUMENTED_MODEL_LANGUAGES.items()
            if language in languages
        )
        suggestion = (
            f" Verified alternatives: {', '.join(alternatives)}."
            if alternatives
            else " No bundled model supports this language; select a current model "
            f"from {MODEL_DOCS_URL}."
        )
        raise RuntimeError(
            f"ElevenLabs model compatibility check blocked synthesis before any "
            f"billable request: {model_id!r} does not support language "
            f"{language!r}.{suggestion}"
        )

    return source


def should_send_language_code(model_id: str) -> bool:
    return model_id in LANGUAGE_CODE_MODELS


def main() -> None:
    parser = argparse.ArgumentParser(
        description=(
            "Verify an ElevenLabs model/language combination before paid TTS."
        )
    )
    parser.add_argument("language_tag", help="BCP 47 tag, for example vi-VN")
    parser.add_argument("model_id", help="ElevenLabs model ID")
    parser.add_argument(
        "--offline",
        action="store_true",
        help="use only the bundled official-documentation snapshot",
    )
    args = parser.parse_args()
    api_key = None if args.offline else os.getenv("ELEVENLABS_API_KEY")
    try:
        source = validate_model_language(
            args.model_id,
            args.language_tag,
            api_key=api_key,
        )
    except (RuntimeError, ValueError) as error:
        sys.exit(str(error))
    print(
        f"compatible: {args.model_id} supports "
        f"{primary_language_code(args.language_tag)} ({source})"
    )


if __name__ == "__main__":
    main()
