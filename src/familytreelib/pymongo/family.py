from datetime import datetime
from typing import Optional, Annotated

from bson import ObjectId
from pydantic import BaseModel, Field, ConfigDict, BeforeValidator


class Family(BaseModel):

    id: Annotated[str, BeforeValidator(str)] = Field(..., alias="_id")
    first_user_id: int
    second_user_id: int
    chat_id: Optional[int] = None
    create_date: datetime
    baby_user_id: Optional[int] = None
    baby_create_date: Optional[datetime] = None
    score: int
    last_casino_play: datetime
    last_grow_kid: datetime
    last_hamster_update: datetime
    tap_count: int
    model_config = ConfigDict(
        arbitrary_types_allowed=True,
        json_encoders={ObjectId: str},
        json_schema_extra={
            "example": {
                "id": "0",
                "first_user_id": 0,
                "second_user_id": 0,
                "chat_id": 0,
                "create_date": "1970-01-01T00:00:00",
                "baby_user_id": 0,
                "baby_create_date": "1970-01-01T00:00:00",
                "score": 0,
                "last_casino_play": "1970-01-01T00:00:00",
                "last_grow_kid": "1970-01-01T00:00:00",
                "last_hamster_update": "1970-01-01T00:00:00",
                "tap_count": 0,
            }
        },
    )

    @classmethod
    def from_mongo(cls, data: dict):
        if data is None:
            return None
        return cls(**data)

    @classmethod
    def partner_id(cls, root_id: int) -> int:
        if cls.first_user_id == root_id:
            return cls.second_user_id
        return cls.first_user_id
