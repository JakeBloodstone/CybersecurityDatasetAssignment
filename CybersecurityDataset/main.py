import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
import numpy as np

# ---------------------------
# 1. LOAD DATA
# ---------------------------
df = pd.read_csv("Cybersecurity_incidents_clean.csv")

print(df.head())
print(df.info())
#
# # ---------------------------
# # 2. CLEANING
# # ---------------------------
df["Date_of_Attack"] = pd.to_datetime(df["Date_of_Attack"], dayfirst=True)
df["Month"] = df["Date_of_Attack"].dt.to_period("M")

print(df["Date_of_Attack"].dtype)

# # ---------------------------
# # 3. ATTACK TYPE ANALYSIS
# # ---------------------------
attack_counts = df["Attack_Type"].value_counts()
print(attack_counts)

sns.countplot(data=df, x="Attack_Type")
plt.xticks(rotation=45)
plt.title("Frequency of Attack Types")
plt.show()

# # ---------------------------
# # 4. SECTOR ANALYSIS
# # ---------------------------
sector_counts = df["Targeted_Sector"].value_counts()
print(sector_counts)

sns.countplot(data=df, x="Targeted_Sector")
plt.xticks(rotation=45)
plt.title("Attacks by Sector")
plt.show()

# ---------------------------
# 5. TIME SERIES ANALYSIS
# ---------------------------
monthly_attacks = df.groupby("Month").size()

monthly_attacks.plot()
plt.title("Monthly Attack Trends")
plt.xlabel("Month")
plt.ylabel("Number of Attacks")
plt.show()

# # ---------------------------
# # 6. SEVERITY VS FINANCIAL IMPACT
# # ---------------------------
plt.figure(figsize=(10,6))

sns.scatterplot(
    x=df["Severity_Score"] + np.random.uniform(-0.3, 0.3, size=len(df)),
    y=df["Estimated_Financial_Impact_USD"],
    alpha=0.4
)

# Format y-axis
plt.gca().yaxis.set_major_formatter(
    ticker.FuncFormatter(lambda x, pos: f"${x:,.0f}")
)

plt.title("Severity vs Financial Impact (USD)")
plt.xlabel("Severity Score")
plt.ylabel("Financial Impact (USD)")
plt.show()

print(df[["Severity_Score", "Estimated_Financial_Impact_USD"]].corr())

# ---------------------------
# 7. CORRELATION HEATMAP
# ---------------------------
sns.heatmap(
    df[["Severity_Score", "Estimated_Financial_Impact_USD"]].corr(),
    annot=True,
    cmap="coolwarm",
    fmt=".2f"  # cleaner numbers
)

plt.title("Correlation Heatmap")
plt.show()
#
# # ---------------------------
# # 8. OUTLIERS
# # ---------------------------
plt.figure(figsize=(10,6))

sns.boxplot(
    y=df["Estimated_Financial_Impact_USD"],
    color="lightblue"
)

sns.stripplot(
    y=df["Estimated_Financial_Impact_USD"],
    color="black",
    alpha=0.3,
    jitter=0.3
)

plt.show()
#
# ---------------------------
# FIX DATE + MONTH
# ---------------------------
df["Date_of_Attack"] = pd.to_datetime(df["Date_of_Attack"], dayfirst=True)
df["Month"] = df["Date_of_Attack"].dt.to_period("M")

# ---------------------------
# ATTACK TRENDS
# ---------------------------
# Get top 4 most common attack types
top_types = df["Attack_Type"].value_counts().nlargest(4).index

# Filter dataset
filtered_df = df[df["Attack_Type"].isin(top_types)]

# Rebuild trends
attack_trends = filtered_df.groupby(["Month", "Attack_Type"]).size().unstack()

attack_trends.plot(figsize=(10,6))

plt.title("Top Cyber Attack Trends Over Time")
plt.xlabel("Month")
plt.ylabel("Number of Attacks")
plt.legend(title="Attack Type")
plt.show()
#
# ---------------------------
# TOP 10 ATTACKS
# ---------------------------
top_attacks = df.nlargest(10, "Estimated_Financial_Impact_USD").copy()

top_attacks["Incident"] = (
    top_attacks["Attack_Type"] + " (" + top_attacks["Region"] + ")"
)

plt.figure(figsize=(10,6))

sns.barplot(
    data=top_attacks,
    x="Estimated_Financial_Impact_USD",
    y="Incident",
    hue="Attack_Type"
)

plt.title("Top 10 Most Damaging Cybersecurity Incidents")
plt.xlabel("Financial Impact (USD)")
plt.ylabel("Incident")

plt.show()
#---------------------------
#SECTOR SEVERITY
#---------------------------
# ---------------------------
# CALCULATE FIRST
# ---------------------------
sector_severity = df.groupby("Targeted_Sector")["Severity_Score"].mean().sort_values()

# ---------------------------
# THEN PLOT
# ---------------------------
plt.figure(figsize=(10,6))

sns.barplot(
    x=sector_severity.values,
    y=sector_severity.index,
    hue=sector_severity.index,
    palette="viridis",
    legend=False
)

plt.title("Average Attack Severity by Sector")
plt.xlabel("Average Severity Score")
plt.ylabel("Sector")

plt.show()