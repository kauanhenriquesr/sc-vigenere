from frequency import frequency
from cypher.cypher_decypher import encrypt, decrypt
from collections import Counter

PORTUGUESE_FREQUENCY = {
    'a': 14.63, 'b': 1.04, 'c': 3.88, 'd': 4.99, 'e': 12.57, 'f': 1.02, 'g': 1.30,
    'h': 1.28, 'i': 6.18, 'j': 0.40, 'k': 0.02, 'l': 2.78, 'm': 4.74, 'n': 5.05,
    'o': 10.73, 'p': 2.52, 'q': 1.20, 'r': 6.53, 's': 7.81, 't': 4.34, 'u': 4.63,
    'v': 1.67, 'w': 0.01, 'x': 0.21, 'y': 0.01, 'z': 0.47, ' ': 15.00
}

ENGLISH_FREQUENCY = {
    'a': 8.167, 'b': 1.492, 'c': 2.782, 'd': 4.253, 'e': 12.702, 'f': 2.228,
    'g': 2.015, 'h': 6.094, 'i': 6.966, 'j': 0.153, 'k': 0.772, 'l': 4.025,
    'm': 2.406, 'n': 6.749, 'o': 7.507, 'p': 1.929, 'q': 0.095, 'r': 5.987,
    's': 6.327, 't': 9.056, 'u': 2.758, 'v': 0.978, 'w': 2.360, 'x': 0.150,
    'y': 1.974, 'z': 0.074, ' ': 15.00
}

def index_of_coincidence(text):
    counts = histogram(text)
    L = len(text)
    if L <= 1:
        return 0.0
    return sum((count / L) ** 2 for count in counts.values())

def histogram(text):
    dictionary = {}
    for c in range(256):
        dictionary[c] = 0
    for char in text:
        dictionary[ord(char)] += 1/256

    print(dictionary)
    return dictionary

def find_key_length(text, max_key_length=30):
    ic_scores = {}
    for key_length in range(1, max_key_length + 1):
        groups = [text[i::key_length] for i in range(key_length)]
        avg_ic = sum(index_of_coincidence(g) for g in groups) / key_length
        ic_scores[key_length] = avg_ic

    return sorted(ic_scores, key=lambda k: ic_scores[k], reverse=True)
    

texto_original ="""
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
chave = "papajorgeocurioso"  # chave de tamanho 5
find_key_length(texto_original)
encrypted = encrypt(texto_original, chave)

found_key_length = find_key_length(encrypted)

print(f"Texto original: '{texto_original}'")
print(f"Chave usada: '{chave}'")
print(f"Texto cifrado: '{encrypted}'")

print(f"\nChave encontrada: '{found_key_length}'")
# Verifica se a chave está correta
print(f"\nChave original: '{chave}'")
print(f"Chave encontrada está correta? {'Sim' if found_key_length == chave else 'Não'}")