#!/usr/bin/env python3
# Purpose: merge raw station CSVs, compute FPY and a failure Pareto, write outputs.

import pandas as pd
import pathlib

# --- Paths: use locations relative to THIS file ---
# __file__ = scripts/merge_and_fpy.py
ROOT = pathlib.Path(__file__).resolve().parents[1]        # project root
RAW_DIR = ROOT / "data" / "raw"                           # input CSVs
OUT_DIR = ROOT / "data" / "processed"                     # output files
OUT_DIR.mkdir(parents=True, exist_ok=True)                # create if missing

def load_all() -> pd.DataFrame:
    """Read every CSV in data/raw, tag source filename, normalize columns, add date."""
    files = list(RAW_DIR.glob("*.csv"))
    if not files:
        raise SystemExit("No CSVs found in data/raw")

    frames = []
    for f in files:
        df = pd.read_csv(f)           # read each file
        df["source_file"] = f.name    # keep provenance for traceability
        frames.append(df)

    data = pd.concat(frames, ignore_index=True)

    # Clean headers: lowercase, underscores (avoids Excel-style name drift)
    data.columns = [c.strip().lower().replace(" ", "_") for c in data.columns]

    # Parse timestamp to datetime; then extract a plain date for grouping
    if "timestamp" in data.columns:
        data["timestamp"] = pd.to_datetime(data["timestamp"], errors="coerce")
        data["date"] = data["timestamp"].dt.date

    return data

def compute_fpy(data: pd.DataFrame) -> pd.DataFrame:
    """First-pass yield by day.
    Assumes one record per serial per station attempt for the day.
    """
    grp = data.groupby("date").agg(
        units_built=("serial", "nunique"),
        units_pass=("result", lambda x: (x == "PASS").sum()),
    ).reset_index()
    grp["fpy_pct"] = (grp["units_pass"] / grp["units_built"] * 100).round(2)
    return grp

def pareto_failures(data: pd.DataFrame) -> pd.DataFrame:
    """Count failures by fail_code and compute cumulative percent (Pareto)."""
    fails = data.query("result == 'FAIL'").copy()
    if fails.empty:
        return pd.DataFrame(columns=["fail_code", "count", "cum_pct"])
    # Empty strings become UNSPEC so they appear in the chart
    fails["fail_code"] = fails["fail_code"].replace({"": "UNSPEC"})
    p = (
        fails.groupby("fail_code")
        .size()
        .sort_values(ascending=False)
        .rename("count")
        .reset_index()
    )
    p["cum_pct"] = (p["count"].cumsum() / p["count"].sum() * 100).round(2)
    return p

def main():
    data = load_all()
    # Persist consolidated raw for auditing and future dashboards
    data.to_csv(OUT_DIR / "all_logs_consolidated.csv", index=False)

    fpy = compute_fpy(data)
    fpy.to_csv(OUT_DIR / "daily_fpy.csv", index=False)

    pareto = pareto_failures(data)
    pareto.to_csv(OUT_DIR / "failure_pareto.csv", index=False)

    print("OK ->", OUT_DIR)

if __name__ == "__main__":
    main()
