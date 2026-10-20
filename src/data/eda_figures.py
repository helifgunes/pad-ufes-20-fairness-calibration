"""Aggregate-only scientific figures for the metadata exploration stage."""

from pathlib import Path
import textwrap

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

from .metadata_audit import CLASSES, patient_table

BLUE, ORANGE, GREY = "#0072B2", "#D55E00", "#777777"


def create_figures(frame: pd.DataFrame, audit: dict, output: Path) -> list[Path]:
    """Write SVG and PNG figures with no individual-level observations."""
    output = Path(output)
    output.mkdir(parents=True, exist_ok=True)
    plt.rcParams.update({"font.family": "DejaVu Sans", "font.size": 10,
                         "axes.spines.top": False, "axes.spines.right": False,
                         "svg.fonttype": "none", "svg.hashsalt": "pad-ufes20-phase2"})
    saved = []

    def finish(fig, name, note):
        fig.text(.01, .015, textwrap.fill(note, width=int(fig.get_figwidth()*14)),
                 fontsize=8, color="#444444", va="bottom")
        fig.tight_layout(rect=(0, .09, 1, 1))
        for extension in ["svg", "png"]:
            path = output / f"{name}.{extension}"
            kwargs = {"metadata": {"Date": None}} if extension == "svg" else {"dpi": 300}
            fig.savefig(path, facecolor="white", **kwargs)
            if extension == "svg":
                # Keep generated XML tidy without altering SVG path geometry.
                path.write_text("\n".join(line.rstrip() for line in
                                         path.read_text(encoding="utf-8").splitlines()) + "\n",
                                encoding="utf-8")
            saved.append(path)
        plt.close(fig)

    x = np.arange(len(CLASSES))
    fig, ax = plt.subplots(figsize=(9, 4.8))
    for offset, metric, label, colour in [(-.25, "images", "Images", BLUE),
            (0, "patient_lesion_pairs", "Patient–lesion pairs", ORANGE),
            (.25, "patients", "Patients with this diagnosis", GREY)]:
        values = [audit["class_support"][c][metric] for c in CLASSES]
        bars = ax.bar(x+offset, values, width=.24, label=label, color=colour)
        ax.bar_label(bars, fontsize=7, padding=2)
    ax.set_xticks(x, CLASSES)
    ax.set(ylabel="Count", title="Diagnostic class support by analysis unit")
    ax.margins(y=.18)
    ax.legend(frameon=False, fontsize=8)
    finish(fig, "class_support", "Source: verified PAD-UFES-20 v1 metadata. A patient can contribute to multiple diagnosis categories.")

    patients = patient_table(frame)
    fig, axes = plt.subplots(1, 2, figsize=(10, 4.6))
    gender = audit["patient_demographics"]["gender"]
    gender_counts = dict(gender["known_patient_distribution"])
    gender_counts["Missing / unresolved"] = sum(gender["status_patients"][k] for k in ["missing", "invalid", "conflict"])
    age_counts = audit["patient_demographics"]["age"]["age_group_patients"]
    for ax, counts, title in zip(axes, [gender_counts, age_counts],
                               ["Recorded gender", "Patient age groups"]):
        labels = list(counts)
        heights = [v if isinstance(v, int) else np.nan for v in counts.values()]
        bars = ax.bar(np.arange(len(labels)), heights, color=[BLUE, ORANGE, GREY][:len(labels)])
        ax.set_xticks(np.arange(len(labels)), labels, rotation=12, ha="right")
        ax.bar_label(bars, fontsize=9, padding=3)
        ax.set(title=title, ylabel="Unique patients")
        ax.margins(y=.15)
    finish(fig, "patient_demographics", f"N={len(patients):,} patients. All conflicting patient ages remain unresolved, including disagreements within the same age band.")

    distribution = audit["patient_demographics"]["fitspatrick"]["known_patient_distribution"]
    counts = [distribution.get(str(i), 0) for i in range(1, 7)]
    counts.append(audit["patient_demographics"]["fitspatrick"]["status_patients"]["missing"])
    fig, ax = plt.subplots(figsize=(8, 4.8))
    positions = np.arange(7)
    heights = [v if isinstance(v, int) else np.nan for v in counts]
    ax.bar(positions, heights, color=[BLUE]*6+[GREY])
    for position, value in zip(positions, counts):
        ax.text(position, (value+8) if isinstance(value, int) else 8,
                str(value), ha="center", va="bottom", fontsize=9)
    ax.set_xticks(positions, ["I", "II", "III", "IV", "V", "VI", "Missing"])
    ax.set(ylabel="Unique patients", xlabel="Recorded Fitzpatrick type",
           title="Recorded Fitzpatrick coverage is uneven")
    ax.margins(y=.15)
    finish(fig, "fitzpatrick_coverage", "Positive counts below 10 are suppressed and bars omitted. Fitzpatrick type is not an objective skin-colour measurement.")

    missing = {name: values for name, values in audit["missingness_by_image_record"].items()
               if values["unavailable_rows"] > 0}
    missing = dict(sorted(missing.items(), key=lambda pair: pair[1]["unavailable_rows"]))
    fig, ax = plt.subplots(figsize=(9, 8))
    y = np.arange(len(missing))
    blank = np.array([v["blank_rows"] for v in missing.values()])/len(frame)*100
    unknown = np.array([v["unknown_rows"] for v in missing.values()])/len(frame)*100
    ax.barh(y, blank, color=BLUE, label="Blank")
    ax.barh(y, unknown, left=blank, color=ORANGE, label="UNK")
    labels = ["fitzpatrick (source: fitspatrick)" if c == "fitspatrick" else c for c in missing]
    ax.set_yticks(y, labels)
    ax.set(xlabel="Unavailable image records (%)", title="Missing metadata by field", xlim=(0, 48))
    ax.legend(frameon=False)
    finish(fig, "metadata_missingness", f"Denominator: {len(frame):,} image records. Blank and literal UNK values are counted separately; raw values are not overwritten.")

    coverage = audit["demographic_coverage_by_diagnosis"]["gender"]
    known = np.array([coverage[c]["known_images"] for c in CLASSES])
    absent = np.array([coverage[c]["missing_images"] for c in CLASSES])
    fig, ax = plt.subplots(figsize=(8, 4.8))
    ax.bar(x, known/(known+absent)*100, color=BLUE, label="Recorded gender available")
    ax.bar(x, absent/(known+absent)*100, bottom=known/(known+absent)*100,
           color=GREY, label="Missing")
    ax.set_xticks(x, CLASSES)
    ax.set(ylabel="Image records (%)", title="Demographic availability differs by diagnosis", ylim=(0, 112))
    ax.legend(frameon=False, fontsize=8, loc="upper center", bbox_to_anchor=(.5, 1.2), ncol=2)
    finish(fig, "demographic_missingness_by_diagnosis", "Gender and Fitzpatrick missingness have identical record masks in this release. Availability does not imply representative sampling.")

    age = pd.to_numeric(patients.loc[patients.age_status.eq("known"), "age"])
    frequencies, edges = np.histogram(age, bins=[0, 20, 40, 60, 80, 100])
    fig, ax = plt.subplots(figsize=(8, 4.8))
    for left, right, count in zip(edges[:-1], edges[1:], frequencies):
        if 0 < count < 10:
            ax.text((left+right)/2, 3, "<10", ha="center")
        else:
            ax.bar((left+right)/2, count, width=(right-left)*.95, color=BLUE)
            ax.text((left+right)/2, count+5, str(count), ha="center")
    ax.set(xlabel="Age (years)", ylabel="Unique patients", title="Age distribution among patients with consistent records")
    ax.set_xticks(edges)
    ax.margins(y=.15)
    conflicts = audit["patient_demographics"]["age"]["status_patients"]["conflict"]
    finish(fig, "patient_age_distribution", f"N={len(age):,} patients with one consistent valid age; {conflicts:,} conflicting patients are excluded from this age-only plot. Small positive bins are suppressed.")
    return saved
