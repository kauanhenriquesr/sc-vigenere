"""Módulo para teste de implementação"""

import string

from collections import Counter
from unidecode import unidecode

PORTUGUESE_FREQUENCY = {
    'a': 14.63, 'b': 1.04, 'c': 3.88, 'd': 4.99, 'e': 12.57, 'f': 1.02, 'g': 1.30,
    'h': 1.28, 'i': 6.18, 'j': 0.40, 'k': 0.02, 'l': 2.78, 'm': 4.74, 'n': 5.05,
    'o': 10.73, 'p': 2.52, 'q': 1.20, 'r': 6.53, 's': 7.81, 't': 4.34, 'u': 4.63,
    'v': 1.67, 'w': 0.01, 'x': 0.21, 'y': 0.01, 'z': 0.47
}


def normalize_text(text):
    """Função que normaliza o texto"""

    # Converte o texto para unicode
    text = unidecode(text)

    # Converte para minúsculo
    text = text.lower()

    # Cria um dicionário com as letras em ASCII
    allowed = set(string.ascii_lowercase)

    # Mantém apenas as letras que estão em allowed
    text = ''.join(c for c in text if c in allowed)

    # Retorna o texto normalizado
    return text


def encryptvig(message, key):
    """Função que aplica a cifragem de Vigenere"""

    encrypted_text = []
    for i, _ in enumerate(message):
        x = (ord(_) + ord(key[i % len(key)]) - 2 * ord('a')) % 26
        x += ord('a')
        encrypted_text.append(chr(x))
    return "".join(encrypted_text)


def decryptvig(encrypted_text, key):
    """Função que aplica a decifragem de Vigenere"""

    decrypted_text = []
    for i, _ in enumerate(encrypted_text):
        x = (ord(_) - ord(key[i % len(key)]) + 26) % 26
        x += ord('a')
        decrypted_text.append(chr(x))
    return "".join(decrypted_text)


def index_of_coincidence(text):
    """Função que define o IC (Índice de Coincidência)"""

    freq = Counter(text)
    n = len(text)
    if n <= 1:
        return 0.0
    return sum(f * (f - 1) for f in freq.values()) / (n * (n - 1))


def find_key_length(text, max_key_length=30):
    """Função que busca o tamanho da chave"""

    ic_scores = {}
    for key_length in range(1, max_key_length + 1):
        groups = [text[i::key_length] for i in range(key_length)]
        avg_ic = sum(index_of_coincidence(g) for g in groups) / key_length
        ic_scores[key_length] = avg_ic
    return sorted(ic_scores, key=lambda k: ic_scores[k], reverse=True)


def break_vigenere(cipher_text, key_length, language_frequency):
    """Função que quebra o algoritmo de Vigenere"""

    key = ""
    for i in range(key_length):
        group = cipher_text[i::key_length]
        scores = {}

        for shift in range(26):
            decrypted = ''.join(
                chr(((ord(c) - ord('a') - shift) % 26) + ord('a'))
                for c in group
            )
            freq = Counter(decrypted)
            total = sum(freq.values())
            chi_squared = 0.0

            for letter in language_frequency:
                expected = language_frequency[letter] * total / 100
                observed = freq.get(letter, 0)
                chi_squared += ((observed - expected) ** 2) / \
                    expected if expected != 0 else 0

            scores[shift] = chi_squared

        best_shift = min(scores, key=scores.get)
        key += chr(best_shift + ord('a'))

    return key


if __name__ == "__main__":
    TEXTO_ORIGINAL = """
    teste de texto gigante para testar o algoritmo de vigenere e com isso a gente vai conseguir ver a frequencia apropriada do texto. Porém contudo entretanto a gente vai testar cada vez mais, para o indice de recorrência aumentar. O rato roeu a roupa do rei de roma. A cifra de vigenere é interessante para estudos criptográficos.
    O que deve ser entregue: o código fonte e seu executável (link para repositório), descritivo (4 pg 
    max) da cifra com sua implementação e do ataque e sua implementação. 
    Data de Entrega: 23/05/2023, até 10h. Instruções de entrega serão divulgadas oportunamente. 
    Apresentações: a partir de 27/05/2023 
    Links úteis 
    I - Funcionamento da cifra de Vigenere:
    Em uma vila escondida entre montanhas e florestas densas, vivia um velho relojoeiro chamado Elias. Ele era conhecido por consertar qualquer tipo de relógio, desde os mais simples até os mais antigos e misteriosos. Mas havia um em especial, guardado em uma caixa de madeira escura empoeirada, que ele jamais deixava ninguém tocar.
    Diziam que aquele relógio era mágico.
    Certo dia, uma menina chamada Clara entrou na relojoaria com um pedido incomum.
    Em uma vila escondida entre montanhas e florestas densas, vivia um velho relojoeiro chamado Elias. Ele era conhecido por consertar qualquer tipo de relógio, desde os mais simples até os mais antigos e misteriosos. Mas havia um em especial, guardado em uma caixa de madeira escura empoeirada, que ele jamais deixava ninguém tocar.
    Diziam que aquele relógio era mágico.
    Certo dia, uma menina chamada Clara entrou na relojoaria com um pedido incomum.
    """

    CHAVE = "papajorgeocurioso"

    # Normalizar o texto (sem acento, sem espaços, só letras a-z)
    TEXTO_NORMALIZADO = normalize_text(TEXTO_ORIGINAL)
    CHAVE_NORMALIZADA = normalize_text(CHAVE)

    # Cifrar
    ENCRYPTED = encryptvig(TEXTO_NORMALIZADO, CHAVE_NORMALIZADA)

    # Estimar o tamanho da chave
    tamanho_estimado = find_key_length(ENCRYPTED)[0]

    # Quebrar a cifra
    chave_quebrada = break_vigenere(
        ENCRYPTED, tamanho_estimado, PORTUGUESE_FREQUENCY)

    # Decifrar com a chave quebrada
    TEXTO_DECRIPTADO = decryptvig(ENCRYPTED, chave_quebrada)

    # Resultados
    print(f"Chave real:        {CHAVE_NORMALIZADA}")
    print(f"Tamanho estimado:  {tamanho_estimado}")
    print(f"Chave quebrada:    {chave_quebrada}")
    print(f"\nTexto original:    {TEXTO_NORMALIZADO[:100]}...")
    print(f"Texto decriptado:  {TEXTO_DECRIPTADO[:100]}...")
