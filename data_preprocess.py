
import re


def insert_whitespace(text):
    pattern = r'([A-Za-z0-9]+)([^A-Za-z0-9]+)'
    result = re.sub(pattern, r'\1 \2', text)

    pattern = r'([^A-Za-z]+)([A-Za-z]+)'
    result = re.sub(pattern, r'\1 \2', result)
    return result

def preprocess_text(text):
    text = text.replace("、", ",")
    text = text.replace("，", ",")
    text = text.replace(", ", ",")
    text = text.replace("参", "三")
    text = text.replace("中段一巢區", "中段第一巢區")
    text = text.replace("中段二巢區", "中段第二巢區")

    result = insert_whitespace(text)

    before = result + ""
    result = re.sub(r'[a-z|A-Z]([0-9]+) -', r'L\1 ', result)

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
