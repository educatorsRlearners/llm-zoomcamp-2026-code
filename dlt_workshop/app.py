import pandas as pd
import plotly.graph_objects as go
import streamlit as st

st.set_page_config(page_title="Rank & Map", page_icon="🗺️", layout="centered")

FACTORS = ["Air quality", "Internet speed", "Public transport"]
FACTOR_COLUMNS = {
    "Air quality": "air_quality",
    "Internet speed": "internet_speed",
    "Public transport": "public_transport",
}

# All factor scores are 0-100, higher is better.
CITIES = pd.DataFrame(
    {
        "city": [
            "New York",
            "Los Angeles",
            "Chicago",
            "Houston",
            "Phoenix",
            "San Francisco",
            "Seattle",
            "Boston",
            "Denver",
            "Austin",
            "Miami",
            "Portland",
        ],
        "lat": [
            40.7128,
            34.0522,
            41.8781,
            29.7604,
            33.4484,
            37.7749,
            47.6062,
            42.3601,
            39.7392,
            30.2672,
            25.7617,
            45.5152,
        ],
        "lon": [
            -74.0060,
            -118.2437,
            -87.6298,
            -95.3698,
            -112.0740,
            -122.4194,
            -122.3321,
            -71.0589,
            -104.9903,
            -97.7431,
            -80.1918,
            -122.6784,
        ],
        "air_quality": [65, 45, 70, 55, 60, 75, 80, 72, 68, 66, 78, 82],
        "internet_speed": [85, 80, 78, 72, 70, 90, 88, 84, 75, 82, 74, 79],
        "public_transport": [95, 55, 85, 40, 42, 80, 68, 82, 50, 45, 48, 65],
    }
)

TOP_N = 5
MIN_MARKER_SIZE = 14
MAX_MARKER_SIZE = 46

ACCENT = "#2f6fed"  # single "highlighted" status color — not a categorical set

st.title("Rank items & explore the map")

st.subheader("1. Rank the factors in order of importance")
st.caption("Click factors below in order, most important first.")
ranked = st.multiselect(
    "Select factors in order of importance",
    options=FACTORS,
    default=[],
    label_visibility="collapsed",
)

if ranked:
    st.write("**Your ranking:**")
    for i, factor in enumerate(ranked, start=1):
        st.write(f"{i}. {factor}")
else:
    st.info("Select all three factors above to set your ranking.")


def compute_weights(ranked_factors: list[str]) -> dict[str, float]:
    """Most-important factor gets the highest weight; unranked factors get none."""
    if not ranked_factors:
        return {factor: 1 / len(FACTORS) for factor in FACTORS}
    n = len(ranked_factors)
    raw = {factor: n - i for i, factor in enumerate(ranked_factors)}
    total = sum(raw.values())
    return {factor: raw.get(factor, 0) / total for factor in FACTORS}


weights = compute_weights(ranked)

scored = CITIES.copy()
scored["score"] = sum(
    weights[factor] * scored[FACTOR_COLUMNS[factor]] for factor in FACTORS
)
top_cities = scored.sort_values("score", ascending=False).head(TOP_N)

score_min, score_max = top_cities["score"].min(), top_cities["score"].max()
if score_max > score_min:
    normalized = (top_cities["score"] - score_min) / (score_max - score_min)
else:
    normalized = pd.Series(1.0, index=top_cities.index)
marker_sizes = MIN_MARKER_SIZE + normalized * (MAX_MARKER_SIZE - MIN_MARKER_SIZE)

st.subheader(f"2. Top {TOP_N} cities for your ranking")

fig = go.Figure()

fig.add_trace(
    go.Scattergeo(
        lon=top_cities["lon"],
        lat=top_cities["lat"],
        text=top_cities["city"],
        mode="markers+text",
        textposition="top center",
        marker=dict(
            size=marker_sizes,
            color=ACCENT,
            line=dict(width=1, color="white"),
        ),
        name="Top cities",
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
