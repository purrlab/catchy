import string

# From https://www.ncbi.nlm.nih.gov/pmc/articles/PMC6119233/
# Punctuation is important: commas and colons have been shown to increase citations, but
# articles with question marks or exclamation points are cited less frequently


def find_punctuation(title):
    # This function takes a string as input as returns a list
    # with punctuation symbols found in the input string
    suspects = string.punctuation  # !"#$%&'()*+,-./:;<=>?@[\]^_`{|}~
    #print(suspects)
    elements = []
    for ss in suspects:
        if ss in title:
            elements.append(ss)
    return elements


title = 'Copycats: the many lives!'
list_punctuation = find_punctuation(title)
print(list_punctuation)

