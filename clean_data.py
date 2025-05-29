import pandas as pd
import re

# Load raw scraped data
df = pd.read_excel("funded_startups_multiple_sectors_2025.xlsx")

# Normalize column names (lowercase + underscores)
df.columns = df.columns.str.strip().str.lower().str.replace(" ", "_")
print("Normalized Columns:", df.columns)

# Optional: Rename for easier handling
if 'funding_amount_(usd)' in df.columns:
    df.rename(columns={'funding_amount_(usd)': 'funding_amount_raw'}, inplace=True)
else:
    print("⚠️ 'funding_amount_(usd)' column not found in Excel.")
    exit()

# Define a function to convert funding string to numeric USD value
def parse_funding(value):
    if pd.isna(value):
        return 0
    value = value.replace('$', '').replace(',', '').strip().upper()
    if 'K' in value:
        return float(value.replace('K', '')) * 1_000
    elif 'M' in value:
        return float(value.replace('M', '')) * 1_000_000
    elif 'B' in value:
        return float(value.replace('B', '')) * 1_000_000_000
    try:
        return float(value)
    except:
        return 0

# Apply the conversion function to funding column
df['funding_amount_usd'] = df['funding_amount_raw'].apply(parse_funding)

# Optional: Convert funding date column to datetime
if 'last_funding_date' in df.columns:
    df['last_funding_date'] = pd.to_datetime(df['last_funding_date'], errors='coerce')

# Final preview
print(df[['name', 'industry', 'funding_amount_raw', 'funding_amount_usd']].head())

# Save cleaned data
df.to_excel("cleaned_funding_data_2025.xlsx", index=False)
print("✅ Cleaned data saved as 'cleaned_funding_data_2025.xlsx'")
