from pydantic import BaseModel, Field


class WatchConfig(BaseModel):
    enable: bool = True
    json_: bool = Field(True, alias="json")
    split24: bool = False
    raw: int = 0
