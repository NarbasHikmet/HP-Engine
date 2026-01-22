class PopperGate:
    """
    Minimal falsifiability gate (v0):
    Produces VERIFIED / CONFLICT / INSUFFICIENT
    using cross-metric sanity checks.
    """

    def verify(self, metrics: dict):
        """
        metrics: {"PPDA": float|None, "Field_Tilt": float|None, "Pressing_Intensity": float|None}
        """
        status = {"overall": "VERIFIED", "checks": []}

        ppda = metrics.get("PPDA")
        ft = metrics.get("Field_Tilt")
        pi = metrics.get("Pressing_Intensity")

        # If any core metric missing -> insufficient
        if ppda is None or ft is None or pi is None:
            status["overall"] = "INSUFFICIENT"
            status["checks"].append({
                "rule": "core_metrics_present",
                "result": "FAIL",
                "note": "At least one core metric is None -> cannot publish strong claim"
            })
            return status

        # Rule-1: High pressing intensity should generally align with lower PPDA (proxy sanity)
        # If PI is high but PPDA is also high -> conflict
        if pi > 0.18 and ppda > 11:
            status["overall"] = "CONFLICT"
            status["checks"].append({
                "rule": "pressing_intensity_vs_ppda",
                "result": "CONFLICT",
                "note": f"PI={pi} suggests intense high-zone pressure, but PPDA={ppda} suggests weak press."
            })
        else:
            status["checks"].append({
                "rule": "pressing_intensity_vs_ppda",
                "result": "PASS",
                "note": f"PI={pi}, PPDA={ppda}"
            })

        # Rule-2: If Field Tilt is very high but PPDA is also very high, interpretation may be "ball dominance without counterpress"
        if ft > 60 and ppda > 12:
            status["overall"] = "CONFLICT"
            status["checks"].append({
                "rule": "field_tilt_vs_ppda",
                "result": "CONFLICT",
                "note": f"FT={ft}% dominance but PPDA={ppda} weak press: possible slow rest-defense / low counterpress."
            })
        else:
            status["checks"].append({
                "rule": "field_tilt_vs_ppda",
                "result": "PASS",
                "note": f"FT={ft}, PPDA={ppda}"
            })

        return status