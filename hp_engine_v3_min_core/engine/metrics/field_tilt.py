from __future__ import annotations
from typing import Dict, Any, Tuple
import pandas as pd
import numpy as np

def _minute(ts_s: float) -> float:
    return ts_s / 60.0

def _bin_index(minute: float, bins):
    for i in range(len(bins)-1):
        if bins[i] <= minute < bins[i+1]:
            return f"{bins[i]}-{bins[i+1]}"
    return f"{bins[-2]}-{bins[-1]}+"

def calc_field_tilt_v1(events: pd.DataFrame, spec: Dict[str, Any]) -> Tuple[Dict[str, Any], Dict[str, Any]]:
    bins = spec.get("temporal", {}).get("bins_minutes", [0,15,30,45,60,75,90,120])
    final_third_x = (2/3) * 105.0

    df = events.copy()
    df["x"] = pd.to_numeric(df["x"], errors="coerce")
    df["timestamp_s"] = pd.to_numeric(df["timestamp_s"], errors="coerce")

    is_pass = df["event_type"].str.contains("pass", na=False)
    in_final = df["x"] >= final_third_x
    ft_pass = df[is_pass & in_final]

    teams = sorted([t for t in df["team_id"].dropna().unique().tolist()])
    out = {"match": {}, "bins": {}}

    df_min = df["timestamp_s"].apply(lambda x: _minute(x) if pd.notna(x) else np.nan)
    df["_bin"] = df_min.apply(lambda m: _bin_index(m, bins) if pd.notna(m) else "NA")
    ft_pass = ft_pass.assign(_bin=df.loc[ft_pass.index, "_bin"])

    total = int(len(ft_pass))
    for team in teams:
        team_n = int(len(ft_pass[ft_pass["team_id"] == team]))
        share = (team_n / total) if total > 0 else np.nan
        out["match"][team] = {"field_tilt": share, "final_third_passes": team_n, "total_final_third_passes": total}

    for b in sorted(df["_bin"].dropna().unique().tolist()):
        if b == "NA":
            continue
        out["bins"][b] = {}
        ft_b = ft_pass[ft_pass["_bin"] == b]
        total_b = int(len(ft_b))
        for team in teams:
            team_n = int(len(ft_b[ft_b["team_id"] == team]))
            share = (team_n / total_b) if total_b > 0 else np.nan
            out["bins"][b][team] = {"field_tilt": share, "final_third_passes": team_n, "total_final_third_passes": total_b}

    meta = {
        "status": "FULL",
        "final_third_definition": f"x >= {final_third_x:.1f}m (final third)",
        "notes": ["Event-only field tilt; possession time not required."]
    }
    return out, meta