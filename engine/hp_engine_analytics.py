class HPTaxonomy:
    """
    HP Engine: 8 Ana Dünya Futbol Sistemi ve Algoritmik Tetikleyiciler.
    Referans: Futbol Zeka Sistemi 1 & 2.
    """
    SYSTEMS = {
        "SYS-001": {
            "name": "Positional Play (Juego de Posición)",
            "architect": "Guardiola / Cruyff",
            "thresholds": {"possession": 65, "pass_accuracy": 88, "field_tilt": 65, "ppda": 12.0},
            "triggers": ["Spatial_Geometry", "1v1_Isolation", "Rest_Defence"],
            "squad_needs": {"DM": "DM_ANCHOR", "LCB": "CB_BALL_PLAYING", "ST": "ST_FALSE_NINE"}
        },
        "SYS-002": {
            "name": "Gegenpressing (Heavy Metal Football)",
            "architect": "Klopp / Rangnick",
            "thresholds": {"ppda": 8.5, "high_regains": 12, "verticality": 0.70, "sprint_vol": 95},
            "triggers": ["Sprint_Volume", "Vertical_Directness", "5_Second_Press"],
            "squad_needs": {"ST": "ST_PRESSING", "CB": "CB_PACE_DEFENDER", "DM": "DM_BALL_WINNER"}
        },
        "SYS-003": {
            "name": "Relational Play (Jogo Bonito 2.0)",
            "architect": "Fernando Diniz",
            "thresholds": {"pass_combination": 8, "short_pass_ratio": 85, "cluster_density": 0.75},
            "squad_needs": {"DM": "DM_REGISTA", "ST": "ST_PIVOT", "CM_MEZZALA"}
        },
        "SYS-004": {"name": "Vertical Transition (Bielsista)", "architect": "Bielsa", "thresholds": {"vertical_passes": 35, "sprint_distance": 1200}},
        "SYS-005": {"name": "Catenaccio Moderno", "architect": "Conte/Simeone", "thresholds": {"block_height": 35, "compactness": 450}},
        "SYS-006": {"name": "Total Football 2.0", "architect": "De Zerbi", "thresholds": {"gk_build_up": 25, "baiting_press": 0.8}},
        "SYS-007": {"name": "Direct Verticality", "architect": "Mourinho", "thresholds": {"direct_speed": 2.5, "long_ball_ratio": 18}},
        "SYS-008": {"name": "Asymmetric Attack", "architect": "Gasperini", "thresholds": {"wingback_xG": 0.25, "man_marking_intensity": 0.9}}
    }
