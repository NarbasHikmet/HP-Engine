from __future__ import annotations

import streamlit as st

from .api import METRICS, MetricCategory, get_metric, get_summary, search_metrics, get_by_category


def render_metrics_explorer():
    """
    Drop-in Streamlit UI panel for browsing the metrics encyclopedia.
    Safe to call from any Streamlit app.
    """
    st.subheader("📚 Football Metrics Encyclopedia")

    summary = get_summary()
    st.caption(f"Total metrics: {summary.get('total_metrics', len(METRICS))}")

    # Category overview
    with st.expander("Category summary", expanded=False):
        cats = []
        for c in MetricCategory:
            cats.append((c.value, len(get_by_category(c))))
        st.write({k: v for k, v in cats})

    mode = st.radio("Mode", ["Lookup by ID", "Search"], horizontal=True)

    if mode == "Lookup by ID":
        metric_id = st.selectbox("Metric ID", options=sorted(METRICS.keys()))
        m = get_metric(metric_id)
        if not m:
            st.error("Metric not found.")
            return
        _render_metric(m)

    else:
        q = st.text_input("Search (name / alias)", value="")
        if q.strip():
            results = search_metrics(q.strip())
            st.caption(f"Results: {len(results)}")
            if results:
                chosen = st.selectbox("Select a metric", options=[r.metric_id for r in results])
                m = get_metric(chosen)
                if m:
                    _render_metric(m)
            else:
                st.warning("No matches.")


def _render_metric(m):
    st.markdown(f"### {m.metric_id} — {m.full_name}")
    st.write(f"**TR:** {m.turkish_name}")
    st.write(f"**Category:** `{m.category.value}` / **Sub:** `{m.subcategory}`")
    st.write(m.description)

    col1, col2 = st.columns(2)
    with col1:
        st.write("**Unit:**", m.unit)
        st.write("**Range:**", m.range)
    with col2:
        st.write("**Dependencies:**", m.dependencies if m.dependencies else "—")
        st.write("**Aliases:**", m.aliases if m.aliases else "—")

    with st.expander("Formula / Method", expanded=False):
        st.code(m.formula or "—")

    with st.expander("Data requirements", expanded=False):
        st.json(m.data_requirements or {})

    with st.expander("Derivation steps", expanded=False):
        if m.derivation_steps:
            for i, step in enumerate(m.derivation_steps, 1):
                st.write(f"{i}. {step}")
        else:
            st.write("—")

    with st.expander("Platforms", expanded=False):
        if m.platforms:
            st.json([{
                "platform": p.platform,
                "field_name": p.field_name,
                "calculation_method": p.calculation_method,
                "notes": p.notes,
            } for p in m.platforms])
        else:
            st.write("—")

    with st.expander("References", expanded=False):
        if m.references:
            st.json([{
                "authors": r.authors,
                "title": r.title,
                "year": r.year,
                "venue": r.venue,
                "doi": r.doi,
                "url": r.url,
                "key_finding": r.key_finding,
            } for r in m.references])
        else:
            st.write("—")

    with st.expander("Use cases / Limitations", expanded=False):
        st.write("**Use cases:**")
        if m.use_cases:
            for x in m.use_cases:
                st.write(f"- {x}")
        else:
            st.write("- —")

        st.write("**Limitations:**")
        if m.limitations:
            for x in m.limitations:
                st.write(f"- {x}")
        else:
            st.write("- —")