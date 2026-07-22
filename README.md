# Time Series Forecasting and Risk-Aware Portfolio Analysis of NSE Stocks

An end-to-end statistical project that combines **time-series forecasting, volatility analysis, portfolio construction, and out-of-sample backtesting** for selected NSE stocks.

The project begins with a detailed case study of **Reliance Industries** and then extends the same workflow to an eight-stock portfolio. It compares classical forecasting models and evaluates whether forecast-guided allocation can improve portfolio performance relative to simpler strategies and the **Nifty 50** benchmark.

---

## Project Objective

The main objective is to answer the following question:

> Can classical time-series models support stock selection and portfolio allocation while controlling investment risk?

The project focuses on both prediction accuracy and practical portfolio performance. It avoids random train-test shuffling and uses chronological validation to reduce look-ahead bias.

---

## Project Workflow

The notebook is divided into two main parts.

### Part 1: Reliance Industries Case Study

- Historical price and return analysis
- Rolling mean and annualised volatility
- Augmented Dickey-Fuller stationarity testing
- ACF and PACF analysis
- STL trend decomposition
- ARIMA order selection using AIC
- ETS forecasting
- ARIMA-ETS ensemble forecasting
- One-step walk-forward validation
- Residual and Ljung-Box diagnostics
- ARCH testing and optional GARCH(1,1) volatility modelling
- Ten-trading-day price and volatility forecasts

### Part 2: Multi-Stock Portfolio Analysis

- Automated analysis of eight NSE stocks
- Reusable ARIMA, ETS, and ensemble forecasting pipeline
- Forecast error and directional-accuracy comparison
- Short-horizon expected-return estimation
- Rolling volatility and trend analysis
- Portfolio construction
- Out-of-sample backtesting
- Comparison with the Nifty 50
- Risk-adjusted performance evaluation

---

## Stock Universe

| Ticker | Company | Sector |
|---|---|---|
| `RELIANCE.NS` | Reliance Industries | Energy |
| `HDFCBANK.NS` | HDFC Bank | Banking |
| `TCS.NS` | Tata Consultancy Services | Information Technology |
| `SUNPHARMA.NS` | Sun Pharmaceutical | Pharmaceuticals |
| `MARUTI.NS` | Maruti Suzuki | Automobile |
| `HINDUNILVR.NS` | Hindustan Unilever | FMCG |
| `ADANIENT.NS` | Adani Enterprises | Infrastructure |
| `WIPRO.NS` | Wipro | Information Technology |

Daily market data is downloaded using `yfinance`.

**Fixed data period:** 1 January 2021 to 17 July 2026  
The notebook uses an exclusive `yfinance` end date of `2026-07-18` to keep the results reproducible.

---

## Forecasting Models

The following models are evaluated:

1. **Naive baseline**  
   The next price is predicted as the most recently observed price.

2. **ARIMA**  
   The differencing order is fixed at `d = 1`, while small values of `p` and `q` are compared using the Akaike Information Criterion.

3. **Exponential Smoothing (ETS)**  
   A damped additive-trend model is used to capture gradual price movement.

4. **ARIMA-ETS Ensemble**  
   The final prediction is the arithmetic average of the ARIMA and ETS forecasts.

### Validation Design

- Chronological 80/20 train-test split
- No random shuffling
- One-step walk-forward validation
- Training information is updated only after the actual observation becomes available
- Portfolio backtest weights are calculated using training-period information only

This design reduces data leakage and provides a more realistic evaluation than a long fixed-origin forecast.

---

## Portfolio Strategies

Four portfolio strategies are constructed.

### Equal Weight

Each stock receives the same portfolio weight.

### Forecast-Guided

Stocks are weighted using their predicted short-horizon returns. Forecast returns are shifted into a positive range and normalised.

### Inverse Volatility

Stocks with lower recent volatility receive larger weights:

\[
w_i \propto \frac{1}{\sigma_i}
\]

where \(\sigma_i\) is the stock's 30-day annualised volatility.

### Combined 60/40

The final risk-aware strategy combines forecast and volatility information:

\[
w_i^{combined}
=
0.60w_i^{forecast}
+
0.40w_i^{volatility}
\]

---

## Evaluation Metrics

### Forecasting Metrics

- Mean Absolute Error
- Root Mean Squared Error
- Mean Absolute Percentage Error
- Directional Accuracy
- Direction Coverage

### Portfolio Metrics

- Total Return
- Annualised Return
- Annualised Volatility
- Sharpe Ratio with a zero risk-free rate
- Maximum Drawdown
- Final Portfolio Value

---

## Final Backtest Results

**Out-of-sample comparison period:** 12 June 2025 to 17 July 2026  
**Initial virtual capital:** ₹10,00,000

| Strategy | Total Return | Annualised Return | Annualised Volatility | Sharpe Ratio | Maximum Drawdown |
|---|---:|---:|---:|---:|---:|
| Forecast-Guided | **-1.31%** | -1.22% | 16.69% | 0.009 | -23.83% |
| Nifty 50 | -2.23% | -2.08% | 12.89% | -0.099 | -15.18% |
| Combined 60/40 | -3.00% | -2.80% | 14.79% | -0.119 | -21.03% |
| Equal Weight | -4.10% | -3.83% | 13.59% | -0.220 | -19.92% |
| Inverse Volatility | -5.54% | -5.18% | 12.97% | -0.345 | -19.22% |

### Main Findings

- The **Forecast-Guided strategy produced the highest total return** during the test period.
- It outperformed the Nifty 50 by approximately **0.92 percentage points**.
- This outperformance came with higher volatility and a deeper maximum drawdown than the benchmark.
- The Combined 60/40 portfolio reduced some volatility relative to the Forecast-Guided strategy but did not produce a better return.
- ARIMA, ETS, and the ensemble generally delivered only small improvements over the naive baseline.
- Directional accuracy remained close to random for several stocks, showing the limitations of price-only forecasting.

The results suggest that statistical forecasts may support allocation decisions, but they should not be treated as reliable standalone trading signals.

---

## Repository Structure

```text
nse-time-series-portfolio-analysis/
│
├── Time_Series_NSE_Portfolio_Final_Cleaned.ipynb
├── README.md
│
└── time_series_project_outputs/
    ├── multi_stock_prices.csv
    ├── multi_stock_stationarity_volatility.csv
    ├── multi_stock_model_results.csv
    ├── final_stock_comparison.csv
    ├── current_portfolio_allocation.csv
    ├── backtest_inputs.csv
    ├── backtest_weights.csv
    ├── backtest_portfolio_values.csv
    ├── portfolio_and_nifty_values.csv
    ├── portfolio_performance_summary.csv
    ├── final_project_summary.csv
    ├── final_project_conclusion.txt
    ├── portfolio_drawdown_comparison.png
    └── total_return_comparison.png
```

The output folder and final ZIP archive are created automatically when the notebook is executed.

---

## How to Run

### Google Colab

1. Upload `Time_Series_NSE_Portfolio_Final_Cleaned.ipynb` to Google Colab.
2. Select **Runtime → Run all**.
3. Keep the internet connection active because the notebook downloads market data through `yfinance`.
4. Wait for the walk-forward and eight-stock modelling sections to finish.
5. Download the generated `time_series_project_final_outputs.zip` file.

### Local Environment

Clone the repository and create a virtual environment:

```bash
git clone <your-repository-url>
cd nse-time-series-portfolio-analysis

python -m venv .venv
```

Activate the environment:

```bash
# Windows
.venv\Scripts\activate

# macOS/Linux
source .venv/bin/activate
```

Install the dependencies:

```bash
pip install numpy pandas matplotlib yfinance statsmodels arch scikit-learn tqdm jupyter
```

Start Jupyter Notebook:

```bash
jupyter notebook
```

Open the project notebook and run the cells from top to bottom.

---

## Tools and Technologies

- Python
- Google Colab / Jupyter Notebook
- pandas
- NumPy
- Matplotlib
- yfinance
- statsmodels
- ARCH
- scikit-learn
- tqdm

---

## Skills Demonstrated

- Time-series preprocessing
- Stationarity testing
- ARIMA and exponential-smoothing models
- Walk-forward validation
- Forecast evaluation
- Residual diagnostics
- Volatility modelling
- Portfolio construction
- Backtesting without look-ahead bias
- Risk-adjusted performance analysis
- Benchmark comparison
- Reproducible research workflow

---

## Limitations

- Forecasts use historical market prices only.
- Earnings, macroeconomic variables, corporate events, and news sentiment are not included.
- The backtest uses fixed buy-and-hold weights.
- Transaction costs, taxes, and slippage are excluded.
- Forecast-guided weights can be sensitive to very small predicted-return differences.
- Results represent one fixed historical sample and may not generalise to future market conditions.

---

## Future Improvements

- Rolling or monthly portfolio rebalancing
- Transaction-cost and slippage modelling
- Financial-news sentiment analysis
- Macroeconomic and fundamental variables
- Sector and maximum-position constraints
- Alternative portfolio-optimisation methods
- More robust confidence-based forecast weighting
- Evaluation across multiple rolling backtest windows

---

## Author

**Anish Kumar**  
M.Sc. Statistics  
Banaras Hindu University

---

## Disclaimer

This project is intended for educational and statistical-analysis purposes only. It does not constitute financial or investment advice.
