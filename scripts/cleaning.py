#!/usr/bin/python3.6

import os
import pandas as pd

from utils import convert_emojis
from utils import convert_emoticons
from utils import remove_emoji

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
df_clean['tweet'] = df_clean['tweet'].apply(convert_emoticons)
df_clean['tweet'] = df_clean['tweet'].apply(convert_emojis)

# Remove lasting emojis
df_clean['tweet'] = df_clean['tweet'].apply(remove_emoji)

# Save clean data
output_path = os.path.join('..', 'data', 'clean_tweets.csv')
df_clean.to_csv(output_path, index=False)
