class MetricEngine:

    def compute_ppda(self, events):
        opp_passes = len([e for e in events if e["team"] == "opponent" and e["type"] == "pass"])
        def_actions = len([e for e in events if e["team"] == "team" and e["type"] in ["tackle", "interception"]])

        if def_actions == 0:
            return None

        return round(opp_passes / def_actions, 2)

    def compute_field_tilt(self, events):
        team_final = len([
            e for e in events
            if e["team"] == "team" and e["type"] == "pass" and e["x"] > 66
        ])
        opp_final = len([
            e for e in events
            if e["team"] == "opponent" and e["type"] == "pass" and e["x"] > 66
        ])

        total = team_final + opp_final
        if total == 0:
            return None

        return round((team_final / total) * 100, 1)