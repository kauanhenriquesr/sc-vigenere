"""frequency module"""


def histogram(string):
    """Calculates the histogram of characters in a string."""

    # Initialize an empty dictionary to store the histogram
    dict_histogram = {}

    for charactere in string:
        key_tuple = (hex(ord(charactere)), charactere)
        if key_tuple in dict_histogram.keys():
            dict_histogram[key_tuple] += 1
        else:
            dict_histogram[key_tuple] = 1

    return dict_histogram


def frequency(string, n):
    """Calculates the frequency of characters based on the histogram and a normalization factor."""

    dict_histogram = histogram(string)

    dict_frequency = {}

    for hex_char, value in dict_histogram.items():
        freq = value/(len(string)/n)

        if freq not in dict_frequency.keys():
            dict_frequency[hex_char] = freq

    return dict_frequency
