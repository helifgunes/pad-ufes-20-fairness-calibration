"""Run the metadata-only audit and save aggregate results and figures."""

import argparse
import hashlib
import json
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
from src.data.metadata_audit import audit_metadata, read_metadata, sha256_file
from src.data.eda_figures import create_figures


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--metadata", type=Path, default=ROOT/"data/raw/metadata.csv")
    parser.add_argument("--output", type=Path, default=ROOT/"results/metadata_audit.json")
    parser.add_argument("--figures", type=Path, default=ROOT/"figures/eda")
    parser.add_argument("--skip-figures", action="store_true")
    args = parser.parse_args()
    if args.metadata.resolve() == args.output.resolve():
        raise SystemExit("Metadata input and report output paths must differ; raw data was not changed.")
    frame = read_metadata(args.metadata)
    audit = audit_metadata(frame, source_sha256=sha256_file(args.metadata))
    audit["source_code_sha256"] = {rel: hashlib.sha256((ROOT/rel).read_bytes()).hexdigest()
        for rel in ["src/data/metadata_audit.py", "src/data/eda_figures.py", "scripts/audit_data.py"]}
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(audit, indent=2, allow_nan=False)+"\n")
    if not args.skip_figures:
        paths = create_figures(frame, audit, args.figures)
        print(f"Generated {len(paths)} aggregate figure files.")
    print(json.dumps({"counts": audit["counts"], "integrity_checks": audit["integrity_checks"],
                      "status": "Metadata exploration only; no image decoding, split or model training performed."}, indent=2))


if __name__ == "__main__":
    main()
