from pydantic import BaseModel
from typing import Literal


class EntityIntent(BaseModel):
    index: int
    intent: Literal["prefer", "exclude", "reference", "neutral"]


class IntentOutput(BaseModel):
    results: list[EntityIntent]
    excluded_genres: list[str]