import pandas as pd

df = pd.read_csv("Cybersecurity_incidents_clean.csv")

print(df.head())
print(df.info())

# Check missing values
print(df.isnull().sum())

# Convert date properly
df["Date_of_Attack"] = pd.to_datetime(df["Date_of_Attack"], dayfirst=True)

# Check unique attack types
print(df["Attack_Type"].unique())

attack_counts = df["Attack_Type"].value_counts()
print(attack_counts)

import seaborn as sns
import matplotlib.pyplot as plt

sns.countplot(data=df, x="Attack_Type")
plt.xticks(rotation=45)
plt.title("Frequency of Attack Types")
plt.show()