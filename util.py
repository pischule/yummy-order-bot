def replace_all(text, symbols, replacement):
    symbols_set = set(symbols)
    return ''.join([replacement if c in symbols_set else c for c in text])
