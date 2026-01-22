class MetricEngine:

    def compute_ppda(self, events):
        opp_passes = len([e for e in events if e.get("team") == "opponent" and e.get("type") == "pass"])
        def_actions = len([e for e in events if e.get("team") == "team" and e.get("type") in ["tackle", "interception"]])

        if def_actions == 0:
            return None

        return round(opp_passes / def_actions, 2)

    def compute_field_tilt(self, events):
        team_final = len([
            e for e in events
            if e.get("team") == "team" and e.get("type") == "pass" and float(e.get("x", 0)) > 66
        ])
        opp_final = len([
            e for e in events
            if e.get("team") == "opponent" and e.get("type") == "pass" and float(e.get("x", 0)) > 66
        ])

        total = team_final + opp_final
        if total == 0:
            return None

        return round((team_final / total) * 100, 1)

    def compute_pressing_intensity(self, events):
        """
        Proxy (event-only):
        - numerator: team's defensive actions in high zone (x>66)
        - denominator: opponent passes (all)
        """
        opp_passes = len([e for e in events if e.get("team") == "opponent" and e.get("type") == "pass"])
        high_zone_def_actions = len([
            e for e in events
            if e.get("team") == "team"
            and e.get("type") in ["tackle", "interception", "foul"]
            and float(e.get("x", 0)) > 66
        ])

        if opp_passes == 0:
            return None

        return round(high_zone_def_actions / opp_passes, 3)