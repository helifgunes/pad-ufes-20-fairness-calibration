# Data Access and Local Storage

Status: official version 1 metadata was downloaded and checksum-verified on 19 October 2026. Image files have not been downloaded or inspected. See the [metadata report](../reports/eda_report.md).

1. Open the [official PAD-UFES-20 version 1 release](https://data.mendeley.com/datasets/zr7vgbcyr2/1).
2. Read the release information and [CC BY 4.0 licence](https://creativecommons.org/licenses/by/4.0/). Cite the dataset DOI `10.17632/zr7vgbcyr2.1` and its associated paper. Retain attribution and identify changes.
3. Download the metadata first. Use `python scripts/download_metadata.py` or import an official browser download with `--from-file PATH`. The script rejects bytes that do not match the SHA-256 displayed on the official file page. Download images when the metadata audit and available storage have been checked.
4. Keep downloaded files and extracted contents under `data/raw/` or a separately configured local data root. Preserve the original files and record SHA-256 checksums.
5. Audit the actual CSV schema and archive contents before defining image paths. Do not assume an archive layout from a mirror or tutorial.
6. Store patient-linked split manifests, individual predictions and processed metadata locally, never in public results folders.

This directory is ignored except for this README. Do not override the ignore rule to publish the dataset. Notebooks must be inspected for embedded images and individual metadata before publication.

Dataset access does not establish institutional ethical approval for every downstream use. Follow applicable university research procedures and the source conditions. No attempt to identify patients is permitted in this project.
