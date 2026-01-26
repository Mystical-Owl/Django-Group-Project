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
    # Updated path to load from default_data folder (assuming script runs from project root)
    csv_path = os.path.join('default_data', 'funds_daily_2015_to_2036.csv')
    df = pd.read_csv(csv_path)
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
# FUND NAME MAPPING
# ───────────────────────────────────────────────────────────────

short_names = {
    'Fund_A': 'Fund A',
    'Fund_B': 'Fund B',
    'Fund_C': 'Fund C',
    'Fund_D': 'Fund D'
}

long_names = {
    'Fund_A': 'Conviction Growth Fund (Fund A)',
    'Fund_B': 'Diversified Assets Fund (Fund B)',
    'Fund_C': 'Balanced Horizon Fund (Fund C)',
    'Fund_D': 'Money Market Fund (Fund D)'
}

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
        return datetime(current_date.year - 1, 12, 31)
    else:
        raise ValueError("Invalid choice for start_date")

def create_l_chart(data, fund_cols, title, start_date, current_date, is_combined=False):
    fig = go.Figure()
    
    pct_text = ''
    
    if is_combined:
        for col in fund_cols:
            short_name = short_names.get(col, col)
            fig.add_trace(go.Scatter(
                x=data.index, 
                y=data[col], 
                mode='lines', 
                name=short_name
            ))
        
        pct_text = '<br>'.join([f"{short_names.get(col, col)}: {calculate_pct_change(data[col].iloc[0], data[col].iloc[-1]):.2f}%" for col in fund_cols])
        
        legend_text = "<b>Fund Mapping:</b><br>" + "<br>".join([f"{long_names[col]}" for col in fund_cols])
        
        fig.update_layout(
            title=title,
            xaxis_title='Year',
            yaxis_title='Value',
            yaxis=dict(range=[0, None]),
            legend=dict(x=0, y=1.1, orientation='h')
        )
        
        fig.add_annotation(
            x=0.02, y=0.95,
            text=legend_text,
            showarrow=False,
            xref='paper', yref='paper',
            align='left',
            bgcolor='rgba(255,255,255,0.8)',
            bordercolor='black',
            borderwidth=1,
            font=dict(size=11)
        )
    else:
        col = fund_cols[0]
        long_name = long_names.get(col, col)
        fig.add_trace(go.Scatter(x=data.index, y=data[col], mode='lines', name=long_name))
        pct_change = calculate_pct_change(data[col].iloc[0], data[col].iloc[-1])
        pct_text = f"Percentage Change: {pct_change:.2f}%"
        
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
    
    fig.update_layout(width=900, height=600, margin=dict(l=220, r=220))
    
    return fig

def create_b_chart(pct_changes, title):
    renamed_changes = {short_names.get(k, k): v for k, v in pct_changes.items()}
    bar_df = pd.DataFrame({'Fund': list(renamed_changes.keys()), 'Percentage Change': list(renamed_changes.values())})
    fig = px.bar(bar_df, x='Fund', y='Percentage Change', title=title)
    fig.update_yaxes(range=[0, None])
    return fig

# ───────────────────────────────────────────────────────────────
# ACTION: YOUR RETURN
# ───────────────────────────────────────────────────────────────

def your_return(fund_input, start_date_str, current_date_str):
    start_date = pd.to_datetime(start_date_str)
    current_date = pd.to_datetime(current_date_str)
    
    if fund_input.upper() == "ALL":
        fund_cols = ['Fund_A', 'Fund_B', 'Fund_C', 'Fund_D']
        title = f"All Funds Value Change from {start_date_str} to {current_date_str}"
        fig = create_l_chart(df.loc[start_date:current_date], fund_cols, title, start_date, current_date, is_combined=True)
        filename = os.path.join(OUTPUT_FOLDER, f"All_Funds_Your_return_{start_date_str}_to_{current_date_str}.html")
    else:
        fund_col = fund_map[fund_input.upper()]
        display_name = long_names[fund_col]
        data = df.loc[start_date:current_date, [fund_col]]
        title = f"{display_name} Value Change from {start_date_str} to {current_date_str}"
        fig = create_l_chart(data, [fund_col], title, start_date, current_date)
        filename = os.path.join(OUTPUT_FOLDER, f"{fund_input.upper()}_Your_return_{start_date_str}_to_{current_date_str}.html")
    
    fig.write_html(filename, include_plotlyjs='cdn', auto_open=False)
    print(f"Chart saved to {filename}")

# ───────────────────────────────────────────────────────────────
# ACTION: PAST RETURN
# ───────────────────────────────────────────────────────────────

def past_return(fund_input, current_date_str, choice):
    current_date = pd.to_datetime(current_date_str)
    start_date = get_start_date(current_date, choice)
    
    if fund_input.upper() == "ALL":
        fund_cols = ['Fund_A', 'Fund_B', 'Fund_C', 'Fund_D']
        title = f"All Funds {choice} to {current_date_str}"
        fig = create_l_chart(df.loc[start_date:current_date], fund_cols, title, start_date, current_date, is_combined=True)
        filename = os.path.join(OUTPUT_FOLDER, f"All_Funds_{choice}_to_{current_date_str}.html")
    else:
        fund_col = fund_map[fund_input.upper()]
        display_name = long_names[fund_col]
        data = df.loc[start_date:current_date, [fund_col]]
        title = f"{display_name} {choice} to {current_date_str}"
        fig = create_l_chart(data, [fund_col], title, start_date, current_date)
        filename = os.path.join(OUTPUT_FOLDER, f"{fund_input.upper()}_{choice}_to_{current_date_str}.html")
    
    fig.write_html(filename, include_plotlyjs='cdn', auto_open=False)
    print(f"Chart saved to {filename}")

# ───────────────────────────────────────────────────────────────
# ACTION: ILLUSTRATE RETURN
# ───────────────────────────────────────────────────────────────

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
            display_name = long_names[fund_col]
            title = f"{display_name} {choice} to {current_date_str}"
            fig = create_l_chart(data, [fund_col], title, start_date, current_date)
            filename = os.path.join(OUTPUT_FOLDER, f"{fund}_{choice}_to_{current_date_str}.html")
            fig.write_html(filename, include_plotlyjs='cdn', auto_open=False)
            print(f"Chart saved to {filename}")
    
    # Combined L-charts and Bar charts - four fixed periods with Dec 31 start
    combined_periods = [
        ("Past_since_2016", datetime(2015, 12, 31), "Since_2016"),
        ("Since_2020", datetime(2019, 12, 31), "Since_2020"),
        ("Since_2023", datetime(2022, 12, 31), "Since_2023"),
        ("Past_since_this_year", datetime(2024, 12, 31), "Since_this_year")
    ]
    
    for _, start_date, title_suffix in combined_periods:
        data = df.loc[start_date:current_date]
        title = f"All Funds {title_suffix} to {current_date_str}"
        fig = create_l_chart(data, ['Fund_A', 'Fund_B', 'Fund_C', 'Fund_D'], title, start_date, current_date, is_combined=True)
        filename = os.path.join(OUTPUT_FOLDER, f"Combined_All_Funds_{title_suffix}_to_{current_date_str}.html")
        fig.write_html(filename, include_plotlyjs='cdn', auto_open=False)
        print(f"Chart saved to {filename}")
    
    # Bar charts
    for _, start_date, title_suffix in combined_periods:
        data = df.loc[start_date:current_date]
        pct_changes = {}
        for fund in funds:
            fund_col = fund_map[fund]
            pct_changes[short_names[fund_col]] = calculate_pct_change(data[fund_col].iloc[0], data[fund_col].iloc[-1])
        title = f"Bar Chart % Change All Funds {title_suffix} to {current_date_str}"
        fig = create_b_chart(pct_changes, title)
        filename = os.path.join(OUTPUT_FOLDER, f"Bar_All_Funds_{title_suffix}_to_{current_date_str}.html")
        fig.write_html(filename, include_plotlyjs='cdn', auto_open=False)
        print(f"Chart saved to {filename}")

# ───────────────────────────────────────────────────────────────
# PORTFOLIO CALC HELPER
# ───────────────────────────────────────────────────────────────

def calculate_portfolio_value(start_date, current_date, invested_amount, weights):
    start_row = df.loc[start_date]
    current_row = df.loc[current_date]
    port_start = invested_amount
    port_current = 0
    current_holdings = {}
    for fund_col, weight in weights.items():
        if weight > 0:
            growth = current_row[fund_col] / start_row[fund_col] if start_row[fund_col] != 0 else 1.0
            holding = invested_amount * weight * growth
            current_holdings[fund_col] = holding
            port_current += holding
    gain = port_current - port_start
    return_pct = (gain / port_start * 100) if port_start != 0 else 0
    current_alloc_pct = {fund: (val / port_current * 100) if port_current != 0 else 0 for fund, val in current_holdings.items()}
    return port_start, port_current, gain, return_pct, current_holdings, current_alloc_pct

# ───────────────────────────────────────────────────────────────
# ACTION: YOUR PORTFOLIO RETURN (latest version with UI fix)
# ───────────────────────────────────────────────────────────────

def your_portfolio_return():
    current_date_str = input("Please input a current_date (YYYY-MM-DD): ").strip()
    try:
        current_date = pd.to_datetime(current_date_str)
        if current_date < pd.to_datetime("2015-12-31"):
            print("Warning: Current date before data start → clamped to 2015-12-31")
            current_date = pd.to_datetime("2015-12-31")
            current_date_str = "2015-12-31"
        elif current_date > pd.to_datetime("2036-12-31"):
            print("Warning: Current date after data end → clamped to 2036-12-31")
            current_date = pd.to_datetime("2036-12-31")
            current_date_str = "2036-12-31"
    except:
        print("Invalid current_date format. Using 2025-12-31 as fallback.")
        current_date = pd.to_datetime("2025-12-31")
        current_date_str = "2025-12-31"

    investor_input = input("Please input investor_data (invested_amount, pct_A, pct_B, pct_C, pct_D, start_date): ").strip()
    
    try:
        parts = [x.strip() for x in investor_input.split(',')]
        if len(parts) != 6:
            raise ValueError("Exactly 6 values required (comma separated)")
        
        invested_amount = float(parts[0])
        pct_A = int(parts[1])
        pct_B = int(parts[2])
        pct_C = int(parts[3])
        pct_D = int(parts[4])
        start_date_str = parts[5]
        
        pct_sum = pct_A + pct_B + pct_C + pct_D
        if pct_sum != 100:
            raise ValueError(f"Percentages must sum to 100% (got {pct_sum})")
        
        start_date = pd.to_datetime(start_date_str)
        if start_date < pd.to_datetime("2015-12-31"):
            print("Warning: Start date before data start → clamped to 2015-12-31")
            start_date = pd.to_datetime("2015-12-31")
            start_date_str = "2015-12-31"
        elif start_date > current_date:
            raise ValueError("Start date cannot be after current date")
        
        weights = {
            'Fund_A': pct_A / 100.0,
            'Fund_B': pct_B / 100.0,
            'Fund_C': pct_C / 100.0,
            'Fund_D': pct_D / 100.0
        }
        
        active_funds = [f for f, w in weights.items() if w > 0]
        
        port_start, port_current, gain, return_pct, current_holdings, current_alloc_pct = calculate_portfolio_value(
            start_date, current_date, invested_amount, weights
        )
        
        print(f"\nPortfolio Summary for dummy_investor_1")
        print(f"  Invested: ${invested_amount:,.2f}")
        print(f"  Start date: {start_date_str} → Value: ${port_start:,.2f}")
        print(f"  Current date: {current_date_str} → Value: ${port_current:,.2f}")
        print(f"  Gain/Loss: ${gain:,.2f} ({return_pct:+.2f}%)")
        
        # Portfolio value chart
        dates = df.loc[start_date:current_date].index
        portfolio_values = []
        
        for dt in dates:
            row = df.loc[dt]
            port_val = invested_amount
            for fund_col, weight in weights.items():
                growth = row[fund_col] / df.loc[start_date, fund_col] if df.loc[start_date, fund_col] != 0 else 1.0
                port_val += (invested_amount * weight) * (growth - 1)
            portfolio_values.append(port_val)
        
        fig_port = go.Figure()
        
        fig_port.add_trace(go.Scatter(
            x=dates, y=portfolio_values, 
            name="Your Portfolio", 
            line=dict(width=3, color='royalblue')
        ))
        
        fund_colors = {
            'Fund_A': '#1f77b4',
            'Fund_B': '#2ca02c',
            'Fund_C': '#ff7f0e',
            'Fund_D': '#9467bd'
        }
        
        fund_traces = []
        for fund_col in active_funds:
            fund_values = []
            for dt in dates:
                start_val = df.loc[start_date, fund_col]
                curr_val = df.loc[dt, fund_col]
                growth = curr_val / start_val if start_val != 0 else 1.0
                fund_values.append(invested_amount * weights[fund_col] * growth)
            
            trace = go.Scatter(
                x=dates, y=fund_values,
                name=short_names[fund_col],
                line=dict(dash='dash', color=fund_colors[fund_col]),
                visible=False
            )
            fig_port.add_trace(trace)
            fund_traces.append(trace)
        
        min_port = min(portfolio_values)
        y_min = min(0, min_port * 0.95) if min_port < invested_amount else 0
        
        fig_port.update_layout(
            title=f"Your Portfolio Value Change from {start_date_str} to {current_date_str}",
            xaxis_title="Date",
            yaxis_title="Portfolio Value (USD)",
            yaxis=dict(range=[y_min, max(portfolio_values) * 1.05]),
            legend=dict(x=0.0, y=1.05, orientation='h', xanchor='left'),  # Lowered y, anchored left
            margin=dict(l=250, r=200, t=150, b=50),  # Increased top margin for breathing room
            updatemenus=[
                dict(
                    type="buttons",
                    direction="left",
                    x=1.0,  # Moved to right
                    xanchor='right',  # Anchor to right edge
                    y=1.25,
                    pad=dict(t=50),
                    showactive=True,
                    buttons=[
                        dict(
                            label="Hide Funds",
                            method="update",
                            args=[{"visible": [True] + [False] * len(active_funds)}]
                        ),
                        dict(
                            label="Show Funds",
                            method="update",
                            args=[{"visible": [True] * (1 + len(active_funds))}]
                        )
                    ]
                )
            ]
        )
        
        fig_port.add_annotation(
            x=1.05, y=0.5,
            text=f"Current Value: ${port_current:,.2f}<br>Return: {return_pct:+.2f}%",
            showarrow=False,
            xref='paper', yref='paper',
            align='left',
            font=dict(size=12)
        )
        
        filename_port = os.path.join(OUTPUT_FOLDER, f"Your_Portfolio_Chart_dummy_investor_1_to_{current_date_str}.html")
        fig_port.write_html(filename_port, include_plotlyjs='cdn', auto_open=False)
        print(f"Portfolio chart saved to {filename_port}")
        
        # Pie chart
        pie_labels = []
        pie_values = []
        pie_hover = []
        for fund_col in fund_map.values():
            if weights[fund_col] > 0:
                current_value = current_holdings[fund_col]
                short_label = short_names[fund_col]
                long_label = long_names[fund_col]
                pie_labels.append(short_label)
                pie_values.append(current_value)
                pie_hover.append(f"{long_label}<br>${current_value:,.2f}<br>{current_alloc_pct[fund_col]:.2f}%")
        
        fig_pie = px.pie(
            names=pie_labels,
            values=pie_values,
            title="Current Portfolio Holdings by Value"
        )
        fig_pie.update_traces(
            textinfo='label+percent',
            textposition='inside',
            hovertemplate="%{customdata}<extra></extra>",
            customdata=pie_hover
        )
        
        # Right-side box: Current breakdown
        current_text = "<b>Current Portfolio Breakdown:</b><br>"
        current_text += f"Total Portfolio Value: ${port_current:,.2f}<br><br>"
        for fund_col in fund_map.values():
            if weights[fund_col] > 0:
                current_value = current_holdings[fund_col]
                alloc_pct = current_alloc_pct[fund_col]
                current_text += f"{long_names[fund_col]}:<br>  Value: ${current_value:,.2f}<br>  Allocation: {alloc_pct:.2f}%<br><br>"
        
        fig_pie.add_annotation(
            x=1.02, y=0.5,
            text=current_text,
            showarrow=False,
            xref='paper', yref='paper',
            align='left',
            bgcolor='rgba(255,255,255,0.8)',
            bordercolor='black',
            borderwidth=1,
            font=dict(size=11)
        )
        
        # Left-side box: Initial investment & allocation
        initial_text = "<b>Initial Investment:</b><br>"
        initial_text += f"Total Invested: ${invested_amount:,.2f}<br><br>"
        initial_text += "<b>Initial Allocation %:</b><br>"
        for fund_col, w in weights.items():
            if w > 0:
                initial_text += f"{short_names[fund_col]}: {w*100:.0f}%<br>"
        
        fig_pie.add_annotation(
            x=0.02, y=0.95,
            text=initial_text,
            showarrow=False,
            xref='paper', yref='paper',
            align='left',
            bgcolor='rgba(240,240,255,0.9)',
            bordercolor='navy',
            borderwidth=1,
            font=dict(size=11)
        )
        
        filename_pie = os.path.join(OUTPUT_FOLDER, f"Your_Portfolio_Pie_dummy_investor_1_to_{current_date_str}.html")
        fig_pie.write_html(filename_pie, include_plotlyjs='cdn', auto_open=False)
        print(f"Current holdings pie chart saved to {filename_pie}")
        
    except ValueError as ve:
        print(f"Input error: {ve}")
    except Exception as e:
        print(f"Unexpected error: {e}")

# ───────────────────────────────────────────────────────────────
# MAIN INTERACTIVE PROGRAM
# ───────────────────────────────────────────────────────────────

print("Welcome to Fund Chart Generator")
action = input("Please choose your action: “Your_return” or “Past_return”, “Illustrate_return” or “Your_portfolio_return”: ").strip()

if action == "Your_return":
    fund = input("Please choose a fund (A,B,C,D or All): ").strip()
    start_date = input("Please input a start_date (YYYY-MM-DD): ").strip()
    current_date = input("Please input a current_date (YYYY-MM-DD): ").strip()
    your_return(fund, start_date, current_date)
elif action == "Past_return":
    fund = input("Please choose a fund (A,B,C,D or All): ").strip()
    current_date = input("Please input a current_date (YYYY-MM-DD): ").strip()
    choice = input("Please input one of: “Past_3_months”, “Past_12_months”, “Past_36_months”, “Past_60_months”, “Past_since_2016”, “Past_since_this_year”: ").strip()
    past_return(fund, current_date, choice)
elif action == "Illustrate_return":
    illustrate_return()
elif action == "Your_portfolio_return":
    your_portfolio_return()
else:
    print("Invalid action")