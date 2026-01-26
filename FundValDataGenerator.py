import numpy as np
import pandas as pd
from datetime import datetime
import os  # Added for path joining

# ───────────────────────────────────────────────────────────────
# CONFIGURATION - using original targets
# ───────────────────────────────────────────────────────────────

START_DATE = datetime(2015, 12, 31)
END_DATE   = datetime(2036, 12, 31)
BASE_VALUE = 100.00

CHANGE_DATE = datetime(2026, 1, 1)

fund_configs = {
    'A': {
        '2016-2025': {'return': 0.15, 'vol': 0.18},
        '2026-2036': {'return': 0.10, 'vol': 0.11}
    },
    'B': {
        '2016-2025': {'return': 0.10, 'vol': 0.12},
        '2026-2036': {'return': 0.08, 'vol': 0.10}
    },
    'C': {
        '2016-2025': {'return': 0.18, 'vol': 0.22},
        '2026-2036': {'return': 0.15, 'vol': 0.18}
    },
    'D': {
        'whole_period': {'return': 0.025, 'vol': 0.005}
    }
}

target_cagrs = {
    'A': {'2016-2025': 0.15, '2026-2036': 0.10},
    'B': {'2016-2025': 0.10, '2026-2036': 0.08},
    'C': {'2016-2025': 0.18, '2026-2036': 0.15},
    'D': {'whole_period': 0.025}
}

# ───────────────────────────────────────────────────────────────
# Generate daily prices with best seed search (vectorized for speed)
# ───────────────────────────────────────────────────────────────

dates = pd.date_range(START_DATE, END_DATE, freq='D')
dt_2025 = datetime(2025, 12, 31)
num_days = len(dates)

def cagr(start, end, years):
    if start <= 0 or end <= 0:
        return 0.00
    return ((end / start) ** (1 / years) - 1) * 100

def generate_prices(seed):
    np.random.seed(seed)
    prices = {}
    for fund_name, config in fund_configs.items():
        if fund_name == 'D':
            r = config['whole_period']['return']
            v = config['whole_period']['vol']
            mu_annual = np.log(1 + r) + 0.5 * v**2
            mu_daily = mu_annual / 365
            sigma_daily = v / np.sqrt(365)
            
            # Vectorized: Generate all daily log returns at once
            daily_log_rets = np.random.normal(mu_daily, sigma_daily, num_days - 1)
            cum_returns = np.exp(np.cumsum(daily_log_rets))
            price_series = np.concatenate(([BASE_VALUE], BASE_VALUE * cum_returns))
        else:
            regimes = {}
            for period, params in config.items():
                r = params['return']
                v = params['vol']
                mu_annual = np.log(1 + r) + 0.5 * v**2
                regimes[period] = {
                    'mu_daily': mu_annual / 365,
                    'sigma_daily': v / np.sqrt(365)
                }
            
            # Split into periods for vectorization
            pre_change_mask = dates < CHANGE_DATE
            pre_days = np.sum(pre_change_mask) - 1  # Exclude start date
            post_days = num_days - 1 - pre_days
            
            # Pre-2026
            mu_d_pre = regimes['2016-2025']['mu_daily']
            sigma_d_pre = regimes['2016-2025']['sigma_daily']
            daily_log_rets_pre = np.random.normal(mu_d_pre, sigma_d_pre, pre_days)
            
            # Post-2026
            mu_d_post = regimes['2026-2036']['mu_daily']
            sigma_d_post = regimes['2026-2036']['sigma_daily']
            daily_log_rets_post = np.random.normal(mu_d_post, sigma_d_post, post_days)
            
            # Combine and compute cumulative prices
            daily_log_rets = np.concatenate((daily_log_rets_pre, daily_log_rets_post))
            cum_returns = np.exp(np.cumsum(daily_log_rets))
            price_series = np.concatenate(([BASE_VALUE], BASE_VALUE * cum_returns))
        
        prices[fund_name] = pd.Series(price_series, index=dates)
    return prices

best_seed = None
min_error = float('inf')

for seed in range(10000):
    if seed % 100 == 0:  # Print progress every 100 seeds
        print(f"Progress: Testing seed {seed} / 10000 (current min_error: {min_error:.2f})")
    prices = generate_prices(seed)
    error = 0
    all_close = True
    for fund in ['A', 'B', 'C', 'D']:
        start = prices[fund].iloc[0]
        end_2025 = prices[fund].loc[dt_2025]
        end = prices[fund].iloc[-1]
        cagr1 = cagr(start, end_2025, 10)
        cagr2 = cagr(end_2025, end, 11)
        if fund == 'D':
            t1 = target_cagrs['D']['whole_period'] * 100
            t2 = t1  # Same for both periods
        else:
            t1 = target_cagrs[fund]['2016-2025'] * 100
            t2 = target_cagrs[fund]['2026-2036'] * 100
        diff1 = abs(cagr1 - t1)
        diff2 = abs(cagr2 - t2)
        error += diff1 + diff2
        if diff1 > 3 or diff2 > 3:  # 3% tolerance
            all_close = False
    if all_close and error < min_error:
        min_error = error
        best_seed = seed
    if best_seed is not None and min_error < 10:  # Stop early if good
        break

if best_seed is not None:
    print(f"Using seed {best_seed} with total error {min_error:.2f}")
    prices = generate_prices(best_seed)  # Regenerate with best seed
else:
    print("No good seed found; try larger range or higher tolerance.")
    # Optional: Exit or continue with last seed
    prices = generate_prices(seed)  # Use last as fallback

# ───────────────────────────────────────────────────────────────
# Export full daily data to CSV
# ───────────────────────────────────────────────────────────────

df_daily = pd.DataFrame({
    'Date': dates.strftime('%Y-%m-%d'),
    'Fund_A': prices['A'].round(2),
    'Fund_B': prices['B'].round(2),
    'Fund_C': prices['C'].round(2),
    'Fund_D': prices['D'].round(2)
})

# Updated export path to default_data folder (assuming script runs from project root)
export_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'default_data', 'funds_daily_2015_to_2036.csv')
df_daily.to_csv(export_path, index=False)
print(f"Full daily data exported to: {export_path}\n")

# ───────────────────────────────────────────────────────────────
# Print end values at year-end 2015, 2025, 2036
# ───────────────────────────────────────────────────────────────

print("Fund Values at Year-End:")
print("══════════════════════════════════════════════════════════════")
print(f"{'Date':<12} {'Fund A':>12} {'Fund B':>12} {'Fund C':>12} {'Fund D':>12}")
print("══════════════════════════════════════════════════════════════")

for year in [2015, 2025, 2036]:
    dt = datetime(year, 12, 31)
    date_str = dt.strftime('%Y-%m-%d')
    try:
        va = prices['A'].loc[dt]
        vb = prices['B'].loc[dt]
        vc = prices['C'].loc[dt]
        vd = prices['D'].loc[dt]
        print(f"{date_str:<12} {va:12.2f} {vb:12.2f} {vc:12.2f} {vd:12.2f}")
    except KeyError:
        print(f"{date_str:<12} {'Data not available':>48}")

print("══════════════════════════════════════════════════════════════\n")

# ───────────────────────────────────────────────────────────────
# Print CAGRs for the three requested periods
# ───────────────────────────────────────────────────────────────

print("=== CAGRs for 2016-2036 (21 years) ===")
for fund in ['A', 'B', 'C', 'D']:
    start = prices[fund].iloc[0]
    end = prices[fund].iloc[-1]
    rate = cagr(start, end, 21)
    print(f"Fund {fund}: {rate:5.2f}% (End Value: {end:,.2f})")

print("\n=== CAGRs for 2016-2025 (10 years) ===")
for fund in ['A', 'B', 'C', 'D']:
    start = prices[fund].iloc[0]
    end = prices[fund].loc[dt_2025]
    rate = cagr(start, end, 10)
    print(f"Fund {fund}: {rate:5.2f}% (End Value: {end:,.2f})")

print("\n=== CAGRs for 2026-2036 (11 years) ===")
for fund in ['A', 'B', 'C', 'D']:
    start = prices[fund].loc[dt_2025]
    end = prices[fund].iloc[-1]
    rate = cagr(start, end, 11)
    print(f"Fund {fund}: {rate:5.2f}% (End Value: {end:,.2f})")
    