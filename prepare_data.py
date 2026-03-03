import pandas as pd
from sklearn.model_selection import train_test_split
import numpy as np
import os

TARGET_CURRENCIES = ['USD', 'EUR', 'GBP', 'INR', 'JPY', 'AUD', 'CAD', 'BRL', 'NZD', 'SGD']

df = pd.read_csv('data/raw/data/banknote_net.csv')
df = df[df['Currency'].isin(TARGET_CURRENCIES)]

print(f"Total samples: {len(df)}")
print(f"\nSamples per currency:")
print(df['Currency'].value_counts())

feature_cols = [f'v_{i}' for i in range(256)]
X = df[feature_cols].values
y = df['Currency'].values

X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42, stratify=y
)

os.makedirs('data/processed', exist_ok=True)
np.save('data/processed/X_train.npy', X_train)
np.save('data/processed/X_test.npy', X_test)
np.save('data/processed/y_train.npy', y_train)
np.save('data/processed/y_test.npy', y_test)

print(f"\nTraining samples: {len(X_train)}")
print(f"Testing samples: {len(X_test)}")
print("\nProcessed data saved to data/processed/ ✅")