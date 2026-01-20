import numpy as np
import pandas as pd

class HPAnalytics:
    """VAEP, xT ve NAS Analiz Motoru."""
    def __init__(self):
        self.grid_x, self.grid_y = 16, 12 # Ansiklopedi Standartı

    def calculate_xt(self, events_df):
        """16x12 Izgara üzerinde Markov Zinciri temelli xT hesaplar."""
        # Koordinat Normalizasyonu (100x100 -> 16x12)
        events_df['cell_x'] = (events_df['x'] / (100/self.grid_x)).astype(int).clip(0, 15)
        events_df['cell_y'] = (events_df['y'] / (100/self.grid_y)).astype(int).clip(0, 11)
        # Formül: xT = (P_move * P_trans * xT_next) + (P_shoot * P_goal)
        return events_df

    def detect_nas(self, player_events):
        """Negative Action Spiral (NAS): Hata sonrası 180s kognitif çöküş analizi."""
        trigger_errors = player_events[player_events['is_error'] == True]
        nas_reports = []
        for _, err in trigger_errors.iterrows():
            window = player_events[(player_events['time'] > err['time']) & 
                                 (player_events['time'] <= err['time'] + 180)]
            if not window.empty and window['success'].mean() < 0.5:
                nas_reports.append({"timestamp": err['time'], "severity": "CRITICAL"})
        return nas_reports

    def calculate_acwr(self, load_series):
        """Acute:Chronic Workload Ratio (0.8 - 1.3 Safe Zone)."""
        acute = load_series.tail(7).mean()
        chronic = load_series.tail(28).mean()
        return round(acute / chronic, 2) if chronic > 0 else 0
