from pydantic import BaseModel

from src.enums import Status


class SeverityCount(BaseModel):
    critical: int
    high: int
    medium: int
    low: int
    information: int


class ScanBase(BaseModel):
    requested_by: int
    name: str
    scanners: list[str]
    assets_scanned: list[int]


class ScanIn(ScanBase):
    pass


class ScanOut(ScanBase):
    id: int
    status: Status
    severity_counts: SeverityCount


class ScanPatch(BaseModel):
    status: Status
    severity_counts: SeverityCount
