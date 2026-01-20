class HPTaxonomy:
    """HP Engine: 8 Ana Sistem ve Algoritmik Eşikler."""
    SYSTEMS = {
        "SYS-001": {
            "name": "Positional Play (Juego de Posición)",
            "architect": "Guardiola/Cruyff",
            "triggers": ["Spatial_Geometry", "1v1_Isolation", "Rest_Defence"],
            "thresholds": {"possession": 65, "pass_accuracy": 88, "field_tilt": 65, "ppda": 12.0},
            "squad_needs": {"GK": "GK_SWEEPER", "CB": "CB_BALL_PLAYING", "DM": "DM_ANCHOR"}
        },
        "SYS-002": {
            "name": "Gegenpressing (Heavy Metal)",
            "architect": "Klopp/Rangnick",
            "triggers": ["Sprint_Volume", "Vertical_Directness", "5_Second_Press"],
            "thresholds": {"ppda": 8.5, "high_regains": 12, "verticality": 0.7, "sprint_vol": 95},
            "squad_needs": {"ST": "ST_PRESSING", "CB": "CB_PACE_DEFENDER", "DM": "DM_BALL_WINNER"}
        },
        "SYS-003": {
            "name": "Relational Play (Jogo Bonito 2.0)",
            "architect": "Diniz/Santana",
            "triggers": ["Cluster_Formation", "Micro_Connection"],
            "thresholds": {"pass_combination": 8, "short_pass_ratio": 85, "possession": 55}
        },
        # SYS-004-008: Diğer ekoller (Catenaccio, Total Football 2.0 vb. kümülatif olarak eklenecek)
    }

    def detect_system(self, metrics):
        """Gerçekleşen metriklerle ideal DNA'yı karşılaştırır."""
        if metrics.get("ppda", 15) < 9.0: return self.SYSTEMS["SYS-002"]
        return self.SYSTEMS["SYS-001"]
