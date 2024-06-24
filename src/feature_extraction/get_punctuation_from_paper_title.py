import string
import pandas as pd
import csv

# From https://www.ncbi.nlm.nih.gov/pmc/articles/PMC6119233/
# Punctuation is important: commas and colons have been shown to increase citations, but
# articles with question marks or exclamation points are cited less frequently


def find_punctuation(title):
    # This function takes a string as input and returns a string
    # with punctuation symbols found in the input string
    suspects = string.punctuation  # !"#$%&'()*+,-./:;<=>?@[\]^_`{|}~
    #print(suspects)
    elements = ""
    for ss in suspects:
        if ss in title:
            elements += ss
    return elements


df = pd.read_csv('../../data/papers_names_years_venues.csv')

list_punctuation = []
for index, row in df.iterrows():
    list_punctuation.append(find_punctuation(row['title']))

df['punctuation'] = list_punctuation

# Save the dataframe to a CSV file
df.to_csv('../../data/papers_names_years_venues_punctuation.csv', index=False)

