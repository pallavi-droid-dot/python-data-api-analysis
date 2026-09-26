import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import requests

# Set plot style
sns.set_theme(style="whitegrid")

# ---------------------------------------------------------
# Part 1: Consume a REST API & Process JSON
# ---------------------------------------------------------
print("Fetching live data from REST API...")
url = "https://api.coingecko.com/api/v3/coins/markets"
params = {
    'vs_currency': 'usd',
    'order': 'market_cap_desc',
    'per_page': 10,
    'page': 1
}

response = requests.get(url, params=params)

if response.status_code == 200:
    api_data = response.json()
    df_api = pd.DataFrame(api_data)[['name', 'symbol', 'current_price', 'market_cap', 'price_change_percentage_24h']]
    print("\nAPI Data Loaded Successfully:")
    print(df_api.head())
else:
    print(f"Failed to fetch API data. Status code: {response.status_code}")

# ---------------------------------------------------------
# Part 2: Data Cleaning & Manipulation
# ---------------------------------------------------------
df_api.loc[2, 'price_change_percentage_24h'] = np.nan

print("\n--- Data Cleaning ---")
print("Missing values before cleaning:\n", df_api.isnull().sum())

mean_change = df_api['price_change_percentage_24h'].mean()
df_api['price_change_percentage_24h'].fillna(mean_change, inplace=True)

print("Missing values after cleaning:\n", df_api.isnull().sum())

df_api['market_cap_billions'] = df_api['market_cap'] / 1e9

# ---------------------------------------------------------
# Part 3: Data Visualization
# ---------------------------------------------------------
fig, axes = plt.subplots(1, 2, figsize=(14, 5))

sns.barplot(data=df_api, x='market_cap_billions', y='name', ax=axes[0], palette='Blues_r')
axes[0].set_title('Top 10 Cryptocurrencies by Market Cap ($B)')
axes[0].set_xlabel('Market Cap (in Billions USD)')
axes[0].set_ylabel('Cryptocurrency')

sns.barplot(data=df_api, x='symbol', y='price_change_percentage_24h', ax=axes[1], palette='coolwarm')
axes[1].set_title('24h Price Change (%)')
axes[1].set_xlabel('Coin Symbol')
axes[1].set_ylabel('Price Change (%)')

plt.tight_layout()
plt.savefig('crypto_analysis.png')
plt.show()

# ---------------------------------------------------------
# Part 4: Automated Summary Report
# ---------------------------------------------------------
summary_report = f"""
==================================================
        PYTHON DATA ANALYSIS REPORT
==================================================
Total Coins Analyzed: {len(df_api)}
Highest Market Cap: {df_api.iloc[0]['name']} (${df_api.iloc[0]['market_cap_billions']:.2f}B)
Average 24h Price Change: {df_api['price_change_percentage_24h'].mean():.2f}%

Top Performers (24h):
{df_api.sort_values(by='price_change_percentage_24h', ascending=False)[['name', 'price_change_percentage_24h']].to_string(index=False)}
==================================================
"""

print(summary_report)

with open('summary_report.txt', 'w') as f:
    f.write(summary_report)
