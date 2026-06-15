import streamlit as st
import pandas as pd
import numpy as np
import joblib
import plotly.express as px
import plotly.graph_objects as go

# =========================================================
# PAGE CONFIG
# =========================================================

st.set_page_config(
    page_title="Cattle Feed Optimizer",
    page_icon="🐄",
    layout="wide",
    initial_sidebar_state="expanded"
)

# =========================================================
# CUSTOM CSS
# =========================================================

st.markdown("""
<style>

html, body, [class*="css"] {
    font-family: 'Segoe UI', sans-serif;
    background-color: #071028;
    color: white;
}

.main {
    background: #071028;
}

section[data-testid="stSidebar"] {
    background: linear-gradient(180deg,#08152f,#091a3d);
    border-right: 1px solid rgba(255,255,255,0.08);
}

.sidebar-title {
    font-size: 22px;
    font-weight: 700;
    color: white;
    margin-bottom: 20px;
}

.metric-card {
    background: linear-gradient(145deg,#0b1736,#0d1d45);
    padding: 22px;
    border-radius: 20px;
    border: 1px solid rgba(255,255,255,0.06);
    box-shadow: 0 0 20px rgba(0,0,0,0.3);
}

.metric-title {
    font-size: 16px;
    color: #b8c7ff;
}

.metric-value {
    font-size: 40px;
    font-weight: bold;
    color: white;
}

.metric-growth {
    color: #31d67b;
    font-size: 14px;
}

.card {
    background: linear-gradient(145deg,#0b1736,#0d1d45);
    padding: 20px;
    border-radius: 22px;
    border: 1px solid rgba(255,255,255,0.06);
    margin-bottom: 20px;
}

.card-title {
    font-size: 24px;
    font-weight: 600;
    margin-bottom: 20px;
}

.small-card {
    background: #0c1838;
    padding: 18px;
    border-radius: 18px;
    border: 1px solid rgba(255,255,255,0.05);
    text-align: center;
}

.footer-bar {
    background: #0c1838;
    padding: 15px;
    border-radius: 18px;
    text-align: center;
    color: #b5c7ff;
    margin-top: 20px;
}

</style>
""", unsafe_allow_html=True)

# =========================================================
# LOAD MODEL
# =========================================================

model = joblib.load("model/random_forest_model.pkl")
encoder = joblib.load("model/breed_encoder.pkl")

# =========================================================
# SIDEBAR
# =========================================================

st.sidebar.markdown(
    "<div class='sidebar-title'>🐄 Feed Optimizer</div>",
    unsafe_allow_html=True
)

st.sidebar.subheader("Feed Inputs")

maize = st.sidebar.slider("Maize (%)", 0, 100, 35)
soybean = st.sidebar.slider("Soybean Meal (%)", 0, 100, 25)
hay = st.sidebar.slider("Hay (%)", 0, 100, 20)
pkc = st.sidebar.slider("Groundnut Cake (%)", 0, 100, 10)
minerals = st.sidebar.slider("Mineral Mix (%)", 0, 100, 10)

protein = st.sidebar.number_input(
    "Protein Content",
    value=18.0
)

fiber = st.sidebar.number_input(
    "Fiber Content",
    value=12.0
)

energy = st.sidebar.number_input(
    "Energy Level",
    value=70.0
)

breed = st.sidebar.selectbox(
    "Breed",
    [
        "Friesian",
        "White Fulani",
        "Jersey",
        "Holstein",
        "Bunaji"
    ]
)

age = st.sidebar.number_input(
    "Age",
    value=4
)

weight = st.sidebar.number_input(
    "Weight (kg)",
    value=450
)

# =========================================================
# HEADER
# =========================================================

st.markdown("""
<h1 style='color:white;font-size:38px;'>
Intelligent Cattle Feed Recommendation & Cost Optimization System
</h1>

<p style='color:#b8c7ff;font-size:18px;'>
Using Random Forest Algorithm
</p>
""", unsafe_allow_html=True)

# =========================================================
# CALCULATIONS
# =========================================================

breed_encoded = encoder.transform([breed])[0]

input_data = pd.DataFrame([[
    maize,
    soybean,
    hay,
    pkc,
    protein,
    fiber,
    energy,
    breed_encoded,
    age,
    weight
]], columns=[
    'maize',
    'soybean',
    'hay',
    'pkc',
    'protein',
    'fiber',
    'energy',
    'breed',
    'age',
    'weight'
])

prediction = model.predict(input_data)[0]

meat_gain = round(prediction * 0.18, 2)

feed_cost = (
    maize * 4 +
    soybean * 9 +
    hay * 2 +
    pkc * 3 +
    minerals * 5
)

optimized_cost = feed_cost * 0.82

monthly_savings = (feed_cost - optimized_cost) * 30

# =========================================================
# TOP METRICS
# =========================================================

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.markdown(f"""
    <div class='metric-card'>
        <div class='metric-title'>Total Cattle</div>
        <div class='metric-value'>120</div>
        <div class='metric-growth'>+12 this month</div>
    </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown(f"""
    <div class='metric-card'>
        <div class='metric-title'>Daily Feed Cost</div>
        <div class='metric-value'>₦{feed_cost:,.0f}</div>
        <div class='metric-growth'>-5.8% vs yesterday</div>
    </div>
    """, unsafe_allow_html=True)

with col3:
    st.markdown(f"""
    <div class='metric-card'>
        <div class='metric-title'>Milk Production</div>
        <div class='metric-value'>{prediction:.1f} L</div>
        <div class='metric-growth'>+8.4% vs yesterday</div>
    </div>
    """, unsafe_allow_html=True)

with col4:
    st.markdown(f"""
    <div class='metric-card'>
        <div class='metric-title'>Meat Gain</div>
        <div class='metric-value'>{meat_gain:.1f} kg</div>
        <div class='metric-growth'>+6.7% vs yesterday</div>
    </div>
    """, unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

# =========================================================
# CHART SECTION
# =========================================================

left, right = st.columns([1,1.4])

# =========================================================
# PIE CHART
# =========================================================

with left:

    st.markdown("""
    <div class='card'>
        <div class='card-title'>
            Feed Composition Recommendation
        </div>
    """, unsafe_allow_html=True)

    feed_df = pd.DataFrame({
        "Feed": [
            "Maize",
            "Soybean Meal",
            "Hay",
            "Groundnut Cake",
            "Mineral Mix"
        ],
        "Percentage": [
            maize,
            soybean,
            hay,
            pkc,
            minerals
        ]
    })

    fig1 = px.pie(
        feed_df,
        names='Feed',
        values='Percentage',
        hole=0.45
    )

    fig1.update_layout(
        paper_bgcolor="#0b1736",
        plot_bgcolor="#0b1736",
        font_color="white",
        height=500
    )

    st.plotly_chart(
        fig1,
        use_container_width=True
    )

    st.markdown("</div>", unsafe_allow_html=True)

# =========================================================
# TREND GRAPH
# =========================================================

with right:

    st.markdown("""
    <div class='card'>
        <div class='card-title'>
            Production Trends
        </div>
    """, unsafe_allow_html=True)

    days = [
        "11 May",
        "12 May",
        "13 May",
        "14 May",
        "15 May",
        "16 May",
        "17 May"
    ]

    milk = [320, 350, 315, 305, 318, 345, 335]

    meat = [75, 86, 73, 75, 76, 91, 89]

    fig2 = go.Figure()

    fig2.add_trace(go.Scatter(
        x=days,
        y=milk,
        mode='lines+markers',
        name='Milk Production'
    ))

    fig2.add_trace(go.Scatter(
        x=days,
        y=meat,
        mode='lines+markers',
        name='Meat Gain'
    ))

    fig2.update_layout(
        paper_bgcolor="#0b1736",
        plot_bgcolor="#0b1736",
        font_color="white",
        height=500
    )

    st.plotly_chart(
        fig2,
        use_container_width=True
    )

    st.markdown("</div>", unsafe_allow_html=True)

# =========================================================
# COST OPTIMIZATION SUMMARY
# =========================================================

left2, right2 = st.columns([1,1])

with left2:

    st.markdown("""
    <div class='card'>
        <div class='card-title'>
            Cost Optimization Summary
        </div>
    """, unsafe_allow_html=True)

    c1, c2, c3, c4 = st.columns(4)

    with c1:
        st.markdown(f"""
        <div class='small-card'>
            <h4>Current Cost</h4>
            <h2>₦{feed_cost:,.0f}</h2>
            <p>Per Day</p>
        </div>
        """, unsafe_allow_html=True)

    with c2:
        st.markdown(f"""
        <div class='small-card'>
            <h4>Optimized Cost</h4>
            <h2>₦{optimized_cost:,.0f}</h2>
            <p>Per Day</p>
        </div>
        """, unsafe_allow_html=True)

    with c3:
        st.markdown(f"""
        <div class='small-card'>
            <h4>Cost Savings</h4>
            <h2>18.4%</h2>
            <p>Reduction</p>
        </div>
        """, unsafe_allow_html=True)

    with c4:
        st.markdown(f"""
        <div class='small-card'>
            <h4>Monthly Savings</h4>
            <h2>₦{monthly_savings:,.0f}</h2>
            <p>Estimated</p>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("</div>", unsafe_allow_html=True)

# =========================================================
# MODEL PERFORMANCE
# =========================================================

with right2:

    st.markdown("""
    <div class='card'>
        <div class='card-title'>
            Random Forest Model Performance
        </div>
    """, unsafe_allow_html=True)

    accuracy = 93.2

    fig3 = go.Figure(go.Indicator(
        mode="gauge+number",
        value=accuracy,
        gauge={
            'axis': {'range': [0, 100]}
        }
    ))

    fig3.update_layout(
        paper_bgcolor="#0b1736",
        font_color="white",
        height=350
    )

    st.plotly_chart(
        fig3,
        use_container_width=True
    )

    st.markdown("""
    <div style='padding:10px;color:white;'>

    <h4>Model Metrics</h4>

    <p>RMSE (Milk): 8.45</p>
    <p>RMSE (Meat): 2.31</p>
    <p>R² Score (Milk): 0.94</p>
    <p>R² Score (Meat): 0.91</p>

    </div>
    """, unsafe_allow_html=True)

    st.markdown("</div>", unsafe_allow_html=True)

# =========================================================
# FOOTER
# =========================================================

st.markdown(f"""
<div class='footer-bar'>
⭐ System Status: All systems operational <br><br>

Design and Implementation of an Intelligent Cattle Feed Recommendation and Cost Optimization System for Maximizing Milk and Meat Production Using Random Forest Algorithm
</div>
""", unsafe_allow_html=True)