
import re


def insert_whitespace(text):
    pattern = r'([A-Za-z0-9]+)([^A-Za-z0-9]+)'
    result = re.sub(pattern, r'\1 \2', text)
    return result

def preprocess_text(text):
    result = insert_whitespace(text)

    # Add the new functionality here
    result = re.sub(r',\s', r',', result)
    result = re.sub(r',', r' ', result)
    result = re.sub(r'\s+', r' ', result)

    #ll to L
    new_pattern = r'\bll([0-9]+)\b'
    result = re.sub(new_pattern, r'L\1', result)
    #LL to L
    new_pattern = r'\bLL([0-9]+)\b'
    result = re.sub(new_pattern, r'L\1', result)
    return result