import pandas as pd
import plotly.graph_objects as go
import streamlit as st

st.set_page_config(page_title="Rank & Map", page_icon="🗺️", layout="centered")

ITEMS = ["Item A", "Item B", "Item C"]

CITIES = pd.DataFrame(
    {
        "city": ["New York", "Los Angeles", "Chicago", "Houston", "Phoenix"],
        "lat": [40.7128, 34.0522, 41.8781, 29.7604, 33.4484],
        "lon": [-74.0060, -118.2437, -87.6298, -95.3698, -112.0740],
    }
)

ACCENT = "#2f6fed"  # single "highlighted" status color — not a categorical set

st.title("Rank items & explore the map")

st.subheader("1. Rank the items in order of importance")
st.caption("Click items below in order, most important first.")
ranked = st.multiselect(
    "Select items in order of importance",
    options=ITEMS,
    default=[],
    label_visibility="collapsed",
)

if ranked:
    st.write("**Your ranking:**")
    for i, item in enumerate(ranked, start=1):
        st.write(f"{i}. {item}")
else:
    st.info("Select all three items above to set your ranking.")

st.subheader("2. Highlighted cities")

fig = go.Figure()

fig.add_trace(
    go.Scattergeo(
        lon=CITIES["lon"],
        lat=CITIES["lat"],
        text=CITIES["city"],
        mode="markers+text",
        textposition="top center",
        marker=dict(size=10, color=ACCENT, line=dict(width=1, color="white")),
        name="Highlighted cities",
    )
)

fig.update_layout(
    geo=dict(
        scope="usa",
        projection_type="albers usa",
        showland=True,
        landcolor="rgb(235, 235, 235)",
        subunitcolor="rgb(255, 255, 255)",
        countrycolor="rgb(255, 255, 255)",
    ),
    margin=dict(l=0, r=0, t=0, b=0),
    height=500,
)

st.plotly_chart(fig, use_container_width=True)
