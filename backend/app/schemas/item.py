"""Item 请求/响应模型"""

from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field


class ItemCreate(BaseModel):
    model_config = ConfigDict(extra="forbid", strict=True)

    title: str = Field(..., min_length=1, max_length=200)
    description: str | None = Field(default=None, max_length=2000)


class ItemRead(BaseModel):
    model_config = ConfigDict(from_attributes=True, strict=True)

    id: int
    title: str
    description: str | None
    created_at: datetime
