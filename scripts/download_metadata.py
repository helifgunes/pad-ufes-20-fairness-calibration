"""Retrieve official metadata or import a browser-downloaded copy, then verify it."""

import argparse
import hashlib
import json
from pathlib import Path
import sys
from urllib.error import HTTPError, URLError
from urllib.request import urlopen

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
from src.data.metadata_audit import EXPECTED_SHA256

URL = "https://data.mendeley.com/public-files/datasets/zr7vgbcyr2/files/fa850265-57da-48f0-ba3e-998b3e44b1f6/file_downloaded"
FILE_PAGE = "https://data.mendeley.com/datasets/zr7vgbcyr2/1/files/fa850265-57da-48f0-ba3e-998b3e44b1f6"


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--from-file", type=Path, help="Import an official browser-downloaded metadata.csv")
    args = parser.parse_args()
    try:
        if args.from_file:
            payload = args.from_file.read_bytes()
            method = "browser_file_import"
        else:
            with urlopen(URL, timeout=30) as response:
                payload = response.read(2_000_001)
            method = "official_http_download"
    except (HTTPError, URLError) as error:
        raise SystemExit(f"Download failed: {error}. Download metadata.csv from {FILE_PAGE} and rerun with --from-file PATH. Do not bypass security challenges.")
    actual = hashlib.sha256(payload).hexdigest()
    if actual != EXPECTED_SHA256:
        raise SystemExit("Checksum mismatch: the source was not accepted or written to data/raw/.")
    destination = ROOT / "data/raw"
    destination.mkdir(parents=True, exist_ok=True)
    target = destination / "metadata.csv"
    if target.exists() and target.read_bytes() != payload:
        raise SystemExit("Existing metadata differs; preserve and inspect it before replacing it.")
    target.write_bytes(payload)
    from datetime import datetime, timezone
    provenance = {"dataset_doi": "10.17632/zr7vgbcyr2.1", "download_url": URL,
                  "official_file_page": FILE_PAGE, "sha256": actual,
                  "expected_official_sha256": EXPECTED_SHA256, "official_checksum_match": True,
                  "bytes": len(payload), "method": method,
                  "retrieved_date": datetime.now(timezone.utc).date().isoformat()}
    (destination/"metadata_provenance.json").write_text(json.dumps(provenance, indent=2)+"\n")
    print(f"Verified {len(payload):,} bytes against the official SHA-256. Metadata remains local under data/raw/.")


if __name__ == "__main__":
    main()
