"""Module containing the XOR cipher and decipher functions."""


def decrypt(encrypted_text, key):
    """Decrypts a string using the XOR cipher with a key."""

    decrypted_str = ''
    for i, char in enumerate(encrypted_text):
        # Decrypts each character of the encrypted text
        # using the corresponding character from the key (repeating the key if necessary)
        decrypted_str += chr(ord(char) ^ ord(key[i % len(key)]))

    return decrypted_str


def encrypt(plain_text, key):
    """Encrypts a string using the XOR cipher with a key."""

    encrypted_str = ''
    for i, char in enumerate(plain_text):
        # Encrypts each character of the original text
        # using the corresponding character from the key (repeating the key if necessary)
        encrypted_str += chr(ord(char) ^ ord(key[i % len(key)]))

    return encrypted_str
