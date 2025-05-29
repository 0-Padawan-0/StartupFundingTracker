import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import os

# Set up style and create folder to save plots
sns.set(style="whitegrid")
os.makedirs("plots", exist_ok=True)

# Load the cleaned data
df = pd.read_excel("cleaned_funding_data_2025.xlsx")

# Convert funding date
if 'last_funding_date' in df.columns:
    df['last_funding_date'] = pd.to_datetime(df['last_funding_date'], errors='coerce')
    df['month'] = df['last_funding_date'].dt.to_period('M')

# 1. 💰 Top 10 Industries by Total Funding
plt.figure(figsize=(12, 6))
industry_funding = df.groupby('industry')['funding_amount_usd'].sum().sort_values(ascending=False).head(10)
sns.barplot(x=industry_funding.values, y=industry_funding.index, palette="viridis")
plt.title("💰 Top 10 Industries by Total Funding (USD)")
plt.xlabel("Total Funding (USD)")
plt.ylabel("Industry")
plt.tight_layout()
plt.savefig("plots/01_top_industries_total_funding.png")
plt.close()

# 2. 📈 Top 10 Industries by Average Funding
plt.figure(figsize=(12, 6))
avg_funding = df.groupby('industry')['funding_amount_usd'].mean().sort_values(ascending=False).head(10)
sns.barplot(x=avg_funding.values, y=avg_funding.index, palette="Blues_d")
plt.title("📈 Top 10 Industries by Average Funding per Startup")
plt.xlabel("Average Funding (USD)")
plt.ylabel("Industry")
plt.tight_layout()
plt.savefig("plots/02_average_funding_by_industry.png")
plt.close()

# 3. 📊 Top 10 Industries by Number of Startups
plt.figure(figsize=(12, 6))
industry_count = df['industry'].value_counts().head(10)
sns.barplot(x=industry_count.values, y=industry_count.index, palette="coolwarm")
plt.title("📊 Top 10 Industries by Startup Count")
plt.xlabel("Number of Startups")
plt.ylabel("Industry")
plt.tight_layout()
plt.savefig("plots/03_startup_count_by_industry.png")
plt.close()

# 4. 🌍 Top 10 Countries by Total Funding
if 'country' in df.columns:
    plt.figure(figsize=(12, 6))
    country_funding = df.groupby('country')['funding_amount_usd'].sum().sort_values(ascending=False).head(10)
    sns.barplot(x=country_funding.values, y=country_funding.index, palette="magma")
    plt.title("🌍 Top 10 Countries by Total Startup Funding")
    plt.xlabel("Total Funding (USD)")
    plt.ylabel("Country")
    plt.tight_layout()
    plt.savefig("plots/04_top_countries_by_total_funding.png")
    plt.close()

# 5. 🧱 Top 10 Funding Types by Frequency
if 'funding_type' in df.columns:
    plt.figure(figsize=(12, 6))
    funding_type_counts = df['funding_type'].value_counts().head(10)
    sns.barplot(x=funding_type_counts.index, y=funding_type_counts.values, palette="cubehelix")
    plt.title("🧱 Top 10 Funding Types by Frequency")
    plt.xlabel("Funding Type")
    plt.ylabel("Number of Startups")
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.savefig("plots/05_top_funding_types_by_frequency.png")
    plt.close()

# 6. 📅 Monthly Startup Funding Trend
if 'month' in df.columns:
    monthly_funding = df.groupby('month')['funding_amount_usd'].sum()
    plt.figure(figsize=(14, 6))
    monthly_funding.plot(kind='line', marker='o', color='teal')
    plt.title("📅 Monthly Startup Funding Trend")
    plt.xlabel("Month")
    plt.ylabel("Total Funding (USD)")
    plt.grid(True)
    plt.tight_layout()
    plt.savefig("plots/06_monthly_funding_trend.png")
    plt.close()

# 7. 🧩 Stacked Funding Type Distribution by Industry
if 'funding_type' in df.columns:
    pivot_data = pd.crosstab(df['industry'], df['funding_type'])
    pivot_data = pivot_data[pivot_data.sum(axis=1) > 5]  # filter for industries with >5 startups
    pivot_data = pivot_data.head(10)  # limit to top 10 industries
    pivot_data.plot(kind='bar', stacked=True, figsize=(14, 6), colormap='tab20')
    plt.title("🧩 Funding Type Distribution by Industry (Top 10)")
    plt.xlabel("Industry")
    plt.ylabel("Number of Startups")
    plt.tight_layout()
    plt.savefig("plots/07_funding_type_distribution_stacked.png")
    plt.close()
