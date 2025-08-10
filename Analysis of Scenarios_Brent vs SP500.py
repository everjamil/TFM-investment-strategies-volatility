# -*- coding: utf-8 -*-
"""
Created on Sun Aug 10 22:34:34 2025

@author: everl
"""

import pandas as pd
import matplotlib.pyplot as plt
from pandas.tseries.offsets import BDay
import matplotlib.ticker as mtick

#############################################################

# Global settings to improve plot readability
plt.rcParams.update({
    'font.size': 12,            # Base font size
    'axes.titlesize': 18,       # Plot title size
    'axes.labelsize': 14,       # Axis label size
    'xtick.labelsize': 14,      # X-axis tick label size
    'ytick.labelsize': 14,      # Y-axis tick label size
    'legend.fontsize': 14,      # Legend font size
    'figure.titlesize': 16,     # Figure title size
})

# Load data
excel_path = r'[PUT THE PATH OF THE SAVED FILE, THE FILE IS CALLED Data Assets_SP500, Gold, Vix, Brent and Others Indices]'
df = pd.read_excel(excel_path, parse_dates=['Date'])

# Define events
events = {
    'Global Financial Crisis (2008-2009)': pd.to_datetime('2008-09-29'),
    'European Sovereign Debt Crisis and US Downgrade (2011)': pd.to_datetime('2011-08-08'),
    'China Flash Crash and Emerging Markets Tensions (2015)': pd.to_datetime('2015-08-24'),
    'Correction due to Rate Tensions and Overvaluation (2018)': pd.to_datetime('2018-02-05'),
    'COVID-19 Pandemic (2020)': pd.to_datetime('2020-03-09'),
    'Trade War (2025)': pd.to_datetime('2025-04-04'),
}

# Days before and after event
days_before = 20
days_after = 20

def plot_cumulative_returns(df, event_date, event_name):
    colors = {
        'Brent Oil': 'red',
        'S&P 500': 'blue'
    }

    start = event_date - BDay(days_before)
    end = event_date + BDay(days_after)

    window = df[(df['Date'] >= start) & (df['Date'] <= end)].copy()

    # Required columns
    assets_vars = {
        'Brent Oil': 'Var_Brent_Close_Simple',
        'S&P 500': 'Var_S&P 500_Close_Simple'
    }

    # Check columns existence
    for col in assets_vars.values():
        if col not in window.columns:
            raise ValueError(f"Missing column '{col}' in DataFrame.")

    plt.figure(figsize=(12, 6))

    for asset_name, col in assets_vars.items():
        window[f'Cumulative_Return_{asset_name}'] = (1 + window[col]).cumprod() - 1
        plt.plot(window['Date'], window[f'Cumulative_Return_{asset_name}'], label=asset_name, color=colors.get(asset_name, 'black'))

    plt.axvline(event_date, color='red', linestyle='--', label='Event')

    plt.title(f'Cumulative Returns around Event: {event_name}')
    plt.xlabel('Date')
    plt.ylabel('Cumulative Return')
    plt.legend()
    plt.grid(True)
    plt.gca().yaxis.set_major_formatter(mtick.PercentFormatter(xmax=1.0))
    plt.tight_layout()
    plt.show()

# Run for all events
for name, date in events.items():
    plot_cumulative_returns(df, date, name)
