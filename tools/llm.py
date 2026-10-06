import json
import os
from functools import lru_cache
from typing import TypeVar

import anthropic
import openai
from dotenv import load_dotenv
from pydantic import BaseModel, ValidationError

load_dotenv()

T = TypeVar("T", bound=BaseModel)

DEFAULT_MODELS = {"openai": "gpt-4.1-mini", "anthropic": "claude-sonnet-5-5"}
API_ERRORS = (openai.APIStatusError, anthropic.APIStatusError)


def _anthropic_key() -> str | None:
    return os.getenv("ANTHROPIC_API_KEY") or os.getenv("CLAUDE_API_KEY")


def provider() -> str:
    explicit = os.getenv("LLM_PROVIDER")
    if explicit:
        return explicit.lower()
    return "openai" if os.getenv("OPENAI_API_KEY") or not _anthropic_key() else "anthropic"


def current_model() -> str:
    name = provider()
    return os.getenv("LLM_MODEL") or os.getenv(f"{name.upper()}_MODEL") or DEFAULT_MODELS[name]


@lru_cache(maxsize=1)
def _openai_client() -> openai.OpenAI:
    # Reads OPENAI_API_KEY (and optionally OPENAI_BASE_URL) from the environment.
    return openai.OpenAI(max_retries=3)


@lru_cache(maxsize=1)
def _anthropic_client() -> anthropic.Anthropic:
    return anthropic.Anthropic(api_key=_anthropic_key(), max_retries=3)


def _complete(system: str, messages: list[dict], json_mode: bool = False) -> str:
    if provider() == "anthropic":
        response = _anthropic_client().messages.create(
            model=current_model(),
            system=system,
            messages=messages,
            max_tokens=8192,
        )
        return "".join(block.text for block in response.content if block.type == "text")

    extra = {"response_format": {"type": "json_object"}} if json_mode else {}
    response = _openai_client().chat.completions.create(
        model=current_model(),
        messages=[{"role": "system", "content": system}, *messages],
        **extra,
    )
    return response.choices[0].message.content or ""


def _extract_json(text: str) -> str:
    """Drop any prose or ``` fences around the outermost JSON object."""
    start, end = text.find("{"), text.rfind("}")
    return text[start : end + 1] if start != -1 and end > start else text


def chat_text(system: str, user: str) -> str:
    return _complete(system, [{"role": "user", "content": user}])


def chat_json(system: str, user: str, schema: type[T], max_repairs: int = 2) -> T:
    """Ask for a JSON object matching `schema`; feed validation errors back to the model."""
    system = (
        f"{system}\n\nRespond with only a single JSON object (no prose, no code fences) "
        f"that conforms to this JSON schema:\n{json.dumps(schema.model_json_schema())}"
    )
    messages = [{"role": "user", "content": user}]
    for _ in range(max_repairs + 1):
        content = _complete(system, messages, json_mode=True)
        try:
            return schema.model_validate_json(_extract_json(content))
        except ValidationError as err:
            messages.append({"role": "assistant", "content": content})
            messages.append(
                {
                    "role": "user",
                    "content": f"That JSON was invalid:\n{err}\nReturn the corrected JSON object only.",
                }
            )
    raise RuntimeError(f"Model did not return valid {schema.__name__} JSON after {max_repairs} repairs")
