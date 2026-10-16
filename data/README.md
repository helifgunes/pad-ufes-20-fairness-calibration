# Data Access and Local Storage

Status: the official documentation has been checked; no dataset files have been downloaded or audited locally.

1. Open the [official PAD-UFES-20 version 1 release](https://data.mendeley.com/datasets/zr7vgbcyr2/1).
2. Read the release information and [CC BY 4.0 licence](https://creativecommons.org/licenses/by/4.0/). Cite the dataset DOI `10.17632/zr7vgbcyr2.1` and its associated paper. Retain attribution and identify changes.
3. Download the metadata first during Phase 2. Download images when the audit and available storage have been checked. Do not use an unverified third-party repackaging as the authoritative source.
4. Keep downloaded files and extracted contents under `data/raw/` or a separately configured local data root. Preserve the original files and record SHA-256 checksums.
5. Audit the actual CSV schema and archive contents before defining image paths. Do not assume an archive layout from a mirror or tutorial.
6. Store patient-linked split manifests, individual predictions and processed metadata locally, never in public results folders.

This directory is ignored except for this README. Do not override the ignore rule to publish the dataset. Notebooks must be inspected for embedded images and individual metadata before publication.

Dataset access does not establish institutional ethical approval for every downstream use. Follow applicable university research procedures and the source conditions. No attempt to identify patients is permitted in this project.
