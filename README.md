# FinCalc — Indian Investment Returns Calculator

A Python + Streamlit web app that calculates and visualizes SIP returns, lump sum
investment growth, and FD vs Mutual Fund comparisons — built for Indian investors.

## Features

- **SIP Calculator** — see how monthly investments grow over time
- **Lump Sum Calculator** — see how a one-time investment compounds
- **FD vs Mutual Fund Comparison** — visualize the tradeoff between guaranteed and market-linked returns

All calculations use real financial formulas:
- SIP Future Value: `M × [(1+r)ⁿ − 1] / r × (1+r)`
- Compound Interest: `P × (1+r)ⁿ`
- FD (quarterly compounding): `P × (1 + r/4)^(4n)`

## How To Run This (Step by Step)

### 1. Install Python
Download Python 3.10+ from [python.org](https://python.org) if you don't have it already.
Check it's installed by running this in your terminal:
```bash
python --version
```

### 2. Open This Folder in VS Code
- Open VS Code
- File → Open Folder → select this `fincalc-python` folder

### 3. Open a Terminal in VS Code
- Terminal → New Terminal (or press `` Ctrl+` ``)

### 4. Create a Virtual Environment (recommended, keeps things clean)
```bash
python -m venv venv
```

Activate it:
- **Windows:** `venv\Scripts\activate`
- **Mac/Linux:** `source venv/bin/activate`

### 5. Install Dependencies
```bash
pip install -r requirements.txt
```

### 6. Run The App
```bash
streamlit run app.py
```

This will automatically open the app in your browser at `http://localhost:8501`

---

## Project Structure
```
fincalc-python/
├── app.py              # Main application code
├── requirements.txt    # Python dependencies
└── README.md           # This file
```

## Tech Stack
- **Python** — core logic
- **Streamlit** — web app framework
- **Pandas** — data handling for growth tables
- **NumPy** — numerical calculations
- **Matplotlib** — charts and visualizations

## Author
Aryamaan Upadhyay — B.Tech CSE, Manipal Institute of Technology, Bengaluru
