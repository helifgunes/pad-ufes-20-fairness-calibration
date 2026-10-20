"""Synthetic tests for errors that would materially change research conclusions."""

import copy
import json
from pathlib import Path
import subprocess
import sys

import pandas as pd
import pytest

from src.data.metadata_audit import (audit_metadata, lesion_table, patient_table,
                                    read_metadata, suppressed_distribution)


@pytest.fixture
def frame():
    return pd.DataFrame([
        dict(patient_id="patient_A", lesion_id="1", img_id="patient_A_1_a.png", diagnostic="BCC",
             age="59", gender="FEMALE", fitspatrick="2.0", biopsed="True"),
        dict(patient_id="patient_A", lesion_id="1", img_id="patient_A_1_b.png", diagnostic="BCC",
             age="59", gender="FEMALE", fitspatrick="2.0", biopsed="True"),
        dict(patient_id="patient_B", lesion_id="1", img_id="patient_B_1_a.png", diagnostic="NEV",
             age="60", gender="", fitspatrick="UNK", biopsed="False"),
    ])


def test_shared_lesion_id_does_not_merge_different_patients(frame):
    audit = audit_metadata(frame)
    assert audit["counts"]["unique_lesion_id_strings"] == 1
    assert audit["counts"]["patient_lesion_pairs"] == 2
    assert audit["integrity_checks"]["lesion_ids_used_by_multiple_patients"] == 1
    assert len(lesion_table(frame)) == 2


def test_repeated_images_do_not_inflate_patient_demographics(frame):
    patients = patient_table(frame)
    assert len(patients) == 2
    assert patients.gender_status.value_counts().to_dict() == {"known": 1, "missing": 1}
    assert patients.age_group.tolist() == ["Under 60", "60 and over"]


def test_conflicting_ages_are_not_silently_resolved(frame):
    extra = frame.iloc[[0]].copy()
    extra.loc[:, "lesion_id"] = "2"
    extra.loc[:, "img_id"] = "patient_A_2_a.png"
    extra.loc[:, "age"] = "61"
    combined = pd.concat([frame, extra], ignore_index=True)
    patient = patient_table(combined).set_index("patient_id").loc["patient_A"]
    assert patient.age_status == "conflict"
    assert patient.age is None
    assert patient.age_group == "Unresolved / missing"


def test_equivalent_numeric_spellings_do_not_create_conflicts(frame):
    frame.loc[1, "age"] = "59.0"
    frame.loc[1, "fitspatrick"] = "2"
    patient = patient_table(frame).set_index("patient_id").loc["patient_A"]
    assert patient.age_status == "known"
    assert patient.fitspatrick_status == "known"


def test_blank_and_unknown_remain_separate(frame):
    audit = audit_metadata(frame)
    assert audit["missingness_by_image_record"]["gender"]["blank_rows"] == 1
    assert audit["missingness_by_image_record"]["fitspatrick"]["unknown_rows"] == 1
    assert audit["missingness_by_image_record"]["fitspatrick"]["blank_rows"] == 0


def test_conflicting_lesion_targets_are_rejected(frame):
    frame.loc[1, "diagnostic"] = "MEL"
    with pytest.raises(ValueError, match="conflicting diagnostic"):
        lesion_table(frame)


def test_undocumented_diagnosis_is_not_silently_filtered(frame):
    frame.loc[0, "diagnostic"] = "OTHER"
    with pytest.raises(ValueError, match="Undocumented"):
        audit_metadata(frame)


def test_invalid_age_remains_unavailable_and_raw_frame_unchanged(frame):
    frame.loc[0:1, "age"] = "-1"
    original = copy.deepcopy(frame)
    audit_metadata(frame)
    pd.testing.assert_frame_equal(frame, original)
    assert patient_table(frame).iloc[0].age_status == "invalid"


def test_checksum_rejects_unverified_source(tmp_path, frame):
    path = tmp_path/"metadata.csv"
    frame.to_csv(path, index=False)
    with pytest.raises(ValueError, match="checksum"):
        read_metadata(path)


def test_sparse_demographic_counts_are_masked_but_zeros_are_preserved():
    assert suppressed_distribution({"a": 0, "b": 1, "c": 9, "d": 10}) == {
        "a": 0, "b": "<10", "c": "<10", "d": 10}


def test_report_contains_aggregates_not_patient_ids(frame):
    payload = json.dumps(audit_metadata(frame), allow_nan=False)
    assert "patient_A" not in payload
    assert "patient_B" not in payload


def test_no_known_ages_is_serializable_without_fabricated_values(frame):
    frame.loc[:, "age"] = "UNK"
    report = audit_metadata(frame)
    assert report["patient_demographics"]["age"]["known_patient_age_summary_years"]["median"] is None
    json.dumps(report, allow_nan=False)


def test_cli_cannot_overwrite_metadata_with_its_report(tmp_path, frame):
    source = tmp_path/"metadata.csv"
    frame.to_csv(source, index=False)
    before = source.read_bytes()
    root = Path(__file__).resolve().parents[1]
    result = subprocess.run([sys.executable, str(root/"scripts/audit_data.py"),
                             "--metadata", str(source), "--output", str(source),
                             "--skip-figures"], capture_output=True, text=True)
    assert result.returncode != 0
    assert "must differ" in result.stderr
    assert source.read_bytes() == before
