def categorize_char(char):
    if char.isspace():
        return None
    elif char.isalnum():
        return True
    else:
        return None


def tokenize(code):
    last_cat = None
    result = []
    for char in code:
        cat = categorize_char(char)
        if last_cat is not None and last_cat == cat:
            result[-1] += char
        else:
            result.append(char)
        last_cat = cat
    return result
