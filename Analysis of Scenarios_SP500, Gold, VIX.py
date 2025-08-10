# -*- coding: utf-8 -*-
"""
Created on Sun Aug 10 22:30:41 2025

@author: everl
"""
#############################################################

import pandas as pd
import matplotlib.pyplot as plt
from pandas.tseries.offsets import BDay
from matplotlib.ticker import PercentFormatter

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

#################################################################

# Excel file path
excel_path = r'[PUT THE PATH OF THE SAVED FILE, THE FILE IS CALLED Data Assets_SP500, Gold, Vix, Brent and Others Indices]'

# Load data
df = pd.read_excel(excel_path, parse_dates=['Date'])

# Key events
events = {
    'Global Financial Crisis (2008-2009)': pd.to_datetime('2008-09-29'),
    'European Sovereign Debt Crisis & US Downgrade (2011)': pd.to_datetime('2011-08-08'),
    'China Flash Crash and Emerging Markets Tensions (2015)': pd.to_datetime('2015-08-24'),
    'Correction due to Rate Tensions and Overvaluation (2018)': pd.to_datetime('2018-02-05'),
    'COVID-19 Pandemic (2020)': pd.to_datetime('2020-03-09'),
    'Trade War (2025)': pd.to_datetime('2025-04-04'),
}

# Parameters
days_before = 20
days_after = 20

################################################################

# Base function to calculate cumulative returns
def calculate_returns(df, columns):
    df = df.copy()
    for col in columns:
        df[col + '_ret'] = df[col].pct_change()
        df[col + '_cumret'] = (1 + df[col + '_ret']).cumprod() - 1
    return df

################################################################

# Plot S&P 500 and VIX cumulative returns for event
def plot_event(df, event_date, event_name):
    window = df[(df['Date'] >= event_date - BDay(days_before)) & 
                (df['Date'] <= event_date + BDay(days_after))]
    window = calculate_returns(window, ['S&P 500_Close', 'VIX_Close'])

    plt.figure(figsize=(14, 8))
    
    ax1 = plt.gca()
    ax1.plot(window['Date'], window['S&P 500_Close_cumret'], color='blue', label='S&P 500 (cum. return)')
    ax1.set_ylabel('S&P 500 Return')
    ax1.yaxis.set_major_formatter(PercentFormatter(1.0))
    
    ax2 = ax1.twinx()
    ax2.plot(window['Date'], window['VIX_Close_cumret'], color='red', linestyle='--', label='VIX (cum. return)')
    ax2.set_ylabel('VIX Return')
    ax2.yaxis.set_major_formatter(PercentFormatter(1.0))
    
    plt.title(f'Cumulative Return of S&P 500 and VIX - {event_name}')
    ax1.set_xlabel('Date')
    
    ax1.axvline(event_date, color='black', linestyle='--', label='Event')
    lines1, labels1 = ax1.get_legend_handles_labels()
    lines2, labels2 = ax2.get_legend_handles_labels()
    ax1.legend(lines1 + lines2, labels1 + labels2, loc='upper left')
    plt.grid(True)
    plt.show()

################################################################
# Plot event including gold returns
def plot_event_with_gold(df, event_date, event_name):
    window = df[(df['Date'] >= event_date - BDay(days_before)) & 
                (df['Date'] <= event_date + BDay(days_after))]
    window = calculate_returns(window, ['S&P 500_Close', 'VIX_Close', 'Gold_Close'])

    plt.figure(figsize=(14, 8))
    
    ax1 = plt.gca()
    ax1.plot(window['Date'], window['S&P 500_Close_cumret'], label='S&P 500', color='blue')
    ax1.plot(window['Date'], window['Gold_Close_cumret'], label='Gold', color='gold')
    ax1.set_ylabel('S&P 500 and Gold Return')
    ax1.yaxis.set_major_formatter(PercentFormatter(1.0))
    
    ax2 = ax1.twinx()
    ax2.plot(window['Date'], window['VIX_Close_cumret'], label='VIX', color='magenta', linestyle='--')
    ax2.set_ylabel('VIX Return')
    ax2.yaxis.set_major_formatter(PercentFormatter(1.0))
    
    ax1.axvline(event_date, color='black', linestyle='--', label='Event')
    plt.title(f'Cumulative Return of S&P 500, Gold and VIX - {event_name}')
    ax1.set_xlabel('Date')

    lines1, labels1 = ax1.get_legend_handles_labels()
    lines2, labels2 = ax2.get_legend_handles_labels()
    ax1.legend(lines1 + lines2, labels1 + labels2, loc='upper left')
    plt.grid(True)
    plt.show()

##################################################################

# Plot cumulative returns only
def plot_cumulative_return_event(df, event_date, event_name):
    window = df[(df['Date'] >= event_date - BDay(days_before)) & 
                (df['Date'] <= event_date + BDay(days_after))]
    window = calculate_returns(window, ['S&P 500_Close', 'Gold_Close', 'VIX_Close'])

    plt.figure(figsize=(14, 7))
    plt.plot(window['Date'], window['S&P 500_Close_cumret'], label='S&P 500', color='blue')
    plt.plot(window['Date'], window['Gold_Close_cumret'], label='Gold', color='orange')
    plt.plot(window['Date'], window['VIX_Close_cumret'], label='VIX', color='green')
    
    plt.axvline(event_date, color='red', linestyle='--', label='Event')
    plt.title(f'Cumulative Return - {event_name}')
    plt.xlabel('Date')
    plt.ylabel('Cumulative Return')
    plt.gca().yaxis.set_major_formatter(PercentFormatter(1.0))
    plt.legend()
    plt.grid(True)
    plt.show()

# Run for all events
for name, date in events.items():
    plot_event(df, date, name)
    plot_event_with_gold(df, date, name)
    plot_cumulative_return_event(df, date, name)
