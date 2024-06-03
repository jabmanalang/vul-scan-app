from typing import Annotated

from fastapi import APIRouter, Depends, BackgroundTasks
from sqlalchemy.orm import Session

from src.database import session, crud
from src.scan.schemas import ScanIn, ScanOut, ScanPatch
from src.scan.utilities import map_to_schema, call_worker_app

router = APIRouter(
    prefix="/scans"
)


@router.post("")
def post_scan(
        db: Annotated[Session, Depends(session.get_db)],
        background_tasks: BackgroundTasks,
        post_scan_request: ScanIn
):
    # TODO: Validate if user and assets are existing
    scan = crud.create_scan(db, scan_schema=post_scan_request)
    scan_out = map_to_schema(scan=scan)
    background_tasks.add_task(call_worker_app)
    return scan_out


@router.get("/{scan_id}")
def get_scan(
        db: Annotated[Session, Depends(session.get_db)],
        scan_id: int
):
    scan = crud.read_scan(db, scan_id=scan_id)
    scan_out = map_to_schema(scan=scan)
    return scan_out


@router.patch("/{scan_id}", response_model=ScanOut)
def patch_scan(
        db: Annotated[Session, Depends(session.get_db)],
        scan_id: int,
        patch_scan_request: ScanPatch
):
    scan = crud.update_scan(db, scan_id=scan_id, patch_scan_schema=patch_scan_request)
    scan_out = map_to_schema(scan=scan)
    return scan_out
