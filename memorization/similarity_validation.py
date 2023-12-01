from thefuzz import fuzz


def similarity_comparison(answer, translation):
    similarity = fuzz.partial_ratio(answer, translation)
    return similarity