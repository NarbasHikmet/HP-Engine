from engine.master_orchestrator import MasterOrchestrator

events = [
    {"team": "opponent", "type": "pass", "x": 40},
    {"team": "opponent", "type": "pass", "x": 50},
    {"team": "team", "type": "tackle", "x": 55},
    {"team": "team", "type": "interception", "x": 60},
    {"team": "team", "type": "pass", "x": 75},
    {"team": "opponent", "type": "pass", "x": 80},
]

orch = MasterOrchestrator(registry_folder="canon/registry/tactical")
report = orch.run(events, context={"league": "generic"})

print(report)