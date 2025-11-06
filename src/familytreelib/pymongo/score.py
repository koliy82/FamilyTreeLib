from pydantic import BaseModel, ConfigDict


class Score(BaseModel):
    mantissa: int
    exponent: int
    model_config = ConfigDict(
        arbitrary_types_allowed=True,
        json_schema_extra={
            "example": {
                "mantissa": 0,
                "exponent":0,
            }
        },
    )