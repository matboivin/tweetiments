#!/usr/bin/python3.6

import os
import pandas as pd

from utils import convert_emojis
from utils import convert_emoticons

# Create filepath
df_path = os.path.join('..', 'data', 'tweets.csv')

# Create dataframe
df = pd.read_csv(df_path)

# Select columns
features = [
    'id',
    'created_at',
    'date',
    'time',
    'timezone',
    'tweet',
    'replies_count',
    'retweets_count',
    'likes_count',
    'hashtags',
    'retweet'   
]

df_clean = df[features]

# Convert emojis and emoticons
df_clean['tweet'] = df_clean['tweet'].map(convert_emoticons)
df_clean['tweet'] = df_clean['tweet'].map(convert_emojis)

# Remove remaining emojis
df_clean = df_clean.astype(str).apply(lambda x: x.str.encode('ascii', 'ignore').str.decode('ascii'))

# Save clean data
output_path = os.path.join('..', 'data', 'clean_tweets.csv')
df_clean.to_csv(output_path, index=False)
