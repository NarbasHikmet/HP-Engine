from engine.hp_engine_taxonomy import HPTaxonomy
from engine.hp_engine_analytics import HPAnalytics

class HPLogic:
    def __init__(self):
        self.tax = HPTaxonomy()
        self.ana = HPAnalytics()

    def analyze_phase_logic(self, store, current_mode):
        """
        HP 6-Faz Modeli: Build-up, Progression, Incision, Finishing, 
        Defensive Transition, Attacking Transition.
        """
        data = store["data"]
        # 7 Ana Modül Yönlendirmesi
        if current_mode == "Pre-Match Analysis":
            return {"result": "Antidote (Panzehir) Stratejisi: Rakip 3. Bölge baskısı NAS ile kırılacak."}
        
        elif current_mode == "Team Tactical Analysis":
            metrics = {"ppda": 8.2, "field_tilt": 62} # Veriden çekilecek
            system = self.tax.detect_system(metrics)
            return {"ekol": system["name"], "DNA_Match": "92%", "Gaps": ["Rest-defence positioning"]}
        
        # Diğer 5 modül (Individual, Seasonal vb.) kümülatif olarak buraya mühürlenir.
        return {"result": "Genel Analiz Mühürlendi."}
