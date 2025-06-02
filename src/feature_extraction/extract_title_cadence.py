import cadence
import nltk


def score(actual_pattern, reference_pattern):
    length = len(actual_pattern)
    return 1.0 - sum(abs(a - b) for a, b in zip(actual_pattern, reference_pattern)) / length


def compute_cadence_score(title):
    """
        Analyze an input text and return a dictionary with scores indicating
        how closely the text matches five different poetic meters.

        Parameters:
        -----------
        title : str
            The input text to be analyzed.

        Returns:
        --------
        dict
            A dictionary with five keys (representing different poetic meters),
            each mapped to a float score between 0 and 1. The higher the score,
            the more closely the text matches that meter.
    """

    mytext = cadence.Text(title)

    text_sylls = mytext.sylls()
    text_mtree = mytext.sent(1).mtree()
    text_mtree_stats = text_mtree.get_stats()

    # lstress: lexical stress of the node
    # pstress: phrasal stress of the node
    phrasal_stress = text_mtree_stats['prom_pstress'].to_list()  # word stressed in a sentence
    syll_stress = text_sylls['prom_stress'].values.tolist()  # syllables stressed in a sentence

    stress = syll_stress

    # punctuation usually is marked as 'nan' in the stress list. I am removing them
    stress = [x for x in stress if str(x) != 'nan']

    length = len(stress)

    # Build reference patterns for two-syllable feet
    iambic_pattern = [0.0 if i % 2 == 0 else 1.0 for i in range(length)]
    trochaic_pattern = [1.0 if i % 2 == 0 else 0.0 for i in range(length)]
    spondaic_pattern = [1.0] * length

    # Build reference patterns for three-syllable feet
    anapestic_pattern = [1.0 if (i + 1) % 3 == 0 else 0.0 for i in range(length)]
    dactylic_pattern = [1.0 if i % 3 == 0 else 0.0 for i in range(length)]

    return {'iambic': score(stress, iambic_pattern),
            'trochaic': score(stress, trochaic_pattern),
            'spondaic': score(stress, spondaic_pattern),
            'anapestic': score(stress, anapestic_pattern),
            'dactylic': score(stress, dactylic_pattern)}


