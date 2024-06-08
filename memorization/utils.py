import re


def standardize_text(text):
    pattern = re.compile('<.*?>')
    result = re.sub(pattern, '', text)   
    return result.lower().strip().encode('ascii', 'replace').decode("utf-8").replace('?', ' ')


def remove_number_from_text(sentence):
    pattern = r'[0-9]{1,2}\.'
    new_string = re.sub(pattern, '', sentence)
    return new_string.replace('"', '').replace("-", "").strip()