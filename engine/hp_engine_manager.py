from engine.hp_engine_logic import HPLogic

class HPManager:
    """Mantık ve Veriyi Birleştiren Stratejik Katman."""
    
    def run_analysis(self, data, team_name):
        logic = HPLogic()
        
        # 1. Taktiksel Analiz
        actual_scores = logic.get_tactical_phases(data["events"])
        ppda_val = logic.calculate_ppda(data["events"])
        
        # 2. Somatotip (Örnek Ortalama Veri)
        somato = logic.calculate_somatotype(10, 12, 10, 8, 185, 80)
        
        return {
            "team": team_name,
            "expected": {"Kurulum": 75, "Baskı": 80, "Geçiş": 75, "Savunma": 85, "Bitiricilik": 65},
            "actual": actual_scores,
            "ppda": ppda_val,
            "somatotype": somato,
            "narrative": f"Marcello Lippi: {team_name} bugün {ppda_val} PPDA şiddetiyle 'Baskı' fazında egemenlik kurdu."
        }
