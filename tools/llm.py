import json
import os
from functools import lru_cache
from typing import TypeVar

from dotenv import load_dotenv
from openai import OpenAI
from pydantic import BaseModel, ValidationError

load_dotenv()

T = TypeVar("T", bound=BaseModel)


def _model(model: str | None) -> str:
    return model or os.getenv("OPENAI_MODEL") or "gpt-4.1-mini"


@lru_cache(maxsize=1)
def get_client() -> OpenAI:
    # Reads OPENAI_API_KEY (and optionally OPENAI_BASE_URL) from the environment.
    return OpenAI(max_retries=3)


def chat_text(system: str, user: str, model: str | None = None) -> str:
    response = get_client().chat.completions.create(
        model=_model(model),
        messages=[
            {"role": "system", "content": system},
            {"role": "user", "content": user},
        ],
    )
    return response.choices[0].message.content or ""


def chat_json(
    system: str,
    user: str,
    schema: type[T],
    model: str | None = None,
    max_repairs: int = 2,
) -> T:
    """Ask for a JSON object matching `schema`; feed validation errors back to the model."""
    system = (
        f"{system}\n\nRespond with a single JSON object that conforms to this JSON schema:\n"
        f"{json.dumps(schema.model_json_schema())}"
    )
    messages = [
        {"role": "system", "content": system},
        {"role": "user", "content": user},
    ]
    for _ in range(max_repairs + 1):
        response = get_client().chat.completions.create(
            model=_model(model),
            messages=messages,
            response_format={"type": "json_object"},
        )
        content = response.choices[0].message.content or ""
        try:
            return schema.model_validate_json(content)
        except ValidationError as err:
            messages.append({"role": "assistant", "content": content})
            messages.append(
                {
                    "role": "user",
                    "content": f"That JSON was invalid:\n{err}\nReturn the corrected JSON object only.",
                }
            )
    raise RuntimeError(f"Model did not return valid {schema.__name__} JSON after {max_repairs} repairs")
