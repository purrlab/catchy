import string
import pandas as pd
import csv

# From https://www.ncbi.nlm.nih.gov/pmc/articles/PMC6119233/
# Punctuation is important: commas and colons have been shown to increase citations, but
# articles with question marks or exclamation points are cited less frequently

def find_punctuation_pos(title, punctuation):
    pos = 0
    results = []
    while title.find(punctuation, pos) > -1:
        # print(t, t.find(s,p))
        results.append(title.find(punctuation, pos))
        pos = title.find(punctuation, pos) + 1
        #print(title, punctuation, results)
    return results

df = pd.read_csv('../../data/papers_names_years_venues.csv')

punctuation_chars = {':', '?', '!'}
for p in punctuation_chars:
    list_results = []
    for index, row in df.iterrows():
        list_results.append(find_punctuation_pos(row['title'], p))
    print(list_results)

    df['punctuationpos_' + p] = list_results

# Save the dataframe to a CSV file
df.to_csv('../../data/papers_names_years_venues_punctuationpos.csv', index=False)
