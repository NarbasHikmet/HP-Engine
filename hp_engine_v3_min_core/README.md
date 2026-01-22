# HP Engine v3 - Minimal Core (PPDA + Field Tilt)

Working contract-first backbone:
- SportsBase-like provider mapping -> canonical events
- SOT validator that reports (no silent drop)
- Registry-driven MetricEngine
- Minimal PopperGate (claim status + confidence heuristic)
- PlotSpecFactory (no rendering; UI responsibility)
- AureliaNarrative (talk few, show limitations)

## Quick start
```bash
cd hp_engine_v3_min_core
pip install -r requirements.txt
python demo/run_match.py