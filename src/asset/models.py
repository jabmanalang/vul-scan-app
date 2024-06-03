import datetime
from typing import List

from sqlalchemy import DateTime
from sqlalchemy.sql import func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.database.session import Base
from src.scan.models import Scan


class Asset(Base):
    __tablename__ = "assets"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str]
    description: Mapped[str]
    created: Mapped[datetime.datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())
    scans: Mapped[List["Scan"]] = relationship("Scan", secondary="scans_assets", back_populates="assets_scanned")
