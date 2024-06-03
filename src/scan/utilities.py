from src.scan.models import Scan
from src.scan.schemas import SeverityCount, ScanOut


def map_to_schema(scan: Scan) -> ScanOut:
    # Build Assets
    assets_out = []
    for asset in scan.assets_scanned:
        assets_out.append(asset.id)
    # Build Scanners
    scanners_out = []
    for scanner in scan.scanners:
        scanners_out.append(scanner.scanner_name)
    severity_count = scan.severity_count
    severity_count_out = SeverityCount(
        critical=severity_count.critical,
        high=severity_count.high,
        medium=severity_count.medium,
        low=severity_count.low,
        information=severity_count.information
    )
    scan_out = ScanOut(
        id=scan.id,
        requested_by=scan.requested_by.id,
        name=scan.name,
        status=scan.status,
        assets_scanned=assets_out,
        scanners=scanners_out,
        severity_counts=severity_count_out,
        started_at=scan.started_at,
        finished_at=scan.finished_at
    )
    return scan_out


def call_worker_app():
    # TODO: Call worker app to create scan task for scanners
    pass
