import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

# ---------------------------
# 1. LOAD DATA
# ---------------------------
df = pd.read_csv("Cybersecurity_incidents_clean.csv")

print(df.head())
print(df.info())

# ---------------------------
# 2. CLEANING
# ---------------------------
df["Date_of_Attack"] = pd.to_datetime(df["Date_of_Attack"], dayfirst=True)
df["Month"] = df["Date_of_Attack"].dt.to_period("M")

print(df["Date_of_Attack"].dtype)

# ---------------------------
# 3. ATTACK TYPE ANALYSIS
# ---------------------------
attack_counts = df["Attack_Type"].value_counts()
print(attack_counts)

sns.countplot(data=df, x="Attack_Type")
plt.xticks(rotation=45)
plt.title("Frequency of Attack Types")
plt.show()

# ---------------------------
# 4. SECTOR ANALYSIS
# ---------------------------
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

# ---------------------------
# 6. SEVERITY VS FINANCIAL IMPACT
# ---------------------------
sns.scatterplot(
    data=df,
    x="Severity_Score",
    y="Estimated_Financial_Impact_USD"
)

plt.title("Severity vs Financial Impact")
plt.show()

print(df[["Severity_Score", "Estimated_Financial_Impact_USD"]].corr())

# ---------------------------
# 7. CORRELATION HEATMAP
# ---------------------------
sns.heatmap(
    df[["Severity_Score", "Estimated_Financial_Impact_USD"]].corr(),
    annot=True,
    cmap="coolwarm"
)

plt.title("Correlation Heatmap")
plt.show()

# ---------------------------
# 8. OUTLIERS
# ---------------------------
sns.boxplot(y=df["Estimated_Financial_Impact_USD"])
plt.title("Financial Impact Outliers")
plt.show()

# ---------------------------
# 9. ATTACK TYPE TRENDS OVER TIME
# ---------------------------
attack_trends = df.groupby(["Month", "Attack_Type"]).size().unstack()

attack_trends.plot(figsize=(10,6))

plt.title("Attack Type Trends Over Time")
plt.xlabel("Month")
plt.ylabel("Number of Attacks")
plt.legend(title="Attack Type")
plt.show()

# ---------------------------
# 10. TOP 10 MOST DAMAGING ATTACKS
# ---------------------------
top_attacks = df.nlargest(10, "Estimated_Financial_Impact_USD")

sns.barplot(
    data=top_attacks,
    x="Estimated_Financial_Impact_USD",
    y="Attack_Type"
)

plt.title("Top 10 Most Damaging Cyber Attacks")
plt.xlabel("Financial Impact (USD)")
plt.ylabel("Attack Type")
plt.show()

# ---------------------------
# 11. AVERAGE SEVERITY BY SECTOR
# ---------------------------
sector_severity = df.groupby("Targeted_Sector")["Severity_Score"].mean().sort_values()

sector_severity.plot(kind="barh")

plt.title("Average Attack Severity by Sector")
plt.xlabel("Average Severity Score")
plt.ylabel("Sector")
plt.show()