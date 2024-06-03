import datetime
from typing import List, TYPE_CHECKING

from sqlalchemy import ForeignKey, DateTime
from sqlalchemy.sql import func
from sqlalchemy.orm import Mapped, mapped_column, relationship

if TYPE_CHECKING:
    from src.asset.models import Asset
    from src.user.models import User
from src.database.session import Base
from src.enums import Status


class SeverityCount(Base):
    __tablename__ = "severity_counts"

    id: Mapped[int] = mapped_column(primary_key=True)
    scan_id: Mapped[int] = mapped_column(ForeignKey("scans.id"), index=True)
    critical: Mapped[int]
    high: Mapped[int]
    medium: Mapped[int]
    low: Mapped[int]
    information: Mapped[int]


class Scanner(Base):
    __tablename__ = "scanners"

    id: Mapped[int] = mapped_column(primary_key=True)
    scan_id: Mapped[int] = mapped_column(ForeignKey("scans.id"), index=True)
    scanner_name: Mapped[str]


class Scan(Base):
    __tablename__ = "scans"

    id: Mapped[int] = mapped_column(primary_key=True)
    requested_by: Mapped["User"] = relationship("User")
    requested_by_user_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    name: Mapped[str]
    status: Mapped[Status]
    started_at: Mapped[datetime.datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())
    finished_at: Mapped[datetime.datetime] = mapped_column(DateTime(timezone=True), nullable=True)
    severity_count: Mapped[SeverityCount] = relationship("SeverityCount")
    scanners: Mapped[List["Scanner"]] = relationship("Scanner")
    assets_scanned: Mapped[List["Asset"]] = relationship(
        "Asset",
        secondary="scans_assets",
        back_populates="scans"
    )


class ScanAsset(Base):
    __tablename__ = "scans_assets"

    id: Mapped[int] = mapped_column(primary_key=True)
    scan_id: Mapped[int] = mapped_column(ForeignKey("scans.id"), index=True)
    asset_id: Mapped[int] = mapped_column(ForeignKey("assets.id"))
