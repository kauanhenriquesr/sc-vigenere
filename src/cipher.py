def decrypt(encrypted_text, key):
    decrypted_str = ''
    for i, char in enumerate(encrypted_text):
        decrypted_str += chr(ord(char) ^ ord(key[i % len(key)]))

    return decrypted_str


def encrypt(plain_text, key):
    encrypted_str = ''
    for i, char in enumerate(plain_text):
        encrypted_str += chr(ord(char) ^ ord(key[i % len(key)]))

    return encrypted_str
