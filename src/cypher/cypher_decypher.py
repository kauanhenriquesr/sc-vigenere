"""Cypher and decypher module"""


def encrypt_char(char, key_char):
    """Encrypts a single character using the XOR operation with a key character"""

    # Converts characters to their ASCII values, applies XOR, and converts back to a character
    return chr(ord(char) ^ ord(key_char))


def decrypt_char(char, key_char):
    """Decrypts a single character using the XOR operation with a key character"""

    # Converts characters to their ASCII values, applies XOR, and converts back to a character
    return chr(ord(char) ^ ord(key_char))


def encrypt(plain_text, key):
    """Encrypts a string using the XOR cipher with a key"""

    encrypted_str = ''
    for i in range(len(plain_text)):
        # Encrypts each character of the original text
        # using the corresponding character from the key (repeating the key if necessary)
        encrypted_str += encrypt_char(plain_text[i], key[i % len(key)])

    return encrypted_str


def decrypt(encrypted_text, key):
    """Decrypts a string using the XOR cipher with a key"""

    decrypted_str = ''
    for i in range(len(encrypted_text)):
        # Decrypts each character of the encrypted text
        # using the corresponding character from the key (repeating the key if necessary)
        decrypted_str += decrypt_char(encrypted_text[i], key[i % len(key)])

    return decrypted_str


def encryptvig(message, key):
    """Encrypts a message using the Vigenère Cipher"""

    encrypted_text = []
    for i, _ in enumerate(message):
        x = (ord(_) + ord(key[i % len(key)]) - 2 * ord('a')) % 26
        x += ord('a')
        encrypted_text.append(chr(x))
    return "".join(encrypted_text)


def decryptvig(encrypted_text, key):
    """Decrypts a message using the Vigenère Cipher"""

    decrypted_text = []
    for i, _ in enumerate(encrypted_text):
        x = (ord(_) - ord(key[i % len(key)]) + 26) % 26
        x += ord('a')
        decrypted_text.append(chr(x))
    return "".join(decrypted_text)


def testencryptvig():
    """Test function for the Vigenère Cipher"""

    message = "teste"
    key = "key"
    print("Testing Vigenère Cipher:")
    print(f"Original Message: {message}")
    print(f"Key: {key}")

    encrypted = encryptvig(message, key)
    print(f"Encrypted Text: {encrypted}")

    decrypted = decryptvig(encrypted, key)
    print(f"Decrypted Text: {decrypted}")

    if message == decrypted:
        print("Vigenère Cipher test passed!")
    else:
        print("Vigenère Cipher test FAILED!")
    print("-" * 20)


def testencryptxor():
    """Test function for the XOR Cipher"""

    message = "Hello World!"
    key = "secret"
    print("Testing XOR Cipher:")
    print(f"Original Message: {message}")
    print(f"Key: {key}")

    encrypted = encrypt(message, key)
    print(f"Encrypted Text (XOR): {encrypted}")

    decrypted = decrypt(encrypted, key)
    print(f"Decrypted Text (XOR): {decrypted}")

    if message == decrypted:
        print("XOR Cipher test passed!")
    else:
        print("XOR Cipher test FAILED!")
    print("-" * 20)


testencryptvig()
testencryptxor()
