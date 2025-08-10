# -*- coding: utf-8 -*-
"""
Created on Sun Aug 10 22:45:26 2025

@author: everl
"""

import pandas as pd
import matplotlib.pyplot as plt
from pandas.tseries.offsets import BDay
import matplotlib.ticker as mtick

############################################################

# Global settings to improve plot readability
plt.rcParams.update({
    'font.size': 12,
    'axes.titlesize': 18,
    'axes.labelsize': 14,
    'xtick.labelsize': 12,
    'ytick.labelsize': 12,
    'legend.fontsize': 12,
    'figure.titlesize': 16,
})

###########################################################

# Path to the Excel file with bond data
excel_path = r'PUT THE PATH OF THE SAVED FILE, THE FILE IS CALLED Data US10Y vs Bund Germany 10Y_Only Return'
df = pd.read_excel(excel_path, parse_dates=['Date'])

# Eventos clave
events = {
    'Global Financial Crisis (2008-2009)': pd.to_datetime('2008-09-29'),
    'European Sovereign Debt Crisis and US Downgrade (2011)': pd.to_datetime('2011-08-08'),
    'China Flash Crash and Emerging Markets Tensions (2015)': pd.to_datetime('2015-08-24'),
    'Correction due to Rate Tensions and Overvaluation (2018)': pd.to_datetime('2018-02-05'),
    'COVID-19 Pandemic (2020)': pd.to_datetime('2020-03-09'),
    'Trade War (2025)': pd.to_datetime('2025-04-04'),
}

############################################################

# Analysis window parameters
days_before = 20
days_during = 7
days_after = 20

def plot_bonds_event(df, event_date, event_name):
    before_start = event_date - BDay(days_before)
    before_end = event_date - BDay(1)
    
    during_start = event_date - BDay(days_during // 2)
    during_end = event_date + BDay(days_during // 2)
    
    after_start = event_date + BDay(1)
    after_end = event_date + BDay(days_after)
    
    df_before = df[(df['Date'] >= before_start) & (df['Date'] <= before_end)]
    df_during = df[(df['Date'] >= during_start) & (df['Date'] <= during_end)]
    df_after = df[(df['Date'] >= after_start) & (df['Date'] <= after_end)]
    
    plt.figure(figsize=(14, 8))
    
    plt.plot(df_before['Date'], df_before['US_Bond10Y_Close'], label='US 10Y Before', color='blue')
    plt.plot(df_during['Date'], df_during['US_Bond10Y_Close'], label='US 10Y During', color='red')
    plt.plot(df_after['Date'], df_after['US_Bond10Y_Close'], label='US 10Y After', color='green')
    
    plt.plot(df_before['Date'], df_before['GER_Bund10Y_Close'], label='German Bund Before', color='orange', linestyle='--')
    plt.plot(df_during['Date'], df_during['GER_Bund10Y_Close'], label='German Bund During', color='brown', linestyle='--')
    plt.plot(df_after['Date'], df_after['GER_Bund10Y_Close'], label='German Bund After', color='gold', linestyle='--')
    
    plt.title(f'US and German Bund Bond Prices - Event: {event_name}')
    plt.xlabel('Date')
    plt.ylabel('Close Price')
    plt.legend(loc='upper left')
    plt.grid(True)
    plt.show()

############################################################################

def plot_bond_cumulative_return(df, event_date, event_name):
    before_start = event_date - BDay(days_before)
    after_end = event_date + BDay(days_after)
    
    total_window = df[(df['Date'] >= before_start) & (df['Date'] <= after_end)].copy()
    
    for col in ['US_Bond10Y_Close', 'GER_Bund10Y_Close']:
        total_window[col + '_ret'] = total_window[col].pct_change()
        total_window[col + '_ret_cum'] = (1 + total_window[col + '_ret']).cumprod() - 1
    
    plt.figure(figsize=(14, 7))
    plt.plot(total_window['Date'], total_window['US_Bond10Y_Close_ret_cum'], label='US 10Y Cumulative Return', color='blue')
    plt.plot(total_window['Date'], total_window['GER_Bund10Y_Close_ret_cum'], label='German Bund Cumulative Return', color='orange')
    plt.axvline(event_date, color='red', linestyle='--', label='Event')
    plt.title(f'Cumulative Returns Before and After - {event_name}')
    plt.xlabel('Date')
    plt.ylabel('Cumulative Return')
    plt.gca().yaxis.set_major_formatter(mtick.PercentFormatter(xmax=1.0))
    plt.legend()
    plt.grid(True)
    plt.tight_layout()
    plt.show()

##########################################################################

# Run for all events
for name, date in events.items():
    plot_bonds_event(df, date, name)
    plot_bond_cumulative_return(df, date, name)
