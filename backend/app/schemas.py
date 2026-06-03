from pydantic import BaseModel, Field
from typing import List, Literal
from datetime import datetime

LanguageCode = Literal["en", "he"]


class Segment(BaseModel):

    id: str = Field(..., description="Unique identifier for the segment")
    source: str = Field(..., description="Source text to translate", min_length=1)
    target: str = Field(..., description="Translated target text", min_length=1)


class TranslationRequest(BaseModel):

    source_lang: LanguageCode = Field(..., description="Source language code")
    target_lang: LanguageCode = Field(..., description="Target language code")
    text: str = Field(..., description="Text to translate", min_length=1)
    filename: str | None = Field(None, description="Optional filename for context")


class TranslationResponse(BaseModel):

    source_lang: LanguageCode
    target_lang: LanguageCode
    segments: List[Segment]
    timestamp: datetime = Field(
        default_factory=datetime.utcnow,
        description="Timestamp when the translation was processed"
    )