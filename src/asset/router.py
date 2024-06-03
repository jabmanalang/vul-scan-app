import logging
from typing import Annotated

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from src.asset.schemas import AssetIn, AssetOut
from src.database import session, crud

logger = logging.getLogger("vul")

router = APIRouter(
    prefix="/assets"
)


@router.post("", response_model=AssetOut)
def post_asset(
        db: Annotated[Session, Depends(session.get_db)],
        post_asset_request: AssetIn
):
    asset = crud.create_asset(db=db, asset_schema=post_asset_request)
    return asset


@router.get("/{asset_id}", response_model=AssetOut)
def get_asset(
        db: Annotated[Session, Depends(session.get_db)],
        asset_id: int
):
    asset = crud.read_asset(db, asset_id=asset_id)
    return asset
