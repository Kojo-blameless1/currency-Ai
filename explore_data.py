import pandas as pd

# Load the dataset
df = pd.read_csv('data/raw/data/banknote_net.csv')

# Let's see what we're working with
print("Shape:", df.shape)
print("\nColumns:", df.columns.tolist())
print("\nFirst 3 rows:")
print(df.head(3))
print("\nCurrencies available:")
print(df['Currency'].value_counts())

print("\nDenominations per currency:")
print(df.groupby(['Currency', 'Denomination']).size().to_string())