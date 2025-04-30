import pandas as pd
from sklearn.model_selection import train_test_split

# from pipeline import prepare

df = pd.read_csv('./data/raw/data-v5.csv')

df.drop(columns=['localityName'], inplace=True)  # Drop the index column if it exists

# Split the dataset into training and testing sets (80% train, 20% test)
train_df, test_df = train_test_split(df, test_size=0.2, random_state=42)


train_df.to_csv('./data/train_data-cleaned.csv')
test_df.to_csv('./data/test_data-cleaned.csv')
