class HPTaxonomy:
    """
    Futbol Ekolleri ve Oyun Modelleri Ontolojisi.
    Her ekolün gereksinimleri, metrik eşikleri ve ideal oyuncu profilleri burada tanımlanır.
    """
    
    PHILOSOPHIES = {
        "Juego de Posicion": {
            "requirements": ["High Field Tilt", "Central Dominance", "Progressive Passing"],
            "thresholds": {"possession": 60, "field_tilt": 65, "avg_pass_length": 16},
            "squad_needs": {"GK": "Sweeper-Keeper", "CB": "Ball-Playing", "DM": "Deep-Lying Creator"}
        },
        "Gegenpressing": {
            "requirements": ["High Intensity Pressing", "Verticality", "Quick Transitions"],
            "thresholds": {"ppda": 8.0, "high_regains": 12, "verticality_index": 0.7},
            "squad_needs": {"Fullbacks": "Work-Horses", "AM": "Pressing Monster"}
        },
        "Catenaccio / Low Block": {
            "requirements": ["Compactness", "Horizontal Discipline", "Direct Counter"],
            "thresholds": {"defensive_line_height": 35, "compactness_m2": 450},
            "squad_needs": {"CB": "Stopper", "ST": "Target Man"}
        }
    }

    def detect_philosophy(self, actual_metrics):
        """Gerçekleşen metriklerle ideal DNA'yı karşılaştırıp ekolü tespit eder."""
        # Burada 'actual_metrics' ile 'PHILOSOPHIES' karşılaştırılarak en yakın ekol bulunur.
        return "Juego de Posicion" # Simülasyon çıktısı
