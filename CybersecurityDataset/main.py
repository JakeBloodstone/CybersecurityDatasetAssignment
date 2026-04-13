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