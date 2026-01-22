from engine.registry_gate import RegistryGate
from engine.metric_engine import MetricEngine

# Fake SportsBase-like events
events = [
    {"team": "opponent", "type": "pass", "x": 40},
    {"team": "opponent", "type": "pass", "x": 50},
    {"team": "team", "type": "tackle", "x": 55},
    {"team": "team", "type": "interception", "x": 60},
    {"team": "team", "type": "pass", "x": 75},
    {"team": "opponent", "type": "pass", "x": 80},
]

# Registry load
gate = RegistryGate()
metrics = gate.load_folder("canon/registry/tactical")

engine = MetricEngine()

ppda = engine.compute_ppda(events)
field_tilt = engine.compute_field_tilt(events)

print("PPDA:", ppda)
print("Field Tilt:", field_tilt)