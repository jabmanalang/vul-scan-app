from pydantic import BaseModel
from datetime import datetime


class AssetBase(BaseModel):
    name: str
    description: str


class AssetIn(AssetBase):
    pass


class AssetOut(AssetBase):
    id: int
    created: datetime
