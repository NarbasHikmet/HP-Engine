import streamlit as st
import pandas as pd

from engine.master_orchestrator import MasterOrchestrator

st.set_page_config(page_title="HP Engine v3", layout="wide")

st.title("HP Engine v3 — Contract-First Orchestrator")

st.sidebar.header("Input")
uploaded = st.sidebar.file_uploader("SportsBase CSV yükle", type=["csv"])

st.sidebar.header("Run Mode")
mode = st.sidebar.selectbox("Mode", ["pre_match", "post_match", "scouting"], index=0)

run_btn = st.sidebar.button("RUN MATCH", type="primary")

if "last_output" not in st.session_state:
    st.session_state.last_output = None

if run_btn:
    if uploaded is None:
        st.error("CSV yüklemeden RUN MATCH çalışmaz.")
    else:
        try:
            df = pd.read_csv(uploaded)

            orch = MasterOrchestrator(
                provider_name="SportsBase",
                canon_dir="canon",
            )

            output = orch.run(df, mode=mode)

            st.session_state.last_output = output
            st.success("Pipeline completed.")
        except Exception as e:
            st.exception(e)

out = st.session_state.last_output

if out:
    col1, col2 = st.columns([1, 1])

    with col1:
        st.subheader("Validation Report (SOT Gate)")
        st.json(out.get("validation_report", {}))

        st.subheader("Claims (Popper Gate Output)")
        claims = out.get("claims", [])
        st.write(f"Claims: {len(claims)}")
        st.json(claims)

    with col2:
        st.subheader("Features (Metric Engine Output)")
        st.json(out.get("features", {}))

        st.subheader("Plot Specs (UI renders; engine does NOT draw)")
        st.json(out.get("plotspecs", []))

    st.subheader("Transformed Data Preview")
    st.dataframe(out.get("data", pd.DataFrame()).head(50))