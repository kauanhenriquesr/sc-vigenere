def encrypt_char(char, key_char):
    return chr(ord(char) ^ ord(key_char))

def decrypt_char(char, key_char):
    return chr(ord(char) ^ ord(key_char))

def encrypt(plain_text, key):
    encrypted_str = ''
    for i in range(len(plain_text)): encrypted_str += encrypt_char(plain_text[i], key[i % len(key)])
    return encrypted_str

def decrypt(encrypted_text, key):
    decrypted_str = ''
    for i in range(len(encrypted_text)): decrypted_str += decrypt_char(encrypted_text[i], key[i % len(key)])
    return decrypted_str

def encryptvig(message, key):
    encrypted_text = []
    for i in range(len(message)):
        x = (ord(message[i]) + ord(key[i % len(key)])) % 26
        x += ord('a')
        encrypted_text.append(chr(x))
    return "".join(encrypted_text)

def decryptvig(encrypted_text, key):
    decrypted_text = []
    for i in range(len(encrypted_text)):
        x = (ord(encrypted_text[i]) - ord(key[i % len(key)]) + 26) % 26
        x += ord('a')
        decrypted_text.append(chr(x))
    return "".join(decrypted_text)

def testencryptvig():
    message = "teste"
    key = "key"
    encrypted = encryptvig(message, key)
    decrypted = decryptvig(encrypted, key)
    print(f"Message: {message}")
    print(f"Encrypted: {encrypted}")
    print(f"Decrypted: {decrypted}")

testencryptvig()