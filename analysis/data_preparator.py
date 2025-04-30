import pandas as pd
from sklearn.model_selection import train_test_split

from outlier_util import remove_outliers_iqr

# from pipeline import prepare

df = pd.read_csv('./data/raw/data-v5.csv')

df.drop(columns=['localityName'], inplace=True)  # Drop the index column if it exists

df_kangaroo = pd.read_csv('./data/clean/kangaroo-cleaned-with-id.csv')

df = df.merge(df_kangaroo, left_on='propertyId', right_on='id', how='left', suffixes=('', '_kangaroo'))

df = remove_outliers_iqr(df, columns=['price', 'livingArea'], multiplier=1.5, min_thresholds={'livingArea' : 25})

df = df.fillna(-1)

df = df.drop(columns=['id', 'propertyId'])  # Drop the index column if it exists

# Split the dataset into training and testing sets (80% train, 20% test)
train_df, test_df = train_test_split(df, test_size=0.2, random_state=42)

train_df.to_csv('./data/train_data-cleaned.csv')
test_df.to_csv('./data/test_data-cleaned.csv')
