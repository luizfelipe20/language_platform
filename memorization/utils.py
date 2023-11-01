import re


def standardize_text(text):
    pattern = re.compile('<.*?>')
    result = re.sub(pattern, '', text)   
    return str(result).lower()