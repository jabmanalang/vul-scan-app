import logging
import sys

from fastapi import FastAPI

from src.asset.router import router as asset_router
from src.scan.router import router as scan_router
from src.user.router import router as user_router
from src.vulnerability.router import router as vulnerability_router
from src.database.session import Base, engine

logger = logging.getLogger("vul")
logger.setLevel(logging.DEBUG)
stream_handler = logging.StreamHandler(sys.stdout)
log_formatter = logging.Formatter(
    "%(asctime)s [%(processName)s: %(process)d] [%(threadName)s: %(thread)d] [%(levelname)s] %(name)s: %(message)s"
)
stream_handler.setFormatter(log_formatter)
logger.addHandler(stream_handler)

Base.metadata.create_all(bind=engine)

app = FastAPI()

app.include_router(asset_router)
app.include_router(user_router)
app.include_router(scan_router)
app.include_router(vulnerability_router)
