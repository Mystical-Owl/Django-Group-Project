# FundChart_Plotly.py (or .ipynb)
# Interactive Plotly chart generator - saves all outputs to FundCharts_Store/

import pandas as pd
from datetime import datetime, timedelta
import plotly.express as px
import plotly.graph_objects as go
import os

# ───────────────────────────────────────────────────────────────
# CREATE OUTPUT FOLDER
# ───────────────────────────────────────────────────────────────

OUTPUT_FOLDER = "FundCharts_Store"
os.makedirs(OUTPUT_FOLDER, exist_ok=True)
print(f"All charts will be saved to: ./{OUTPUT_FOLDER}/\n")

# ───────────────────────────────────────────────────────────────
# IMPROVED DATA LOADING
# ───────────────────────────────────────────────────────────────

print("=== Loading and validating data ===")

try:
    df = pd.read_csv("funds_daily_2015_to_2036.csv")
    df['Date'] = pd.to_datetime(df['Date'], format='%Y-%m-%d', errors='coerce')
    df['Date'] = df['Date'].dt.tz_localize(None)
    df = df.dropna(subset=['Date'])
    df = df.set_index('Date').sort_index()
    
    print("→ Loaded successfully!")
    print("Shape:", df.shape)
    print("Date range:", df.index.min().date(), "→", df.index.max().date())
    
    key_dates = ['2015-12-31', '2025-12-31', '2036-12-31']
    print("\nKey date availability:")
    for d in key_dates:
        dt = pd.to_datetime(d)
        if dt in df.index:
            row = df.loc[dt]
            print(f"   {d}: Found → A={row['Fund_A']:.2f}  B={row['Fund_B']:.2f}  C={row['Fund_C']:.2f}  D={row['Fund_D']:.2f}")
        else:
            print(f"   {d}: NOT FOUND")
    
except Exception as e:
    print("Error loading CSV:")
    print(e)
    exit()

print("\nData ready. Starting interactive mode...\n")

# ───────────────────────────────────────────────────────────────
# FUND COLUMN MAPPING
# ───────────────────────────────────────────────────────────────

fund_map = {'A': 'Fund_A', 'B': 'Fund_B', 'C': 'Fund_C', 'D': 'Fund_D'}

# ───────────────────────────────────────────────────────────────
# HELPER FUNCTIONS
# ───────────────────────────────────────────────────────────────

def calculate_pct_change(start_val, end_val):
    return ((end_val - start_val) / start_val) * 100 if start_val != 0 else 0

def get_start_date(current_date, choice):
    if choice == "Past_3_months":
        return current_date - timedelta(days=91)
    elif choice == "Past_12_months":
        return current_date - timedelta(days=365)
    elif choice == "Past_36_months":
        return current_date - timedelta(days=1095)
    elif choice == "Past_60_months":
        return current_date - timedelta(days=1826)
    elif choice == "Past_since_2016":
        return datetime(2015, 12, 31)
    elif choice == "Past_since_this_year":
        return datetime(current_date.year, 1, 1)
    else:
        raise ValueError("Invalid choice for start_date")

def create_l_chart(data, fund_cols, title, start_date, current_date, is_combined=False):
    fig = go.Figure()
    
    pct_text = ''
    
    if is_combined:
        # Single shared y-axis for all funds (A/B/C/D on same scale)
        for col in fund_cols:
            fig.add_trace(go.Scatter(
                x=data.index, 
                y=data[col], 
                mode='lines', 
                name=col
            ))
        
        pct_text = '<br>'.join([f"{col}: {calculate_pct_change(data[col].iloc[0], data[col].iloc[-1]):.2f}%" for col in fund_cols])
        
        fig.update_layout(
            title=title,
            xaxis_title='Year',
            yaxis_title='Value',
            yaxis=dict(range=[0, None]),
            legend=dict(x=0, y=1.1, orientation='h')
        )
    else:
        col = fund_cols[0]
        fig.add_trace(go.Scatter(x=data.index, y=data[col], mode='lines', name=col))
        pct_change = calculate_pct_change(data[col].iloc[0], data[col].iloc[-1])
        pct_text = f"Percentage Change: {pct_change:.2f}%"
        
        # Y-axis logic
        if col == 'Fund_D':
            min_val = data[col].min()
            max_val = data[col].max()
            buffer = (max_val - min_val) * 0.05
            y_min = max(80, min_val * 0.98)
            y_max = max_val + buffer
            fig.update_layout(
                title=title,
                xaxis_title='Year',
                yaxis_title='Value',
                yaxis=dict(range=[y_min, y_max])
            )
        else:
            fig.update_layout(
                title=title,
                xaxis_title='Year',
                yaxis_title='Value',
                yaxis=dict(range=[0, None])
            )
    
    # X-axis formatting & visibility
    days_diff = (current_date - start_date).days
    if days_diff > 365:
        fig.update_xaxes(dtick='M12', tickformat='%Y', showline=True, linewidth=1.5, linecolor='black', gridcolor='lightgray')
    else:
        fig.update_xaxes(dtick='M3', tickformat='%Y %b', showline=True, linewidth=1.5, linecolor='black', gridcolor='lightgray')
    
    fig.update_xaxes(zeroline=False)
    
    fig.add_annotation(
        x=1.05, y=0.5, text=pct_text, showarrow=False,
        xref='paper', yref='paper', align='left', font=dict(size=12)
    )
    
    fig.update_layout(width=900, height=600, margin=dict(r=220))
    
    return fig

def create_b_chart(pct_changes, title):
    bar_df = pd.DataFrame({'Fund': list(pct_changes.keys()), 'Percentage Change': list(pct_changes.values())})
    fig = px.bar(bar_df, x='Fund', y='Percentage Change', title=title)
    fig.update_yaxes(range=[0, None])
    return fig

# ───────────────────────────────────────────────────────────────
# ACTION FUNCTIONS
# ───────────────────────────────────────────────────────────────

def your_return(fund, start_date_str, current_date_str):
    start_date = pd.to_datetime(start_date_str)
    current_date = pd.to_datetime(current_date_str)
    fund_col = fund_map[fund.upper()]
    data = df.loc[start_date:current_date, [fund_col]]
    title = f"{fund_col} Value Change from {start_date_str} to {current_date_str}"
    fig = create_l_chart(data, [fund_col], title, start_date, current_date)
    filename = os.path.join(OUTPUT_FOLDER, f"{fund_col}_Your_return_{start_date_str}_to_{current_date_str}.html")
    fig.write_html(filename, include_plotlyjs='cdn', auto_open=False)
    print(f"Chart saved to {filename}")

def past_return(fund, end_date_str, choice):
    end_date = pd.to_datetime(end_date_str)
    start_date = get_start_date(end_date, choice)
    fund_col = fund_map[fund.upper()]
    data = df.loc[start_date:end_date, [fund_col]]
    title = f"{fund_col} {choice} to {end_date_str}"
    fig = create_l_chart(data, [fund_col], title, start_date, end_date)
    filename = os.path.join(OUTPUT_FOLDER, f"{fund_col}_{choice}_to_{end_date_str}.html")
    fig.write_html(filename, include_plotlyjs='cdn', auto_open=False)
    print(f"Chart saved to {filename}")

def illustrate_return():
    current_date = datetime(2025, 12, 31)
    current_date_str = "2025-12-31"
    choices = ["Past_since_2016", "Past_since_this_year"]
    funds = ["A", "B", "C", "D"]
    
    # Individual charts
    for choice in choices:
        start_date = get_start_date(current_date, choice)
        data = df.loc[start_date:current_date]
        for fund in funds:
            fund_col = fund_map[fund]
            title = f"{fund_col} {choice} to {current_date_str}"
            fig = create_l_chart(data, [fund_col], title, start_date, current_date)
            filename = os.path.join(OUTPUT_FOLDER, f"{fund_col}_{choice}_to_{current_date_str}.html")
            fig.write_html(filename, include_plotlyjs='cdn', auto_open=False)
            print(f"Chart saved to {filename}")
    
    # Combined L-charts and Bar charts - four fixed periods
    combined_periods = [
        ("Past_since_2016", datetime(2016, 1, 1), "Since_2016-01-01"),
        ("Since_2020-01-01", datetime(2020, 1, 1), "Since_2020-01-01"),
        ("Since_2023-01-01", datetime(2023, 1, 1), "Since_2023-01-01"),
        ("Past_since_this_year", datetime(2025, 1, 1), "Since_this_year")
    ]
    
    for _, start_date, title_suffix in combined_periods:
        data = df.loc[start_date:current_date]
        title = f"All Funds {title_suffix} to {current_date_str}"
        fig = create_l_chart(data, ['Fund_A', 'Fund_B', 'Fund_C', 'Fund_D'], title, start_date, current_date, is_combined=True)
        filename = os.path.join(OUTPUT_FOLDER, f"Combined_All_Funds_{title_suffix}_to_{current_date_str}.html")
        fig.write_html(filename, include_plotlyjs='cdn', auto_open=False)
        print(f"Chart saved to {filename}")
    
    for _, start_date, title_suffix in combined_periods:
        data = df.loc[start_date:current_date]
        pct_changes = {}
        for fund in funds:
            fund_col = fund_map[fund]
            pct_changes[fund_col] = calculate_pct_change(data[fund_col].iloc[0], data[fund_col].iloc[-1])
        title = f"Bar Chart % Change All Funds {title_suffix} to {current_date_str}"
        fig = create_b_chart(pct_changes, title)
        filename = os.path.join(OUTPUT_FOLDER, f"B_chart_All_Funds_{title_suffix}_to_{current_date_str}.html")
        fig.write_html(filename, include_plotlyjs='cdn', auto_open=False)
        print(f"Chart saved to {filename}")

def illustrate_b_return():
    current_date = datetime(2025, 12, 31)
    current_date_str = "2025-12-31"
    choices = ["Past_since_2016", "Past_since_this_year", "Past_36_months", "Past_60_months"]
    funds = ["A", "B", "C", "D"]
    
    for choice in choices:
        start_date = get_start_date(current_date, choice)
        data = df.loc[start_date:current_date]
        for fund in funds:
            fund_col = fund_map[fund]
            title = f"{fund_col} Illustrate_B {choice} to {current_date_str}"
            fig = create_l_chart(data, [fund_col], title, start_date, current_date)
            filename = os.path.join(OUTPUT_FOLDER, f"{fund_col}_Illustrate_B_{choice}_to_{current_date_str}.html")
            fig.write_html(filename, include_plotlyjs='cdn', auto_open=False)
            print(f"Chart saved to {filename}")
    
    for choice in choices:
        start_date = get_start_date(current_date, choice)
        data = df.loc[start_date:current_date]
        title = f"All Funds Illustrate_B {choice} to {current_date_str}"
        fig = create_l_chart(data, ['Fund_A', 'Fund_B', 'Fund_C', 'Fund_D'], title, start_date, current_date, is_combined=True)
        filename = os.path.join(OUTPUT_FOLDER, f"Combined_Illustrate_B_{choice}_to_{current_date_str}.html")
        fig.write_html(filename, include_plotlyjs='cdn', auto_open=False)
        print(f"Chart saved to {filename}")

# ───────────────────────────────────────────────────────────────
# MAIN INTERACTIVE PROGRAM
# ───────────────────────────────────────────────────────────────

print("Welcome to Fund Chart Generator")
action = input("Please choose your action: “Your_return” or “Past_return”, “Illustrate_return” or “Illustrate_B_return”: ").strip()

if action == "Your_return":
    fund = input("Please choose a fund: A,B,C or D: ").strip()
    start_date = input("Please input a start_date (YYYY-MM-DD): ").strip()
    current_date = input("Please input a current_date (YYYY-MM-DD): ").strip()
    your_return(fund, start_date, current_date)
elif action == "Past_return":
    fund = input("Please choose a fund: A,B,C or D: ").strip()
    end_date = input("Please input an end_date (YYYY-MM-DD): ").strip()
    choice = input("Please input one of: “Past_3_months”, “Past_12_months”, “Past_36_months”, “Past_60_months”, “Past_since_2016”, “Past_since_this_year”: ").strip()
    past_return(fund, end_date, choice)
elif action == "Illustrate_return":
    illustrate_return()
elif action == "Illustrate_B_return":
    illustrate_b_return()
else:
    print("Invalid action")