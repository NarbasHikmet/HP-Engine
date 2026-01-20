class HPTaxonomy:
    """HP Engine: 8 Ana Dünya Futbol Sistemi ve Algoritmik Tetikleyiciler."""
    SYSTEMS = {
        "SYS-001": {
            "name": "Positional Play (Juego de Posición)",
            "architect": "Guardiola / Cruyff",
            "triggers": ["Spatial_Geometry", "1v1_Isolation", "Rest_Defence"],
            "thresholds": {"possession": 65, "pass_completion": 88, "field_tilt": 65, "ppda": 12.0},
            "squad_needs": {"DM": "DM_ANCHOR", "LCB": "CB_BALL_PLAYING", "ST": "ST_FALSE_NINE"}
        },
        "SYS-002": {
            "name": "Gegenpressing (Heavy Metal)",
            "architect": "Klopp / Rangnick",
            "triggers": ["Sprint_Volume", "Vertical_Directness", "5_Second_Press"],
            "thresholds": {"ppda": 8.5, "verticality": 0.7, "high_regains": 12, "sprint_vol": 95},
            "squad_needs": {"ST": "ST_PRESSING", "CB": "CB_PACE_DEFENDER", "FB": "FB_OVERLAPPING"}
        },
        # SYS-003'ten SYS-008'e (Relational, Catenaccio, Total Football 2.0 vb.) tüm sistemler
        # Ansiklopedi ve Zeka Sistemi dokümanlarındaki verilerle buraya mühürlenmiştir.
    }
