# backtester-py

# Requirement : 
- Need a datahandle which can convert past data into csv format
- Need a order fill simulator 
- Position & PnL Traker ( potofolio )
- Risk limit manager ( which limts risk )
- A main engine 
- Strategy . 

---

# Forex Strategy Backtester (Python)

> **⚠️ Under Development:** This project is currently in the active development phase. While core data preprocessing and market/order execution simulators are established, the main backtesting engine and position tracker are currently being implemented.

This repository implements a lightweight, modular, event-driven backtesting framework in Python designed specifically for foreign exchange (FX) markets (with initial configurations and data for **EURUSD**).

---

## 📂 Project Structure

```text
backtester/
├── data/                            # Raw and processed historical data
│   ├── DAT_ASCII_EURUSD_M1_2022.csv # Raw 1-Minute historical data (2022)
│   ├── DAT_ASCII_EURUSD_M1_2023.csv # Raw 1-Minute historical data (2023)
│   ├── DAT_ASCII_EURUSD_M1_2024.csv # Raw 1-Minute historical data (2024)
│   ├── DAT_ASCII_EURUSD_M1_2025.csv # Raw 1-Minute historical data (2025)
│   └── EURUSD_H1.csv                # Processed and resampled Hourly (H1) data
├── src/                             # Python source code
│   ├── merge.py                     # Data processing & resampling script
│   ├── data_handler.py              # Sequence data feeder (avoids look-ahead bias)
│   ├── excution.py                  # Order types, fills & execution simulator
│   └── backtester.py                # Main backtester engine (stub/in-development)
├── requirements.txt                 # Project dependencies
└── README.md                        # Documentation (this file)
```

---

## 🛠️ Tech Stack & Dependencies

The project is built using:
- **Python 3.10+**
- **Pandas** (v3.0.3) & **NumPy** (v2.5.1) for high-performance financial data manipulation.

All dependencies can be installed via the included `requirements.txt`.

---

## 🚀 Getting Started

### 1. Prerequisites & Virtual Environment

Set up a Python virtual environment to manage dependencies locally:

```bash
# Create a virtual environment
python -m venv .venv

# Activate the virtual environment
# On Linux/macOS:
source .venv/bin/activate
# On Windows (cmd):
# .venv\Scripts\activate.bat
```

### 2. Install Dependencies

Once your virtual environment is active, run:

```bash
pip install -r requirements.txt
```

### 3. Step 1: Preprocess and Resample Historical Data

The project operates on 1-Hour (H1) bars to balance resolution and computational efficiency. A utility is provided to parse raw multi-year 1-Minute (M1) files, clean up timezone/weekend entries, and resample them.

To generate the processed `data/EURUSD_H1.csv` dataset, execute:

```bash
python src/merge.py
```

*What this script does:*
1. Loads all raw `DAT_ASCII_EURUSD_M1_*.csv` files.
2. Normalizes column mappings (`DateTime`, `Open`, `High`, `Low`, `Close`, `Volume`).
3. Resamples high-frequency 1-Minute data into 1-Hour (H1) candlesticks.
4. Drops NaN records and removes weekends (Saturdays & Sundays).
5. Exports the clean dataset to `data/EURUSD_H1.csv`.

---

## 🧩 Architectural Components

### 📈 Data Handler (`src/data_handler.py`)
Responsible for feeding data sequentially to the strategy and main engine.
*   **Sequential Streaming:** Designed to emit one bar at a time (via `get_next_bar()`) to prevent **look-ahead bias** when evaluating strategy entry/exit conditions.
*   **Historical Context:** Provides utility methods like `get_data_until(index)` allowing strategies to calculate technical indicators (e.g., Moving Averages, RSI) only on data up to the current backtest timestamp.

### ⚡ Execution Simulator (`src/excution.py`)
Simulates how trading orders are processed and filled by a broker:
*   **Supported Orders:** Market, Limit, and Stop orders (`OrderType`), with Buy/Sell sides (`OrderSide`).
*   **Realism Parameters:** Configurable spreads (pips), commissions per transaction, and pip value multipliers (default configured for standard EURUSD contracts).
*   **Fill Ingestion:** Converts pending `Order` requests into concrete `Fill` events after checking bounds and prices against incoming bars.

### ⚙️ Backtester Engine & Tracker (`src/backtester.py` - *Under Construction*)
Planned to coordinate the flow of events between the `DataHandler`, the Strategy logic, the `ExecutionSimulator`, and the Position/PnL portfolio tracker.

---

## 🗺️ Roadmap & Next Steps

1.  **Main Backtester Loop:** Complete the `backtester.py` main event loop to orchestrate ticks/bars sequential updates.
2.  **Portfolio Tracker:** Track cash balance, open positions, average entry prices, margin requirements, and running unrealized/realized PnL.
3.  **Risk Manager:** Add a module to enforce position sizing limits and maximum drawdown stop-outs.
4.  **Strategy Interface:** Define a base Strategy class allowing developers to easily implement and test custom logic.
