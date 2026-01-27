from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django import forms
from datetime import datetime, timedelta
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
import os
from django.conf import settings
from django.urls import reverse
from django.http import HttpResponse

# Import fund briefs
from .fundbriefing import fund_briefs

# Fund mappings
short_names = {
    'Fund_A': 'Fund A',
    'Fund_B': 'Fund B',
    'Fund_C': 'Fund C',
    'Fund_D': 'Fund D'
}

long_names = {
    'Fund_A': 'Conviction Growth Fund (A)',
    'Fund_B': 'Diversified Assets Fund (B)',
    'Fund_C': 'Balanced Horizon Fund (C)',
    'Fund_D': 'Money Market Fund (D)'
}

fund_map = {'A': 'Fund_A', 'B': 'Fund_B', 'C': 'Fund_C', 'D': 'Fund_D'}

# Lazy load function for fund data
def get_fund_data():
    csv_path = os.path.join(settings.BASE_DIR, 'default_data', 'funds_daily_2015_to_2036.csv')
    df = pd.read_csv(csv_path)
    df['Date'] = pd.to_datetime(df['Date'])
    df = df.set_index('Date').sort_index()
    return df

# Helper functions
def calculate_pct_change(start_val, end_val):
    return ((end_val - start_val) / start_val) * 100 if start_val != 0 else 0

def create_l_chart(data, fund_cols, title, start_date, current_date, is_combined=False):
    fig = go.Figure()
    pct_text = ''
    if is_combined:
        for col in fund_cols:
            short_name = short_names.get(col, col)
            fig.add_trace(go.Scatter(x=data.index, y=data[col], mode='lines', name=short_name))
        pct_text = '<br>'.join([f"{short_names.get(col, col)}: {calculate_pct_change(data[col].iloc[0], data[col].iloc[-1]):.2f}%" for col in fund_cols])
        legend_text = "<b>Fund Mapping:</b><br>" + "<br>".join([f"{long_names[col]}" for col in fund_cols])
        fig.update_layout(title=title, xaxis_title='Year', yaxis_title='Value', yaxis=dict(range=[0, None]), legend=dict(x=0, y=1.1, orientation='h'))
        fig.add_annotation(x=0.02, y=0.95, text=legend_text, showarrow=False, xref='paper', yref='paper', align='left', bgcolor='rgba(255,255,255,0.8)', bordercolor='black', borderwidth=1, font=dict(size=11))
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
            fig.update_layout(title=title, xaxis_title='Year', yaxis_title='Value', yaxis=dict(range=[y_min, y_max]))
        else:
            fig.update_layout(title=title, xaxis_title='Year', yaxis_title='Value', yaxis=dict(range=[0, None]))
    days_diff = (current_date - start_date).days
    if days_diff > 365:
        fig.update_xaxes(dtick='M12', tickformat='%Y', showline=True, linewidth=1.5, linecolor='black', gridcolor='lightgray')
    else:
        fig.update_xaxes(dtick='M3', tickformat='%Y %b', showline=True, linewidth=1.5, linecolor='black', gridcolor='lightgray')
    fig.update_xaxes(zeroline=False)
    fig.add_annotation(x=1.05, y=0.5, text=pct_text, showarrow=False, xref='paper', yref='paper', align='left', font=dict(size=12))
    fig.update_layout(width=900, height=600, margin=dict(l=220, r=220))
    return fig

def calculate_portfolio_value(df, start_date, current_date, invested_amount, weights):
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

# Portfolio form
class PortfolioForm(forms.Form):
    current_date = forms.DateField(initial=datetime(2026, 1, 28))
    invested_amount = forms.FloatField(initial=100000)
    pct_A = forms.IntegerField(initial=35, min_value=0, max_value=100)
    pct_B = forms.IntegerField(initial=25, min_value=0, max_value=100)
    pct_C = forms.IntegerField(initial=20, min_value=0, max_value=100)
    pct_D = forms.IntegerField(initial=20, min_value=0, max_value=100)
    start_date = forms.DateField(initial=datetime(2021, 11, 11))

    def clean(self):
        cleaned_data = super().clean()
        pct_sum = cleaned_data.get('pct_A', 0) + cleaned_data.get('pct_B', 0) + cleaned_data.get('pct_C', 0) + cleaned_data.get('pct_D', 0)
        if pct_sum != 100:
            raise forms.ValidationError("Percentages must sum to 100%.")
        return cleaned_data

# Back URL helper
def get_back_url(request):
    referer = request.META.get('HTTP_REFERER')
    if referer and 'invest_reviews' in referer:
        return referer
    return reverse('invest_reviews:main')  # This will now work after app_name is set


# -- Main page of invest_reviews ---

@login_required
def invest_reviews_view(request):
    chart_folder = 'FundCharts_Store'
    main_chart = f"{chart_folder}/Combined_All_Funds_Since_this_year_to_2025-12-31.html"
    context = {
        'main_chart': main_chart,
        'fund_briefs': fund_briefs,
        'back_url': request.META.get('HTTP_REFERER','/'),
    }
    return render(request, 'invest_reviews/invest_reviews.html', context)

# -- Your Portfolio Output View --

@login_required
def portfolio_view(request):
    df = get_fund_data()
    
    if request.method == 'POST':
        form = PortfolioForm(request.POST)
        if form.is_valid():
            current_date = pd.to_datetime(form.cleaned_data['current_date'])
            invested_amount = form.cleaned_data['invested_amount']
            weights = {
                'Fund_A': form.cleaned_data['pct_A'] / 100.0,
                'Fund_B': form.cleaned_data['pct_B'] / 100.0,
                'Fund_C': form.cleaned_data['pct_C'] / 100.0,
                'Fund_D': form.cleaned_data['pct_D'] / 100.0
            }
            requested_start_date = form.cleaned_data['start_date']
            start_date_dt = pd.to_datetime(requested_start_date)
            
            # Debug prints
            print("Index sample:", df.index[:5])
            print("Requested start (converted):", start_date_dt)
            print("In index (start)?", start_date_dt in df.index)
            print("Requested current (converted):", current_date)
            print("In index (current)?", current_date in df.index)
            
            # Start date handling
            if start_date_dt not in df.index:
                available_start = df.index[df.index >= start_date_dt]
                if available_start.empty:
                    messages.error(request, "No data available after requested start date.")
                    return render(request, 'invest_reviews/portfolio.html', {'form': form})
                start_date = available_start.min()
                messages.warning(request, f"Using nearest start date: {start_date.date()}")
            else:
                start_date = start_date_dt
            
            # Current date handling
            if current_date not in df.index:
                available_end = df.index[df.index <= current_date]
                if available_end.empty:
                    messages.error(request, "No data available before requested current date.")
                    return render(request, 'invest_reviews/portfolio.html', {'form': form})
                current_date = available_end.max()
                messages.warning(request, f"Using nearest current date: {current_date.date()}")
            else:
                current_date = current_date
            
            start_date_str = start_date.strftime('%Y-%m-%d')
            current_date_str = current_date.strftime('%Y-%m-%d')
            
            active_funds = [f for f, w in weights.items() if w > 0]
            port_start, port_current, gain, return_pct, current_holdings, current_alloc_pct = calculate_portfolio_value(
                df, start_date, current_date, invested_amount, weights
            )
            
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
            fig_port.add_trace(go.Scatter(x=dates, y=portfolio_values, name="Your Portfolio", line=dict(width=3, color='royalblue')))
            
            fund_colors = {'Fund_A': '#1f77b4', 'Fund_B': '#2ca02c', 'Fund_C': '#ff7f0e', 'Fund_D': '#9467bd'}
            for fund_col in active_funds:
                fund_values = []
                for dt in dates:
                    start_val = df.loc[start_date, fund_col]
                    curr_val = df.loc[dt, fund_col]
                    growth = curr_val / start_val if start_val != 0 else 1.0
                    fund_values.append(invested_amount * weights[fund_col] * growth)
                fig_port.add_trace(go.Scatter(x=dates, y=fund_values, name=short_names[fund_col], line=dict(dash='dash', color=fund_colors[fund_col]), visible=False))
            
            min_port = min(portfolio_values)
            y_min = min(0, min_port * 0.95) if min_port < invested_amount else 0
            fig_port.update_layout(
                title=f"Your Portfolio Value Change from {start_date_str} to {current_date_str}",
                xaxis_title="Date",
                yaxis_title="Portfolio Value (USD)",
                yaxis=dict(range=[y_min, max(portfolio_values) * 1.05]),
                legend=dict(x=0, y=1.1, orientation='h'),
                margin=dict(l=250, r=200, t=120),
                updatemenus=[dict(type="buttons", direction="left", x=0.1, y=1.25, pad=dict(t=50), showactive=True,
                                  buttons=[dict(label="Hide Funds", method="update", args=[{"visible": [True] + [False] * len(active_funds)}]),
                                           dict(label="Show Funds", method="update", args=[{"visible": [True] * (1 + len(active_funds))}])])]
            )
            fig_port.add_annotation(x=1.05, y=0.5, text=f"Current Value: ${port_current:,.2f}<br>Return: {return_pct:+.2f}%",
                                    showarrow=False, xref='paper', yref='paper', align='left', font=dict(size=12))
            
            port_div = fig_port.to_html(full_html=False, include_plotlyjs='cdn')
            
            pie_labels = [short_names[fund_col] for fund_col in fund_map.values() if weights[fund_col] > 0]
            pie_values = [current_holdings[fund_col] for fund_col in fund_map.values() if weights[fund_col] > 0]
            pie_hover = [f"{long_names[fund_col]}<br>${current_holdings[fund_col]:,.2f}<br>{current_alloc_pct[fund_col]:.2f}%" for fund_col in fund_map.values() if weights[fund_col] > 0]
            
            fig_pie = px.pie(names=pie_labels, values=pie_values, title="Current Portfolio Holdings Value")
            fig_pie.update_traces(textinfo='label+percent', textposition='inside', hovertemplate="%{customdata}<extra></extra>", customdata=pie_hover)
            
            pie_div = fig_pie.to_html(full_html=False, include_plotlyjs='cdn')
            
            return render(request, 'invest_reviews/portfolio.html', {'form': form, 'port_div': port_div, 'pie_div': pie_div, 'back_url': request.META.get('HTTP_REFERER', reverse('invest_reviews:main')),})
    else:
        form = PortfolioForm()
    
    return render(request, 'invest_reviews/portfolio.html', {'form': form})


# -- Fund Description Views --
@login_required
def fund_descriptions_view(request):
    return render(request, 'invest_reviews/fund_descriptions.html', {
        'fund_briefs': fund_briefs,
        'back_url': get_back_url(request),
    })

@login_required
def fund_detail_view(request, fund_key):
    if fund_key not in fund_briefs:
        return redirect('invest_reviews:fund_descriptions')
    
    brief = fund_briefs[fund_key]
    chart_file = f"{fund_key}_Since_2016_to_2025-12-31.html"  # correct filename
    
    context = {
        'fund_key': fund_key,
        'short': brief['short'],
        'long': brief['long'],
        'chart_path': f"FundCharts_Store/{chart_file}",
        'back_url': get_back_url(request),
    }
    return render(request, 'invest_reviews/fund_detail.html', context)

# -- Performance Since Founded Views --
@login_required
def performance_since_founded_view(request):
    combined_chart = "FundCharts_Store/Combined_All_Funds_Since_2016_to_2025-12-31.html"
    
    context = {
        'combined_chart': combined_chart,
        'back_url': get_back_url(request),
    }
    return render(request, 'invest_reviews/performance_since_founded.html', context)

@login_required
def fund_individual_since_founded_view(request, fund_key):
    if fund_key not in ['A', 'B', 'C', 'D']:
        return redirect('invest_reviews:performance_since_founded')
    
    chart_file = f"{fund_key}_Since_2016_to_2025-12-31.html"  # correct filename
    
    context = {
        'fund_key': fund_key,
        'chart_path': f"FundCharts_Store/{chart_file}",
        'back_url': get_back_url(request),
    }
    return render(request, 'invest_reviews/fund_individual.html', context)

# -- This Year Performance Views --
@login_required
def this_year_performance_view(request):
    combined_chart = "FundCharts_Store/Combined_All_Funds_Since_this_year_to_2025-12-31.html"
    
    context = {
        'combined_chart': combined_chart,
        'back_url': get_back_url(request),
    }
    return render(request, 'invest_reviews/this_year_performance.html', context)

@login_required
def fund_individual_this_year_view(request, fund_key):
    if fund_key not in ['A', 'B', 'C', 'D']:
        return redirect('invest_reviews:this_year_performance')
    
    chart_file = f"{fund_key}_Since_this_year_to_2025-12-31.html"
    
    context = {
        'fund_key': fund_key,
        'chart_path': f"FundCharts_Store/{chart_file}",
        'back_url': get_back_url(request),
    }
    return render(request, 'invest_reviews/fund_individual_this_year.html', context)

### what does this do? (George)
# print("DEBUG: fund_individual_this_year_view is defined")  
# # add this line right after the function definition



#  -- More to See View --
@login_required
def more_to_see_view(request):
    return render(request, 'invest_reviews/more_to_see.html', {
        'back_url': get_back_url(request),
    })



@login_required
def test_this_year_fund(request, fund_key):
    return HttpResponse(f"Test OK! You clicked Fund {fund_key}")