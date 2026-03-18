%%writefile app.py
import streamlit as st
import pandas as pd
import numpy as np
import datetime
import calendar
from statsmodels.tsa.arima.model import ARIMA
import plotly.express as px
import plotly.graph_objects as go
import warnings

# Settings
warnings.filterwarnings("ignore")

# --- ORIGINAL BACKEND CODE (UNALTERED) ---
class AIExpenseManager:
    def __init__(self, budget):
        self.budget = budget
        self.limit_threshold = budget * 0.85
        self.df = pd.DataFrame(columns=['Date', 'Category', 'Description', 'Amount'])
        data = {
            'Month': pd.date_range(start='2025-01-01', periods=12, freq='ME'),
            'Total_Spent': [1200, 1350, 1300, 1600, 1550, 1800, 1950, 1850, 2100, 2300, 2200, 2500]
        }
        self.history_df = pd.DataFrame(data).set_index('Month')

    def add_expense(self, category, desc, amount):
        new_entry = {
            'Date': datetime.date.today(),
            'Category': category.title(),
            'Description': desc,
            'Amount': amount
        }
        self.df = pd.concat([self.df, pd.DataFrame([new_entry])], ignore_index=True)

# --- STREAMLIT FRONTEND ---
st.set_page_config(page_title="AI Expense Manager", layout="wide")

# Custom CSS for Dark Theme
st.markdown("""
    <style>
    .main { background-color: #111827; }
    .stMetric { background-color: #1F2937; padding: 15px; border-radius: 10px; border-left: 4px solid #3B82F6; }
    div[data-testid="stForm"] { border: 1px solid #374151; border-radius: 15px; }
    </style>
    """, unsafe_allow_headers=True)

st.title("🧠 AI Expense Intelligence Dashboard")

# Initialize the Class in Session State so data persists during clicks
if 'tracker' not in st.session_state:
    st.session_state.tracker = None

# 1. Salary Input
if st.session_state.tracker is None:
    with st.container():
        st.subheader("Welcome! Please initialize your budget.")
        user_salary = st.number_input("Enter Monthly Salary ($):", min_value=0.0, step=100.0)
        if st.button("Start Tracking"):
            st.session_state.tracker = AIExpenseManager(budget=user_salary)
            st.rerun()
else:
    tracker = st.session_state.tracker

    # Sidebar: Add Expense
    st.sidebar.header("➕ Log Daily Expense")
    categories = ["Household", "Food & Groceries", "Transport", "Health", "Entertainment", "Shopping", "Education", "Personal Care", "Others"]
    
    with st.sidebar.form("expense_form", clear_on_submit=True):
        cat = st.selectbox("Category", categories)
        desc = st.text_input("Description (e.g., Starbucks)")
        amt = st.number_input("Amount ($)", min_value=0.0, step=1.0)
        submitted = st.form_submit_button("Add Expense")
        
        if submitted and amt > 0:
            tracker.add_expense(cat, desc, amt)
            st.toast(f"Logged ${amt} in {cat}")

    # Top Metrics (Daily & Monthly Breakdown)
    total_spent = tracker.df['Amount'].sum()
    remaining = tracker.budget - total_spent
    
    today = datetime.date.today()
    last_day = calendar.monthrange(today.year, today.month)[1]
    days_remaining = last_day - today.day + 1
    daily_limit = remaining / days_remaining if remaining > 0 else 0

    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Total Salary", f"${tracker.budget:,.2f}")
    col2.metric("Total Spent", f"${total_spent:,.2f}")
    col3.metric("Remaining", f"${remaining:,.2f}")
    col4.metric("Daily Allowance", f"${daily_limit:,.2f}")

    # Main Analysis Section
    tab1, tab2 = st.tabs(["📊 Current Spending", "🤖 AI Forecast"])

    with tab1:
        if not tracker.df.empty:
            c1, c2 = st.columns(2)
            
            # Pie Chart (Proportions)
            summary = tracker.df.groupby('Category')['Amount'].sum().reset_index()
            fig_pie = px.pie(summary, values='Amount', names='Category', title="Spending Proportions", hole=0.4, template="plotly_dark")
            c1.plotly_chart(fig_pie, use_container_width=True)

            # Bar Chart (Category comparison)
            fig_bar = px.bar(summary, x='Category', y='Amount', title="Expenses by Category", template="plotly_dark", color='Amount')
            c2.plotly_chart(fig_bar, use_container_width=True)

            # Limit Alert Logic
            if total_spent > tracker.limit_threshold:
                st.error(f"⚠️ LIMIT ALERT: You have used {(total_spent/tracker.budget)*100:.1f}% of your budget. Status: BEHIND LIMIT.")
            else:
                st.success("✅ STATUS: WITHIN LIMIT. Your spending is healthy.")
            
            st.subheader("Transaction History")
            st.dataframe(tracker.df.sort_values(by='Date', ascending=False), use_container_width=True)
        else:
            st.info("No expenses logged yet. Use the sidebar to add your first expense.")

    with tab2:
        st.subheader("ARIMA Predictive Analysis")
        
        # ARIMA Logic
        series = tracker.history_df['Total_Spent']
        model = ARIMA(series, order=(1, 1, 1))
        model_fit = model.fit()
        forecast = model_fit.forecast(steps=1).iloc[0]

        # Allocation Rules
        st.write(f"**Predicted Spending for Next Month:** `${forecast:,.2f}`")
        
        ac1, ac2, ac3 = st.columns(3)
        ac1.metric("Essentials (50%)", f"${tracker.budget * 0.5:,.2f}")
        ac2.metric("Wants (30%)", f"${tracker.budget * 0.3:,.2f}")
        ac3.metric("Savings/Debt (20%)", f"${tracker.budget * 0.2:,.2f}")

        # Forecast Plot
        fig_forecast = go.Figure()
        fig_forecast.add_trace(go.Scatter(x=tracker.history_df.index, y=series, name="History", mode='lines+markers'))
        next_date = tracker.history_df.index[-1] + pd.DateOffset(months=1)
        fig_forecast.add_trace(go.Scatter(x=[next_date], y=[forecast], name="AI Forecast", marker=dict(color='red', size=12)))
        fig_forecast.add_hline(y=tracker.budget, line_dash="dash", line_color="gray", annotation_text="Budget Limit")
        fig_forecast.update_layout(title="Historical Trend & AI Prediction", template="plotly_dark")
        st.plotly_chart(fig_forecast, use_container_width=True)
