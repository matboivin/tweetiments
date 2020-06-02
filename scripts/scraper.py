#!/usr/bin/python3.6

import os
import twint

seed_hashtag = '#AmericaOrTrump' # Replace value
seed_hashtag = seed_hashtag.lower()
output_path = os.path.join('..', 'data', 'tweets.csv')

c = twint.Config()
c.Hide_output = True
c.Limit = 2200 # Replace value
c.Store_object = True
c.Search = seed_hashtag
c.Store_csv = True
c.Output = output_path

print('Getting tweets...')
twint.run.Search(c)

print('Done')
