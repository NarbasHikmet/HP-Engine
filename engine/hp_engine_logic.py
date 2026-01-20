from engine.hp_engine_taxonomy import HPTaxonomy

class HPLogic:
    def __init__(self):
        self.taxonomy = HPTaxonomy()

    def run_team_tactical_analysis(self, store):
        """
        Takımın hangi ekolde olduğunu ve neye gereksinim duyduğunu analiz eder.
        """
        # 1. Gerçekleşen (MR) Verileri Al
        actual_metrics = {"ppda": 10.5, "field_tilt": 58, "possession": 55} # Veriden gelecek
        
        # 2. Ekol Tespiti
        detected_ekol = self.taxonomy.detect_philosophy(actual_metrics)
        ideal_requirements = self.taxonomy.PHILOSOPHIES[detected_ekol]
        
        # 3. Sapma (Anomali) Analizi
        # Örn: Ekol 60 possession istiyor ama biz 55 yapıyoruz.
        gap_analysis = f"{detected_ekol} için %5 daha fazla topla oynama gereklidir."
        
        return {
            "philosophy": detected_ekol,
            "requirements": ideal_requirements["requirements"],
            "gap_analysis": gap_analysis,
            "squad_alignment": ideal_requirements["squad_needs"]
        }
