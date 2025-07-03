import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

# Load dataset
df = pd.read_csv("Sample_F1_Results.csv")

# Get top 3 drivers
top_drivers = df.groupby("Driver")["Points"].sum().nlargest(3).index.tolist()

# Build title and introduction
st.markdown("""
    <h1 style='text-align: center; color: #00C6FF;'>F1 Fan Predictions vs Actual Performance</h1>
    <h4 style='text-align: center;'>What fans believe vs how drivers really perform</h4>
""", unsafe_allow_html=True)

# Poll-style display
st.subheader("🏁 Fan Poll Predictions")
predictions = [
    {"percentage": 55, "driver": top_drivers[1], "correct": False},
    {"percentage": 30, "driver": top_drivers[0], "correct": True},
    {"percentage": 15, "driver": top_drivers[2], "correct": False},
]
cols = st.columns(3)
for i, res in enumerate(predictions):
    with cols[i]:
        st.metric(label=res["driver"], value=f"{res['percentage']}%")
        status = "✅ RIGHT" if res["correct"] else "❌ WRONG"
        st.markdown(
            f"<p style='text-align:center;'>{status}</p>", unsafe_allow_html=True)

# Trend chart (line)
st.subheader("📈 Driver Performance Over Races")
races = df["Race"].unique().tolist()
fig = go.Figure()
for driver in top_drivers:
    driver_df = df[df["Driver"] == driver].sort_values("Race")
    fig.add_trace(go.Scatter(x=driver_df["Race"], y=driver_df["Points"],
                             mode='lines+markers', name=driver))
fig.update_layout(template="plotly_dark", height=400,
                  margin=dict(l=40, r=40, t=40, b=40))
st.plotly_chart(fig, use_container_width=True)

# Donut-style country perception
st.subheader("🌍 Incorrect Predictions by Country")
countries = [
    {"name": "USA", "percentage": 70},
    {"name": "UK", "percentage": 65},
    {"name": "Spain", "percentage": 55},
    {"name": "Germany", "percentage": 50},
    {"name": "Brazil", "percentage": 45}
]
cols = st.columns(5)
for i, c in enumerate(countries):
    with cols[i]:
        pie_fig = go.Figure(go.Pie(
            values=[c["percentage"], 100 - c["percentage"]],
            labels=["Wrong", "Other"],
            hole=0.6,
            marker_colors=["#FF6F61", "#1f77b4"],
            textinfo='none'))
        pie_fig.update_layout(
            showlegend=False, margin=dict(t=10, b=10, l=10, r=10))
        st.plotly_chart(pie_fig, use_container_width=True)
        st.markdown(
            f"<p style='text-align:center'>{c['name']}<br>{c['percentage']}%</p>", unsafe_allow_html=True)
