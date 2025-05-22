def histogram(string):
    dict_histogram = {} 
    for charactere in string:
        if (hex(ord(charactere)), charactere) in dict_histogram.keys(): 
            dict_histogram[(hex(ord(charactere)), charactere)] += 1
        else: dict_histogram[(hex(ord(charactere)), charactere)] = 1
    return dict_histogram

def frequency(string, n):
    dict_histogram = histogram(string)
    dict_frequency = {}
    for hex_char, value in dict_histogram.items(): 
        freq = value/(len(string)/n)
        if freq not in dict_frequency.keys(): 
            dict_frequency[hex_char] = freq
    return dict_frequency