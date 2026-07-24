"""
FinCalc — Indian Investment Returns Calculator
Author: Aryamaan Upadhyay

A Streamlit web app that calculates and visualizes:
1. SIP (Systematic Investment Plan) returns
2. Lump Sum investment growth
3. FD vs Mutual Fund comparison

Run this with: streamlit run app.py
"""

import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# ── Page Configuration ───────────────────────────────────────────────────
st.set_page_config(
    page_title="FinCalc — Investment Calculator",
    page_icon="📈",
    layout="wide"
)

# ── Helper Functions ─────────────────────────────────────────────────────

def format_inr(amount):
    """Formats a number into Indian currency style (Lakh/Crore)."""
    if amount >= 1_00_00_000:
        return f"₹{amount / 1_00_00_000:.2f} Cr"
    elif amount >= 1_00_000:
        return f"₹{amount / 1_00_000:.2f} L"
    elif amount >= 1_000:
        return f"₹{amount / 1_000:.1f} K"
    else:
        return f"₹{amount:.0f}"


def calculate_sip(monthly_investment, annual_rate, years):
    """
    Calculates SIP maturity value using the standard SIP future value formula:
    FV = P × [(1 + r)^n − 1] / r × (1 + r)

    where:
        P = monthly investment
        r = monthly rate of return
        n = number of months
    """
    monthly_rate = annual_rate / 100 / 12
    months = years * 12

    future_value = monthly_investment * (
        ((1 + monthly_rate) ** months - 1) / monthly_rate
    ) * (1 + monthly_rate)

    total_invested = monthly_investment * months
    wealth_gained = future_value - total_invested

    return future_value, total_invested, wealth_gained


def calculate_lumpsum(principal, annual_rate, years):
    """
    Calculates lump sum investment growth using compound interest:
    A = P × (1 + r)^n
    """
    final_value = principal * (1 + annual_rate / 100) ** years
    profit = final_value - principal
    return final_value, profit


def calculate_fd(principal, annual_rate, years):
    """
    Calculates Fixed Deposit maturity value with quarterly compounding
    (standard practice for Indian FDs):
    A = P × (1 + r/4)^(4n)
    """
    return principal * (1 + annual_rate / 400) ** (4 * years)


def build_sip_growth_table(monthly_investment, annual_rate, years):
    """Builds a year-by-year growth table for SIP investments."""
    rows = []
    for year in range(1, years + 1):
        fv, invested, gain = calculate_sip(monthly_investment, annual_rate, year)
        rows.append({
            "Year": year,
            "Total Invested": invested,
            "Corpus Value": fv,
            "Wealth Gained": gain
        })
    return pd.DataFrame(rows)


def build_lumpsum_growth_table(principal, annual_rate, years):
    """Builds a year-by-year growth table for lump sum investments."""
    rows = []
    for year in range(0, years + 1):
        fv, profit = calculate_lumpsum(principal, annual_rate, year)
        rows.append({
            "Year": year,
            "Investment Value": fv,
            "Profit": profit
        })
    return pd.DataFrame(rows)


# ── Sidebar Navigation ───────────────────────────────────────────────────

st.sidebar.title("📈 FinCalc")
st.sidebar.markdown("Indian Investment Returns Calculator")
tool = st.sidebar.radio(
    "Choose a calculator:",
    ["SIP Calculator", "Lump Sum Calculator", "FD vs Mutual Fund"]
)

st.sidebar.markdown("---")
st.sidebar.markdown("**Built with:** Python, Streamlit, Pandas, Matplotlib")
st.sidebar.markdown("**Formulas used:**")
st.sidebar.code("SIP: M × [(1+r)ⁿ−1]/r × (1+r)\nLumpsum: P × (1+r)ⁿ\nFD: P × (1+r/4)⁴ⁿ", language="text")

# ── SIP Calculator Page ──────────────────────────────────────────────────

if tool == "SIP Calculator":
    st.title("SIP Calculator")
    st.markdown("Calculate returns on your **Systematic Investment Plan** (monthly investing)")

    col1, col2 = st.columns([1, 1.5])

    with col1:
        st.subheader("Parameters")
        monthly_amt = st.slider("Monthly Investment (₹)", 500, 100000, 5000, step=500)
        rate = st.slider("Expected Annual Return (%)", 1.0, 30.0, 12.0, step=0.5)
        years = st.slider("Investment Duration (years)", 1, 40, 10)

        future_value, invested, gain = calculate_sip(monthly_amt, rate, years)
        roi_pct = (gain / invested) * 100

        st.markdown("### Results")
        m1, m2, m3 = st.columns(3)
        m1.metric("Total Invested", format_inr(invested))
        m2.metric("Final Corpus", format_inr(future_value))
        m3.metric("Wealth Gained", format_inr(gain))
        st.metric("Return on Investment", f"{roi_pct:.1f}%")

    with col2:
        st.subheader("Growth Over Time")
        df = build_sip_growth_table(monthly_amt, rate, years)

        fig, ax = plt.subplots(figsize=(8, 5))
        ax.fill_between(df["Year"], df["Total Invested"], color="#6b6b88", alpha=0.3, label="Invested Amount")
        ax.fill_between(df["Year"], df["Corpus Value"], color="#00c896", alpha=0.3, label="Corpus Value")
        ax.plot(df["Year"], df["Total Invested"], color="#6b6b88", linewidth=1.5)
        ax.plot(df["Year"], df["Corpus Value"], color="#00c896", linewidth=2.5)
        ax.set_xlabel("Years")
        ax.set_ylabel("Value (₹)")
        ax.legend(loc="upper left")
        ax.grid(alpha=0.2)
        st.pyplot(fig)

        with st.expander("View year-by-year data table"):
            display_df = df.copy()
            for col in ["Total Invested", "Corpus Value", "Wealth Gained"]:
                display_df[col] = display_df[col].apply(lambda x: f"₹{x:,.0f}")
            st.dataframe(display_df, use_container_width=True, hide_index=True)

# ── Lump Sum Calculator Page ─────────────────────────────────────────────

elif tool == "Lump Sum Calculator":
    st.title("Lump Sum Calculator")
    st.markdown("Calculate growth on a **one-time investment**")

    col1, col2 = st.columns([1, 1.5])

    with col1:
        st.subheader("Parameters")
        principal = st.slider("Investment Amount (₹)", 10000, 10000000, 100000, step=10000)
        rate = st.slider("Expected Annual Return (%)", 1.0, 30.0, 12.0, step=0.5)
        years = st.slider("Investment Duration (years)", 1, 40, 10)

        final_value, profit = calculate_lumpsum(principal, rate, years)

        st.markdown("### Results")
        m1, m2, m3 = st.columns(3)
        m1.metric("Principal", format_inr(principal))
        m2.metric("Final Value", format_inr(final_value))
        m3.metric("Profit", format_inr(profit))
        st.metric("CAGR", f"{rate:.1f}%")

    with col2:
        st.subheader("Growth Over Time")
        df = build_lumpsum_growth_table(principal, rate, years)

        fig, ax = plt.subplots(figsize=(8, 5))
        ax.fill_between(df["Year"], df["Investment Value"], color="#7c6aff", alpha=0.3)
        ax.plot(df["Year"], df["Investment Value"], color="#7c6aff", linewidth=2.5)
        ax.axhline(y=principal, color="#6b6b88", linestyle="--", linewidth=1, label="Principal")
        ax.set_xlabel("Years")
        ax.set_ylabel("Value (₹)")
        ax.legend(loc="upper left")
        ax.grid(alpha=0.2)
        st.pyplot(fig)

        with st.expander("View year-by-year data table"):
            display_df = df.copy()
            for col in ["Investment Value", "Profit"]:
                display_df[col] = display_df[col].apply(lambda x: f"₹{x:,.0f}")
            st.dataframe(display_df, use_container_width=True, hide_index=True)

# ── FD vs Mutual Fund Comparison Page ────────────────────────────────────

else:
    st.title("FD vs Mutual Fund Comparison")
    st.markdown("Compare guaranteed **Fixed Deposit** returns against **Mutual Fund** growth potential")

    col1, col2 = st.columns([1, 1.5])

    with col1:
        st.subheader("Parameters")
        principal = st.slider("Principal Amount (₹)", 10000, 5000000, 100000, step=10000)
        fd_rate = st.slider("FD Interest Rate (%)", 3.0, 10.0, 7.0, step=0.25)
        mf_rate = st.slider("Expected MF Return (%)", 5.0, 25.0, 12.0, step=0.5)
        years = st.slider("Duration (years)", 1, 30, 10)

        fd_value = calculate_fd(principal, fd_rate, years)
        mf_value, _ = calculate_lumpsum(principal, mf_rate, years)
        difference = mf_value - fd_value

        st.markdown("### Results")
        m1, m2 = st.columns(2)
        m1.metric("FD Maturity Value", format_inr(fd_value))
        m2.metric("MF Corpus Value", format_inr(mf_value))
        st.metric("MF Advantage Over FD", format_inr(difference), delta=f"{(difference/fd_value)*100:.1f}%")

    with col2:
        st.subheader("Comparison Over Time")

        yrs = np.arange(0, years + 1)
        fd_series = [calculate_fd(principal, fd_rate, y) for y in yrs]
        mf_series = [calculate_lumpsum(principal, mf_rate, y)[0] for y in yrs]

        fig, ax = plt.subplots(figsize=(8, 5))
        ax.plot(yrs, fd_series, color="#6b6b88", linewidth=2.5, label="Fixed Deposit", marker='o', markersize=3)
        ax.plot(yrs, mf_series, color="#00c896", linewidth=2.5, label="Mutual Fund", marker='o', markersize=3)
        ax.fill_between(yrs, fd_series, mf_series, color="#00c896", alpha=0.1)
        ax.set_xlabel("Years")
        ax.set_ylabel("Value (₹)")
        ax.legend(loc="upper left")
        ax.grid(alpha=0.2)
        st.pyplot(fig)

        comparison_df = pd.DataFrame({
            "Year": yrs,
            "FD Value": [f"₹{v:,.0f}" for v in fd_series],
            "MF Value": [f"₹{v:,.0f}" for v in mf_series],
        })
        with st.expander("View year-by-year comparison table"):
            st.dataframe(comparison_df, use_container_width=True, hide_index=True)

# ── Footer ────────────────────────────────────────────────────────────────

st.markdown("---")
st.caption("FinCalc | Built with Python + Streamlit | Formulas based on standard Indian financial mathematics")
