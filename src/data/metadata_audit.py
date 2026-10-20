"""Audit PAD-UFES-20 metadata without printing individual patient records.

The raw table is read as strings. Whitespace is stripped in a separate copy.
Blank and UNK values remain distinguishable in missingness summaries. A lesion
uses the composite (patient_id, lesion_id) key. Demographic summaries use one
entry per patient and flag conflicting observed values instead of selecting one.
"""

from __future__ import annotations

import hashlib
from datetime import datetime, timezone
from pathlib import Path

import numpy as np
import pandas as pd

CLASSES = ("ACK", "BCC", "MEL", "NEV", "SCC", "SEK")
REQUIRED = ("patient_id", "lesion_id", "img_id", "diagnostic", "age",
            "gender", "fitspatrick", "biopsed")
DEMOGRAPHICS = ("age", "gender", "fitspatrick")
EXPECTED_SHA256 = "14d145235cedb022548257acb0d84dcd949e2c916f65d2baa7c38ed5339e9527"
MISSING = ("", "UNK")


def sha256_file(path: Path) -> str:
    """Hash source bytes, not a re-serialized or normalized table."""
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def read_metadata(path: Path, *, verify_official: bool = True) -> pd.DataFrame:
    """Read the fixed release; reject nonmatching bytes before analysis."""
    if verify_official and sha256_file(path) != EXPECTED_SHA256:
        raise ValueError("Metadata checksum does not match the official version 1 file.")
    frame = pd.read_csv(path, dtype=str, keep_default_na=False)
    absent = set(REQUIRED) - set(frame.columns)
    if absent:
        raise ValueError(f"Required metadata columns are missing: {sorted(absent)}")
    return frame.apply(lambda col: col.str.strip())


def _observations(series: pd.Series) -> list[str]:
    return sorted(set(series[~series.isin(MISSING)]))


def _valid(attribute: str, value: str) -> bool:
    if attribute == "gender":
        # Preserve observed source categories; do not invent a binary schema.
        return value not in MISSING
    try:
        numeric = float(value)
    except (ValueError, TypeError):
        return False
    if not np.isfinite(numeric):
        return False
    if attribute == "age":
        return numeric.is_integer() and 0 <= numeric <= 120
    if attribute == "fitspatrick":
        return numeric.is_integer() and 1 <= numeric <= 6
    raise ValueError(f"Unsupported demographic attribute: {attribute}")


def patient_table(frame: pd.DataFrame) -> pd.DataFrame:
    """Derive patient summaries without filling any source row.

    A unique valid observed value may summarize a patient. Missing observations
    are still counted; two distinct values yield conflict even within one age
    band. The absence of visit dates prevents interpreting age disagreements.
    """
    rows = []
    for patient_id, group in frame.groupby("patient_id", sort=True):
        row = {"patient_id": patient_id}
        for attribute in DEMOGRAPHICS:
            values = _observations(group[attribute])
            if attribute in ("age", "fitspatrick"):
                values = sorted({str(int(float(value))) if _valid(attribute, value)
                                 else value for value in values})
            invalid = any(not _valid(attribute, value) for value in values)
            status = ("missing" if not values else "invalid" if invalid
                      else "conflict" if len(values) > 1 else "known")
            row[f"{attribute}_status"] = status
            row[attribute] = values[0] if status == "known" else None
            row[f"{attribute}_partly_missing"] = bool(
                values and group[attribute].isin(MISSING).any())
        rows.append(row)
    patients = pd.DataFrame(rows)
    if patients.empty:
        return patients
    patients["age_group"] = patients.apply(
        lambda row: ("Under 60" if float(row["age"]) < 60 else "60 and over")
        if row["age_status"] == "known" else "Unresolved / missing", axis=1)
    return patients


def lesion_table(frame: pd.DataFrame) -> pd.DataFrame:
    """Return one row per composite key, rejecting conflicting lesion labels."""
    grouped = frame.groupby(["patient_id", "lesion_id"], sort=True)
    if grouped["diagnostic"].nunique().gt(1).any():
        raise ValueError("At least one patient-lesion pair has conflicting diagnostic labels.")
    return grouped.agg(diagnostic=("diagnostic", "first"),
                       n_images=("img_id", "size")).reset_index()


def _counts(series: pd.Series, categories=None) -> dict[str, int]:
    observed = series.value_counts()
    order = list(categories) if categories is not None else sorted(observed.index)
    return {str(value): int(observed.get(value, 0)) for value in order}


def suppressed_distribution(counts: dict[str, int], minimum: int = 10) -> dict:
    """Mask small positive demographic counts, preserving true zeros.

    This is a publication convention, not a formal anonymisation guarantee.
    Several suppressed values can remain constrained by published margins.
    """
    return {key: (f"<{minimum}" if 0 < value < minimum else value)
            for key, value in counts.items()}


def audit_metadata(frame: pd.DataFrame, *, source_sha256: str | None = None) -> dict:
    """Produce aggregate diagnostics only. No individual IDs enter the report."""
    if frame.empty:
        raise ValueError("Metadata table is empty.")
    absent = set(REQUIRED) - set(frame.columns)
    if absent:
        raise ValueError(f"Required columns missing: {sorted(absent)}")
    if frame[list(REQUIRED[:4])].isin(MISSING).any().any():
        raise ValueError("Patient, lesion, image and target identifiers must be populated.")
    unexpected = sorted(set(frame.diagnostic) - set(CLASSES))
    if unexpected:
        raise ValueError(f"Undocumented diagnostic labels: {unexpected}")
    patients = patient_table(frame)
    lesions = lesion_table(frame)
    grouping = frame.groupby(["patient_id", "lesion_id"])
    missingness = {col: {
        "blank_rows": int(frame[col].eq("").sum()),
        "unknown_rows": int(frame[col].eq("UNK").sum()),
        "unavailable_rows": int(frame[col].isin(MISSING).sum()),
        "unavailable_percent": round(float(frame[col].isin(MISSING).mean()*100), 3)
    } for col in frame}
    demographics = {}
    for attribute in DEMOGRAPHICS:
        known = patients.loc[patients[f"{attribute}_status"].eq("known"), attribute]
        entry = {"status_patients": _counts(patients[f"{attribute}_status"],
                                          ["known", "missing", "conflict", "invalid"]),
                 "partly_missing_patients": int(patients[f"{attribute}_partly_missing"].sum())}
        if attribute == "age":
            age = pd.to_numeric(known)
            entry["known_patient_age_summary_years"] = {
                "n": int(len(age)), "mean": round(float(age.mean()), 3) if len(age) else None,
                "median": float(age.median()) if len(age) else None,
                "q1": float(age.quantile(.25)) if len(age) else None,
                "q3": float(age.quantile(.75)) if len(age) else None}
            entry["age_group_patients"] = _counts(patients.age_group,
                       ["Under 60", "60 and over", "Unresolved / missing"])
        else:
            entry["known_patient_distribution"] = suppressed_distribution(_counts(known))
        demographics[attribute] = entry
    records_by_class = _counts(frame.diagnostic, CLASSES)
    class_support = {label: {
        "images": records_by_class[label],
        "patient_lesion_pairs": int(lesions.diagnostic.eq(label).sum()),
        "patients": int(frame.loc[frame.diagnostic.eq(label), "patient_id"].nunique())
    } for label in CLASSES}
    coverage = {}
    for attribute in ["gender", "fitspatrick"]:
        coverage[attribute] = {label: {
            "known_images": int((frame.diagnostic.eq(label) & ~frame[attribute].isin(MISSING)).sum()),
            "missing_images": int((frame.diagnostic.eq(label) & frame[attribute].isin(MISSING)).sum())
        } for label in CLASSES}
    biopsed_values = set(frame.biopsed) - set(MISSING)
    if not biopsed_values.issubset({"True", "False"}):
        raise ValueError("Unexpected biopsed encoding; inspect source documentation.")
    checks = {
        "duplicate_image_ids_extra_rows": int(frame.img_id.duplicated().sum()),
        "duplicate_full_rows": int(frame.duplicated().sum()),
        "lesion_ids_used_by_multiple_patients": int(
            frame.groupby("lesion_id").patient_id.nunique().gt(1).sum()),
        "patient_lesion_attribute_conflicts": {
            col: int(grouping[col].apply(lambda s: len(_observations(s))).gt(1).sum())
            for col in ["diagnostic", "age", "gender", "fitspatrick", "biopsed"]},
        "filename_identifier_mismatches": int((~frame.apply(
            lambda row: row.img_id.startswith(row.patient_id+"_"+row.lesion_id+"_"),axis=1)).sum())}
    counts = {"image_records": len(frame), "metadata_columns": len(frame.columns),
              "unique_patients": len(patients),
              "unique_lesion_id_strings": int(frame.lesion_id.nunique()),
              "patient_lesion_pairs": len(lesions)}
    return {
        "analysis_date": datetime.now(timezone.utc).date().isoformat(), "source_sha256": source_sha256,
        "analysis_type": "metadata_only_no_model_results",
        "counts": counts, "schema_columns": list(frame.columns),
        "class_support": class_support, "missingness_by_image_record": missingness,
        "patient_demographics": demographics, "demographic_coverage_by_diagnosis": coverage,
        "integrity_checks": checks,
        "image_count_per_patient_lesion_pair": _counts(lesions.n_images),
        "biopsy_image_counts": _counts(frame.biopsed, ["True", "False"]),
        "gender_missingness_by_biopsy": {
            state: {"images": int(frame.biopsed.eq(state).sum()),
                    "gender_missing_images": int((frame.biopsed.eq(state) & frame.gender.isin(MISSING)).sum())}
            for state in ["True", "False"]},
        "publication_rule": "Positive demographic counts below 10 are displayed as <10; no IDs or individual ages are exported.",
        "image_content_audit": {"status": "not_performed", "reason": "Image files have not been downloaded or decoded."},
        "split_status": "not_created; feasibility depends on resolving the age policy and checking image content",
        "model_training_status": "not_started"}
