from collections import Counter

def index_of_coincidence(text):
    """Calcula o índice de coincidência para determinar tamanho da chave"""
    n = len(text)
    if n <= 1: return 0
    counter = Counter(text)
    return sum(count * (count - 1) for count in counter.values()) / (n * (n - 1))

def find_key_length(ciphertext, max_length=15):
    """Encontra o tamanho mais provável da chave usando IC"""
    ic_scores = {}
    for key_length in range(1, max_length + 1):
        groups = [ciphertext[i::key_length] for i in range(key_length)]
        avg_ic = sum(index_of_coincidence(group) for group in groups if group) / key_length
        ic_scores[key_length] = avg_ic
    
    # Retorna os 3 tamanhos mais prováveis (maior IC)
    return sorted(ic_scores.items(), key=lambda x: x[1], reverse=True)[:3]

def crack_key_position(cipher_group):
    """Encontra o caractere da chave para uma posição específica usando análise de frequência avançada"""
    
    # Frequências relativas das letras em português (pt.wikipedia.org)
    portuguese_letter_freq = {
        'a': 14.63, 'b': 1.04, 'c': 3.88, 'd': 4.99, 'e': 12.57, 'f': 1.02, 'g': 1.30,
        'h': 1.28, 'i': 6.18, 'j': 0.40, 'k': 0.02, 'l': 2.78, 'm': 4.74, 'n': 5.05,
        'o': 10.73, 'p': 2.52, 'q': 1.20, 'r': 6.53, 's': 7.81, 't': 4.34, 'u': 4.63,
        'v': 1.67, 'w': 0.01, 'x': 0.21, 'y': 0.01, 'z': 0.47
    }
    
    # Caracteres especiais comuns em português
    special_chars_freq = {
        ' ': 15.0,    # Espaço é muito frequente
        '.': 0.5,     # Ponto final
        ',': 0.3,     # Vírgula  
        '\n': 0.2,    # Quebra de linha
        '!': 0.1,     # Exclamação
        '?': 0.1,     # Interrogação
        ':': 0.1,     # Dois pontos
        ';': 0.05     # Ponto e vírgula
    }
    
    # Combina todas as frequências esperadas
    expected_freq = {**portuguese_letter_freq, **special_chars_freq}
    
    best_key_char = None
    best_score = float('-inf')  # Usamos -inf para permitir scores negativos
    
    for key_byte in range(256):
        # Descriptografa o grupo com este byte da chave
        decrypted = ''.join(chr(ord(c) ^ key_byte) for c in cipher_group)
        
        # Calcula frequências observadas no texto descriptografado
        char_count = Counter(decrypted.lower())
        total_chars = len(decrypted)
        observed_freq = {char: (count / total_chars) * 100 for char, count in char_count.items()}
        
        # Calcula score usando múltiplos critérios
        score = 0
        
        # 1. Score baseado em frequências esperadas (chi-quadrado invertido)
        chi_squared = 0
        for char, expected in expected_freq.items():
            observed = observed_freq.get(char, 0)
            # Usa chi-quadrado modificado (menor diferença = melhor score)
            if expected > 0:
                diff = abs(observed - expected)
                chi_squared += diff**2 / expected
        
        # Converte chi-quadrado em score positivo (menor chi² = maior score)
        frequency_score = max(0, 100 - chi_squared)
        score += frequency_score
        
        # 2. Bonus para alta frequência de caracteres comuns
        for char in ['a', 'e', 'o', ' ']:
            if char in observed_freq:
                score += observed_freq[char] * 0.5  # Bonus proporcional à frequência
        
        # 3. Penalizações severas
        penalties = 0
        
        # Penaliza caracteres não-imprimíveis
        non_printable_count = sum(1 for c in decrypted if not c.isprintable())
        penalties += non_printable_count * 10
        
        # Penaliza caracteres de controle específicos
        control_chars = sum(1 for c in decrypted if ord(c) < 32 and c not in ['\n', '\t'])
        penalties += control_chars * 15
        
        # Penaliza frequências muito anômalas de caracteres raros
        rare_chars_penalty = 0
        for char, freq in observed_freq.items():
            if char.isalpha() and char in portuguese_letter_freq:
                expected = portuguese_letter_freq[char]
                # Se a frequência observada é muito maior que a esperada para letras raras
                if expected < 2.0 and freq > expected * 5:
                    rare_chars_penalty += (freq - expected) * 2
        
        penalties += rare_chars_penalty
        
        # Penaliza se não há caracteres alfabéticos suficientes
        alpha_ratio = sum(1 for c in decrypted if c.isalpha()) / total_chars
        if alpha_ratio < 0.6:  # Esperamos pelo menos 60% de letras
            penalties += (0.6 - alpha_ratio) * 50
        
        # Score final
        final_score = score - penalties
        
        if final_score > best_score:
            best_score = final_score
            best_key_char = chr(key_byte)
    
    return best_key_char

def analyze_frequency_match(text, show_details=False):
    """Analisa quão bem as frequências do texto coincidem com o português"""
    
    # Frequências esperadas em português
    portuguese_freq = {
        'a': 14.63, 'e': 12.57, ' ': 15.0, 'o': 10.73, 's': 7.81, 'r': 6.53,
        'i': 6.18, 'n': 5.05, 'd': 4.99, 'm': 4.74, 'u': 4.63, 't': 4.34,
        'c': 3.88, 'l': 2.78, 'p': 2.52, 'v': 1.67, 'g': 1.30, 'h': 1.28,
        'q': 1.20, 'b': 1.04, 'f': 1.02, 'z': 0.47, 'j': 0.40, 'x': 0.21
    }
    
    # Calcula frequências observadas
    char_count = Counter(text.lower())
    total = len(text)
    observed_freq = {char: (count / total) * 100 for char, count in char_count.items()}
    
    # Calcula chi-quadrado
    chi_squared = 0
    matches = 0
    
    for char in portuguese_freq:
        expected = portuguese_freq[char]
        observed = observed_freq.get(char, 0)
        
        if expected > 0:
            chi_squared += ((observed - expected) ** 2) / expected
            
        # Conta "matches" aproximados (dentro de 50% da frequência esperada)
        if abs(observed - expected) <= expected * 0.5:
            matches += 1
    
    # Score de qualidade (0-1, sendo 1 = perfeito)
    quality_score = matches / len(portuguese_freq)
    
    if show_details:
        print(f"\n--- Análise de Frequência ---")
        print(f"Chi-quadrado: {chi_squared:.2f} (menor = melhor)")
        print(f"Score de qualidade: {quality_score:.3f}")
        print(f"Matches aproximados: {matches}/{len(portuguese_freq)}")
        
        print("\nTop 10 caracteres (Observado vs Esperado):")
        for char in list(portuguese_freq.keys())[:10]:
            obs = observed_freq.get(char, 0)
            exp = portuguese_freq[char]
            match_status = "✓" if abs(obs - exp) <= exp * 0.5 else "✗"
            print(f"  '{char}': {obs:5.2f}% vs {exp:5.2f}% {match_status}")
    
    return quality_score, chi_squared

def crack_vigenere(ciphertext):
    """Quebra a cifra de Vigenère XOR com análise detalhada"""
    print("=== INICIANDO CRIPTOANÁLISE AVANÇADA ===")
    
    # 1. Encontra tamanhos prováveis da chave
    key_lengths = find_key_length(ciphertext)
    print("Tamanhos prováveis da chave:")
    for length, ic in key_lengths:
        print(f"  {length}: IC = {ic:.4f}")
    
    results = []
    
    # 2. Tenta quebrar para cada tamanho provável
    for key_length, ic in key_lengths:
        print(f"\n--- Testando chave de tamanho {key_length} ---")
        
        # Divide texto em grupos por posição da chave
        groups = [ciphertext[i::key_length] for i in range(key_length)]
        
        # Encontra cada caractere da chave
        key_chars = []
        for i, group in enumerate(groups):
            if group:
                key_char = crack_key_position(group)
                key_chars.append(key_char)
                print(f"  Posição {i}: '{key_char}' (grupo de {len(group)} chars)")
            else:
                key_chars.append('?')
        
        key = ''.join(key_chars)
        
        # Testa a descriptografia
        decrypted = decrypt(ciphertext, key)
        
        # Análise de qualidade avançada
        quality_score, chi_squared = analyze_frequency_match(decrypted)
        
        # Avalia legibilidade (% de caracteres válidos)
        readable = sum(1 for c in decrypted if c.isprintable() and (c.isalpha() or c.isspace() or c in '.,!?'))
        readability = readable / len(decrypted)
        
        # Score combinado
        combined_score = (quality_score * 0.6) + (readability * 0.4) + (ic * 0.1)
        
        results.append({
            'key': key,
            'key_length': key_length,
            'quality_score': quality_score,
            'readability': readability,
            'combined_score': combined_score,
            'chi_squared': chi_squared,
            'decrypted': decrypted,
            'ic': ic
        })
        
        print(f"  Chave: '{key}'")
        print(f"  Qualidade freq: {quality_score:.3f}")
        print(f"  Legibilidade: {readability:.3f}")
        print(f"  Score total: {combined_score:.3f}")
        print(f"  Preview: {decrypted[:80]}...")
    
    # 3. Retorna o melhor resultado
    best = max(results, key=lambda x: x['combined_score'])
    print("\n" + "="*60)
    print("MELHOR RESULTADO:")
    print("="*60)
    print(f"Chave encontrada: '{best['key']}'")
    print(f"Tamanho: {best['key_length']}")
    print(f"Score combinado: {best['combined_score']:.3f}")
    
    # Análise detalhada do melhor resultado
    analyze_frequency_match(best['decrypted'], show_details=True)
    
    return best

# Integração com suas funções existentes
def decrypt(encrypted_text, key):
    """Sua função original de descriptografia"""
    decrypted_str = ''
    for i in range(len(encrypted_text)): 
        decrypted_str += chr(ord(encrypted_text[i]) ^ ord(key[i % len(key)]))
    return decrypted_str

def encrypt(plain_text, key):
    """Sua função original de criptografia"""
    encrypted_str = ''
    for i in range(len(plain_text)): 
        encrypted_str += chr(ord(plain_text[i]) ^ ord(key[i % len(key)]))
    return encrypted_str

def frequency(string):
    """Versão simplificada da sua função de frequência"""
    counter = Counter(string)
    total = len(string)
    freq_dict = {}
    
    for char, count in counter.most_common():
        percentage = (count / total) * 100
        freq_dict[percentage] = [(hex(ord(char)), char, count)]
    
    return freq_dict

# Função principal integrada
def main():
    print("===== VIGENÈRE CIPHER - ANÁLISE E QUEBRA =====")
    
    try:
        # Carrega o arquivo (adapte o caminho conforme necessário)
        with open("assets/exemplopt.txt", "r", encoding='utf-8') as file:
            plain_text = file.read()
        
        # Sua chave original
        key = "kháé"
        
        # Criptografia
        encrypted_text = encrypt(plain_text, key)
        print(f"\nTexto original carregado: {len(plain_text)} caracteres")
        print(f"Chave usada: '{key}'")
        print(f"Texto cifrado: {encrypted_text[:100]}...")
        
        # Análise de frequência (seu código original)
        print("\n=== ANÁLISE DE FREQUÊNCIA ===")
        freq_encrypted = frequency(encrypted_text)
        
        # CRIPTOANÁLISE - QUEBRA DA CIFRA
        print("\n=== TENTATIVA DE QUEBRA ===")
        result = crack_vigenere(encrypted_text)
        
        print(f"\n=== RESULTADO FINAL ===")
        print(f"Chave descoberta: '{result['key']}'")
        print(f"Chave original:   '{key}'")
        print(f"Sucesso: {'SIM' if result['key'] == key else 'PARCIAL'}")
        print(f"\nTexto descriptografado:")
        print(result['decrypted'][:200] + "..." if len(result['decrypted']) > 200 else result['decrypted'])
        
    except FileNotFoundError:
        print("Arquivo não encontrado! Testando com exemplo...")
        
        # Exemplo de teste
        plain = "Este é um exemplo de texto em português para testar a criptoanálise."
        key = "TESTE"
        encrypted = encrypt(plain, key)
        
        print(f"Texto original: {plain}")
        print(f"Chave: {key}")
        print(f"Texto cifrado: {encrypted}")
        
        result = crack_vigenere(encrypted)
        print(f"\nChave descoberta: '{result['key']}'")
        print(f"Texto recuperado: {result['decrypted']}")

if __name__ == "__main__":
    main()