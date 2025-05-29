'''
In each get_feature_x.py file, several feature extraction functions are defined, within the category of the file name.
all functions should have the fucntion name of: get_feature_x1, get_feature_x2, get_feature_x3, etc.

'''

import lftk 
import spacy




def get_features_lftk_all(file: dict) -> dict:
    '''
    Extracts all features from the given file metadata using LFTK.
    Args:
        file (dict): Metadata of the paper containing keys like 'pdf_path', 'img_path', etc.
    Returns:
        dict: A dictionary containing all extracted features.
    '''

    interested_lftk_features ={}

    # get the information of interests
    title = file.get('title')
    abstract = file.get('abstract')
 

    lftk_features_title=[
        't_word', # totall number of words in the title
        't_stopword', # total number of stopwords in the title
        't_punct', # total number of punctuations in the title
        't_char', # total number of characters in the title
        # TODO: more features needed

    ]

    lftk_features_abstract= lftk_features_title + [
        't_uword', # total number of unique words in the abstract
        't_sent', # total number of sentences in the abstract
        'a_word_ps', # average_number_of_words_per_sentence
        'a_char_ps', # average_number_of_characters_per_sentence
        'a_char_pw', # average_number_of_characters_per_word
        # lexico-semantics
        'a_subtlex_us_zipf_pw', # average subtlex us zipf of words per word
        'a_kup_pw', # average kuperman age of acquisition of words per word
        # 

        # TODO: more features needed

    ]

    nlp = spacy.load("en_core_web_sm")

    title_extractor = lftk.Extractor(docs=nlp(title))
    title_features = title_extractor.extract(features=lftk_features_title)
    # Combine features from title and abstract
    title_features_prefixed = {f'title_{k}': v for k, v in title_features.items()}
    interested_lftk_features.update(title_features_prefixed)

    if isinstance(abstract, str) and abstract.strip():
        abstract_extractor = lftk.Extractor(docs=nlp(abstract))
        abstract_features = abstract_extractor.extract(features=lftk_features_abstract)
        abstract_features_prefixed = {f'abstract_{k}': v for k, v in abstract_features.items()}
    else:
        abstract_features_prefixed = {f'abstract_{k}': None for k in lftk_features_abstract}

    interested_lftk_features.update(abstract_features_prefixed)



    return interested_lftk_features