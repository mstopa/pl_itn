from pydantic import BaseModel
from enum import Enum


class FstType(Enum):
    TAGGER = "tagger"
    VERBALIZER = "verbalizer"


class FstDetails(BaseModel):
    name: str
    type: FstType
    description: str | None = None


class NormalizeRequest(BaseModel):
    text: str
    tagger: str | None = None
    verbalizer: str | None = None
