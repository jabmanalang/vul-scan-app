import datetime

from sqlalchemy.orm import Session

from src.asset.models import Asset
from src.asset.schemas import AssetBase
from src.user.models import User
from src.user.schemas import UserBase
from src.scan.models import Scan, Scanner, SeverityCount
from src.scan.schemas import ScanBase, ScanPatch
from src.vulnerability.models import Vulnerability, VulnerabilityAsset
from src.vulnerability.schemas import VulnerabilityBase
from src.enums import Status


def create_asset(db: Session, asset_schema: AssetBase) -> Asset:
    asset = Asset(**asset_schema.model_dump())
    db.add(asset)
    db.commit()
    db.refresh(asset)
    return asset


def read_asset(db: Session, asset_id: int) -> Asset | None:
    asset = db.query(Asset).where(Asset.id == asset_id).first()
    return asset


def read_assets(db: Session, asset_ids: list[int]) -> list[Asset]:
    assets = db.query(Asset).where(Asset.id.in_(asset_ids)).all()
    return assets


def create_user(db: Session, user_schema: UserBase) -> User:
    user = User(**user_schema.model_dump())
    db.add(user)
    db.commit()
    db.refresh(user)
    return user


def read_user(db: Session, user_id: int) -> User | None:
    user = db.query(User).where(User.id == user_id).first()
    return user


def create_scan(db: Session, scan_schema: ScanBase) -> Scan:
    scan = Scan()
    scan.requested_by = read_user(db, user_id=scan_schema.requested_by)
    scan.name = scan_schema.name
    scan.status = Status.in_progress
    scan.severity_count = SeverityCount(critical=0, high=0, medium=0, low=0, information=0)
    db.add(scan)
    db.flush()
    db.refresh(scan)

    for asset_id in scan_schema.assets_scanned:
        asset = read_asset(db, asset_id=asset_id)
        scan.assets_scanned.append(asset)

    for scanner in scan_schema.scanners:
        scanner_model = Scanner(scanner_name=scanner)
        scan.scanners.append(scanner_model)

    db.commit()
    db.refresh(scan)
    return scan


def read_scan(db: Session, scan_id: int) -> Scan | None:
    scan = db.query(Scan).filter(Scan.id == scan_id).first()
    return scan


def update_scan(db: Session, scan_id: int, patch_scan_schema: ScanPatch) -> Scan:
    scan = read_scan(db, scan_id=scan_id)
    scan.status = patch_scan_schema.status
    scan.severity_count.critical = patch_scan_schema.severity_counts.critical
    scan.severity_count.high = patch_scan_schema.severity_counts.high
    scan.severity_count.medium = patch_scan_schema.severity_counts.medium
    scan.severity_count.low = patch_scan_schema.severity_counts.low
    scan.severity_count.information = patch_scan_schema.severity_counts.information
    if patch_scan_schema.status == Status.completed:
        scan.finished_at = datetime.datetime.now(tz=datetime.timezone.utc).replace(microsecond=0)
    else:
        scan.finished_at = None
    db.commit()
    db.refresh(scan)
    return scan


def create_vulnerability(db: Session, vulnerability_schema: VulnerabilityBase) -> Vulnerability:
    vul = Vulnerability(**vulnerability_schema.model_dump(exclude={"from_scan", "affected_assets"}))
    scan = read_scan(db, scan_id=vulnerability_schema.from_scan)
    vul.from_scan = scan
    assets = read_assets(db, asset_ids=vulnerability_schema.affected_assets)
    vul.affected_assets = assets
    db.add(vul)
    db.commit()
    db.refresh(vul)
    return vul


def read_vulnerabilities(db: Session, scan_id: int | None, asset_id: int | None) -> list[Vulnerability]:
    vul = db.query(Vulnerability).join(VulnerabilityAsset)
    if scan_id is not None:
        vul = vul.filter(Vulnerability.from_scan_id == scan_id)
    if asset_id is not None:
        vul = vul.filter(VulnerabilityAsset.asset_id == asset_id)
    return vul.all()
