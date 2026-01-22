import json
import pandas as pd
import streamlit as st

from engine.master_orchestrator import MasterOrchestrator

st.set_page_config(page_title="HP Engine v3 - Minimal Core", layout="wide")

st.title("HP Engine v3 - Minimal Core (PPDA + Field Tilt)")
st.caption("Contract-first | No silent drop | Popper gate | PlotSpec output")

with st.sidebar:
    st.header("Input")
    uploaded = st.file_uploader(
        "SportsBase Event CSV yükle",
        type=["csv"],
        accept_multiple_files=False
    )

    st.header("Metrics")
    m_ppda = st.checkbox("PPDA", value=True)
    m_ft = st.checkbox("FIELD_TILT", value=True)

    st.header("Run")
    run_btn = st.button("RUN PIPELINE")

# ---- Guardrails
selected_metrics = []
if m_ppda:
    selected_metrics.append("PPDA")
if m_ft:
    selected_metrics.append("FIELD_TILT")

if run_btn:
    if uploaded is None:
        st.error("CSV yüklemeden çalıştırılamaz.")
        st.stop()

    if not selected_metrics:
        st.error("En az 1 metrik seçmelisin.")
        st.stop()

    # Read CSV
    try:
        df = pd.read_csv(uploaded)
    except Exception as e:
        st.error(f"CSV okunamadı: {e}")
        st.stop()

    # Orchestrator init (registry paths relative to hp_engine_v3_min_core/)
    orch = MasterOrchestrator(registry_paths=[
        "canon/registry/tactical/ppda.yaml",
        "canon/registry/tactical/field_tilt.yaml",
    ])

    # Run
    out = orch.run(df, metrics=selected_metrics)

    # UI: 2 columns
    col1, col2 = st.columns([1, 1], gap="large")

    with col1:
        st.subheader("Narrative (Aurelia)")
        st.json(out.get("narrative", {}))

        st.subheader("Validation Report (SOT)")
        st.json(out.get("validation_report", {}))

        st.subheader("Provider Mapping")
        st.json(out.get("provider_mapping", {}))

    with col2:
        st.subheader("Metrics")
        st.json(out.get("metrics", {}))

        st.subheader("Claims (Popper Gate)")
        st.json(out.get("claims", []))

        st.subheader("PlotSpecs (UI render hint)")
        st.json(out.get("plotspecs", []))

    st.divider()
    st.subheader("Raw JSON Output")
    st.code(json.dumps(out, ensure_ascii=False, indent=2), language="json")
else:
    st.info("Soldan CSV yükle, metrik seç, RUN PIPELINE'a bas.")