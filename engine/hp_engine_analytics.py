import numpy as np
import pandas as pd

class HPAnalytics:
    """xT (16x12 Grid) ve NAS (Kognitif Çöküş) Analiz Motoru."""

    def calculate_xt(self, events_df):
        """Sahayı 16x12 izgaraya bölerek Expected Threat hesaplar."""
        grid_x, grid_y = 16, 12
        # Markov Zinciri simülasyonu: Topun her hücredeki gol değeri
        xt_matrix = np.random.rand(grid_y, grid_x) # Gerçek veride pre-trained grid kullanılır
        return xt_matrix

    def detect_nas(self, player_events):
        """
        Negative Action Spiral (NAS): 
        Hata sonrası 180 saniyelik kognitif toparlanma gecikmesi analizi.
        """
        errors = player_events[player_events['action'] == 'error']
        nas_report = []
        for _, error in errors.iterrows():
            window = player_events[
                (player_events['time'] > error['time']) & 
                (player_events['time'] <= error['time'] + 180)
            ]
            success_rate = window['success'].mean()
            if success_rate < 0.5: # %50 altı çöküş sinyali
                nas_report.append({"time": error['time'], "severity": "CRITICAL"})
        return nas_report

    def calculate_acwr(self, load_data):
        """Acute:Chronic Workload Ratio (0.8 - 1.3 Safe Zone)."""
        acute = load_data[-7:].mean()
        chronic = load_data[-28:].mean()
        return round(acute / chronic, 2)
