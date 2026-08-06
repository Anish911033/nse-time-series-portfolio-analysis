"""
Streamlit dashboard for the NSE Time-Series Portfolio Analysis project.

It reads the CSV / PNG artifacts produced by the notebook
(time_series_project_outputs/) and presents them as an interactive
dashboard. It does NOT re-run ARIMA/ETS/GARCH live — those are heavy
and depend on live yfinance downloads, which is not a good fit for a
web dashboard. Re-run the notebook periodically (locally or in CI) and
commit the refreshed CSVs to update the dashboard.
"""

import os
from pathlib import Path

import pandas as pd
import streamlit as st
import plotly.express as px
import plotly.graph_objects as go

st.set_page_config(
    page_title="NSE Time-Series & Portfolio Analysis",
    layout="wide",
    initial_sidebar_state="expanded",
)

OUTPUT_DIR = Path(os.environ.get("OUTPUT_DIR", "time_series_project_outputs"))


@st.cache_data(show_spinner=False)
def load_csv(name: str) -> pd.DataFrame | None:
    path = OUTPUT_DIR / name
    if not path.exists():
        return None
    return pd.read_csv(path)


@st.cache_data(show_spinner=False)
def load_text(name: str) -> str | None:
    path = OUTPUT_DIR / name
    if not path.exists():
        return None
    return path.read_text()


def missing_file_notice(name: str):
    st.info(
        f"`{name}` was not found in `{OUTPUT_DIR}/`. "
        "Run the notebook once and commit its outputs to see this section."
    )


# ---------------------------------------------------------------- Sidebar
st.sidebar.title("NSE Portfolio Analysis")
st.sidebar.caption("Time-series forecasting + risk-aware portfolio backtest")
page = st.sidebar.radio(
    "Section",
    [
        "Overview",
        "Stock Prices & Volatility",
        "Model Comparison",
        "Portfolio Allocation",
        "Backtest Results",
        "Conclusion",
    ],
)

st.sidebar.markdown("---")
st.sidebar.markdown(
    "[GitHub repo](https://github.com/Anish911033/nse-time-series-portfolio-analysis)"
)

# ---------------------------------------------------------------- Overview
if page == "Overview":
    st.title("Time-Series Forecasting & Risk-Aware Portfolio Analysis")
    st.markdown(
        """
        End-to-end statistical workflow: a single-stock case study on
        **Reliance Industries**, extended to an eight-stock portfolio,
        comparing ARIMA, ETS, and an ARIMA-ETS ensemble, then building
        and backtesting four portfolio strategies against the **Nifty 50**.
        """
    )

    summary = load_csv("final_project_summary.csv")
    if summary is not None:
        st.subheader("Final Project Summary")
        st.dataframe(summary, use_container_width=True)
    else:
        missing_file_notice("final_project_summary.csv")

    col1, col2 = st.columns(2)
    with col1:
        img = OUTPUT_DIR / "total_return_comparison.png"
        if img.exists():
            st.image(str(img), caption="Total Return Comparison", use_container_width=True)
    with col2:
        img = OUTPUT_DIR / "portfolio_drawdown_comparison.png"
        if img.exists():
            st.image(str(img), caption="Drawdown Comparison", use_container_width=True)

# ------------------------------------------------- Stock Prices & Volatility
elif page == "Stock Prices & Volatility":
    st.title("Stock Prices & Volatility")

    prices = load_csv("multi_stock_prices.csv")
    if prices is not None:
        date_col = prices.columns[0]
        prices[date_col] = pd.to_datetime(prices[date_col])
        tickers = [c for c in prices.columns if c != date_col]

        chosen = st.multiselect("Select stocks", tickers, default=tickers[:3])
        if chosen:
            fig = px.line(prices, x=date_col, y=chosen, title="Adjusted Close Price")
            st.plotly_chart(fig, use_container_width=True)
    else:
        missing_file_notice("multi_stock_prices.csv")

    stat_vol = load_csv("multi_stock_stationarity_volatility.csv")
    if stat_vol is not None:
        st.subheader("Stationarity & Volatility Summary")
        st.dataframe(stat_vol, use_container_width=True)
    else:
        missing_file_notice("multi_stock_stationarity_volatility.csv")

# ------------------------------------------------------------ Model Comparison
elif page == "Model Comparison":
    st.title("Forecasting Model Comparison")
    st.caption("Naive baseline vs ARIMA vs ETS vs ARIMA-ETS ensemble")

    model_results = load_csv("multi_stock_model_results.csv")
    if model_results is not None:
        st.dataframe(model_results, use_container_width=True)

        metric_cols = [c for c in model_results.columns if c.upper() in ("MAE", "RMSE", "MAPE")]
        if metric_cols and "Model" in model_results.columns:
            metric = st.selectbox("Metric", metric_cols)
            fig = px.bar(
                model_results,
                x=model_results.columns[0],
                y=metric,
                color="Model" if "Model" in model_results.columns else None,
                barmode="group",
                title=f"{metric} by stock and model",
            )
            st.plotly_chart(fig, use_container_width=True)
    else:
        missing_file_notice("multi_stock_model_results.csv")

    comparison = load_csv("final_stock_comparison.csv")
    if comparison is not None:
        st.subheader("Final Stock Comparison")
        st.dataframe(comparison, use_container_width=True)
    else:
        missing_file_notice("final_stock_comparison.csv")

# --------------------------------------------------------- Portfolio Allocation
elif page == "Portfolio Allocation":
    st.title("Portfolio Allocation")

    alloc = load_csv("current_portfolio_allocation.csv")
    if alloc is not None:
        st.dataframe(alloc, use_container_width=True)

        weight_cols = [c for c in alloc.columns if "weight" in c.lower()]
        ticker_col = alloc.columns[0]
        if weight_cols:
            chosen_strategy = st.selectbox("Strategy weights to view", weight_cols)
            fig = px.pie(alloc, names=ticker_col, values=chosen_strategy, title=chosen_strategy)
            st.plotly_chart(fig, use_container_width=True)
    else:
        missing_file_notice("current_portfolio_allocation.csv")

    weights = load_csv("backtest_weights.csv")
    if weights is not None:
        st.subheader("Backtest Weights Over Time")
        st.dataframe(weights, use_container_width=True)
    else:
        missing_file_notice("backtest_weights.csv")

# ------------------------------------------------------------- Backtest Results
elif page == "Backtest Results":
    st.title("Out-of-Sample Backtest")

    perf = load_csv("portfolio_performance_summary.csv")
    if perf is not None:
        st.dataframe(perf, use_container_width=True)
    else:
        missing_file_notice("portfolio_performance_summary.csv")

    values = load_csv("portfolio_and_nifty_values.csv")
    if values is not None:
        date_col = values.columns[0]
        values[date_col] = pd.to_datetime(values[date_col])
        series_cols = [c for c in values.columns if c != date_col]
        chosen = st.multiselect("Series to plot", series_cols, default=series_cols)
        if chosen:
            fig = go.Figure()
            for c in chosen:
                fig.add_trace(go.Scatter(x=values[date_col], y=values[c], mode="lines", name=c))
            fig.update_layout(title="Portfolio Value vs Nifty 50", xaxis_title="Date", yaxis_title="Value (₹)")
            st.plotly_chart(fig, use_container_width=True)
    else:
        missing_file_notice("portfolio_and_nifty_values.csv")

    img = OUTPUT_DIR / "portfolio_drawdown_comparison.png"
    if img.exists():
        st.image(str(img), caption="Drawdown Comparison", use_container_width=True)

# ------------------------------------------------------------------- Conclusion
elif page == "Conclusion":
    st.title("Conclusion")
    text = load_text("final_project_conclusion.txt")
    if text:
        st.markdown(text)
    else:
        missing_file_notice("final_project_conclusion.txt")

    st.markdown("---")
    st.caption(
        "Educational / statistical-analysis project only. "
        "This is not financial or investment advice."
    )
