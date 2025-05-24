"""main module"""

from collections import Counter


def index_of_coincidence(text):
    """Calculates the Index of Coincidence (IC) for a given text."""

    n = len(text)

    if n <= 1:
        return 0

    counter = Counter(text)

    return sum(count * (count - 1) for count in counter.values()) / (n * (n - 1))


def find_key_length(ciphertext, max_length=15):
    """
    Estimates the most probable key length(s) of a polyalphabetic cipher (like Vigenère)
    by calculating the average Index of Coincidence for different key lengths.
    """
    ic_scores = {}

    for key_length in range(1, max_length + 1):
        groups = [ciphertext[i::key_length] for i in range(key_length)]

        avg_ic = sum(index_of_coincidence(group)
                     for group in groups if group) / key_length

        ic_scores[key_length] = avg_ic

    # Return the top 3 key lengths with the highest average IC scores.
    return sorted(ic_scores.items(), key=lambda x: x[1], reverse=True)[:3]


def crack_key_position(cipher_group):
    """Find the key character for a specific position using advanced frequency analysis"""

    # Expected relative frequencies of letters in Portuguese (source: pt.wikipedia.org)
    portuguese_letter_freq = {
        'a': 14.63, 'b': 1.04, 'c': 3.88, 'd': 4.99, 'e': 12.57, 'f': 1.02, 'g': 1.30,
        'h': 1.28, 'i': 6.18, 'j': 0.40, 'k': 0.02, 'l': 2.78, 'm': 4.74, 'n': 5.05,
        'o': 10.73, 'p': 2.52, 'q': 1.20, 'r': 6.53, 's': 7.81, 't': 4.34, 'u': 4.63,
        'v': 1.67, 'w': 0.01, 'x': 0.21, 'y': 0.01, 'z': 0.47
    }

    # Estimated frequencies for common special characters in Portuguese.
    special_chars_freq = {
        ' ': 15.0,    # Space is very frequent
        '.': 0.5,     # Period
        ',': 0.3,     # Comma
        '\n': 0.2,    # Newline
        '!': 0.1,     # Exclamation mark
        '?': 0.1,     # Question mark
        ':': 0.1,     # Colon
        ';': 0.05     # Semicolon
    }

    # Combine letter and special character frequencies for a comprehensive expected distribution.
    expected_freq = {**portuguese_letter_freq, **special_chars_freq}

    best_key_char = None
    # Initialize with negative infinity to find the maximum score.
    best_score = float('-inf')

    for key_byte in range(256):
        # Decrypt the cipher group using the current trial key_byte (XOR operation).
        decrypted = ''.join(chr(ord(c) ^ key_byte) for c in cipher_group)

        # Calculate observed character frequencies in the decrypted text.
        char_count = Counter(decrypted.lower())

        total_chars = len(decrypted)

        observed_freq = {char: (count / total_chars) *
                         100 for char, count in char_count.items()}

        # Calculate a score based on multiple criteria.
        score = 0

        # 1. Score based on expected frequencies (modified chi-squared approach).
        #    A lower chi-squared value (smaller difference from expected) is better.
        chi_squared = 0
        for char, expected in expected_freq.items():
            observed = observed_freq.get(char, 0)

            # Avoid division by zero for characters not in expected_freq
            if expected > 0:
                diff = abs(observed - expected)
                chi_squared += diff**2 / expected

        # Convert chi-squared to a positive score: higher score for lower chi-squared.
        # 100 is an arbitrary baseline; max(0, ...) ensures score isn't negative.
        frequency_score = max(0, 100 - chi_squared)
        score += frequency_score

        # 2. Bonus for high frequency of very common characters (e.g., 'a', 'e', 'o', space).
        for char in ['a', 'e', 'o', ' ']:
            if char in observed_freq:
                # Bonus proportional to frequency.
                score += observed_freq[char] * 0.5

        # 3. Penalties for undesirable characteristics.
        penalties = 0

        # Penalize non-printable characters.
        non_printable_count = sum(1 for c in decrypted if not c.isprintable())
        penalties += non_printable_count * 10

        # Penalize specific control characters (excluding common whitespace like newline, tab).
        control_chars = sum(1 for c in decrypted if ord(c)
                            < 32 and c not in ['\n', '\t'])
        penalties += control_chars * 15

        # Penalize highly anomalous frequencies of rare characters.
        rare_chars_penalty = 0
        for char, freq in observed_freq.items():
            if char.isalpha() and char in portuguese_letter_freq:
                expected = portuguese_letter_freq[char]

                # If observed frequency is much higher than expected for rare letters.
                if expected < 2.0 and freq > expected * 5:
                    rare_chars_penalty += (freq - expected) * 2

        penalties += rare_chars_penalty

        # Penalize if the proportion of alphabetic characters is too low.
        alpha_ratio = sum(1 for c in decrypted if c.isalpha()) / total_chars

        # Assuming at least 60% should be letters.
        if alpha_ratio < 0.6:
            penalties += (0.6 - alpha_ratio) * 50

        # Calculate the final score for this key_byte.
        final_score = score - penalties

        # If this key_byte yields a better score, update the best key character.
        if final_score > best_score:
            best_score = final_score
            best_key_char = chr(key_byte)

    return best_key_char


def analyze_frequency_match(text, show_details=False):
    """
    Analyzes how well the character frequencies in the given text match
    standard Portuguese frequencies. Calculates a chi-squared statistic and a quality score.
    """

    # Expected frequencies for Portuguese letters and space.
    portuguese_freq = {
        'a': 14.63, 'e': 12.57, ' ': 15.0, 'o': 10.73, 's': 7.81, 'r': 6.53,
        'i': 6.18, 'n': 5.05, 'd': 4.99, 'm': 4.74, 'u': 4.63, 't': 4.34,
        'c': 3.88, 'l': 2.78, 'p': 2.52, 'v': 1.67, 'g': 1.30, 'h': 1.28,
        'q': 1.20, 'b': 1.04, 'f': 1.02, 'z': 0.47, 'j': 0.40, 'x': 0.21
    }

    # Calculate observed frequencies in the input text.
    char_count = Counter(text.lower())
    total = len(text)
    observed_freq = {char: (count / total) * 100 for char,
                     count in char_count.items()}

    chi_squared = 0
    matches = 0

    for char in portuguese_freq:
        expected = portuguese_freq[char]
        observed = observed_freq.get(char, 0)

        if expected > 0:
            chi_squared += ((observed - expected) ** 2) / expected

        # Count "approximate matches" (observed within 50% of expected frequency).
        if abs(observed - expected) <= expected * 0.5:
            matches += 1

    # Quality score: proportion of characters that approximately match expected frequencies.
    quality_score = matches / len(portuguese_freq)

    if show_details:
        print(f"\n--- Análise de Frequência ---")
        print(f"Chi-quadrado: {chi_squared:.2f} (menor = melhor)")
        print(f"Score de qualidade: {quality_score:.3f}")
        print(f"Matches aproximados: {matches}/{len(portuguese_freq)}")

        print("\nTop 10 caracteres (Observado vs Esperado):")
        # Display comparison for the 10 most frequent expected characters.
        for char in list(portuguese_freq.keys())[:10]:
            obs = observed_freq.get(char, 0)
            exp = portuguese_freq[char]
            match_status = "✓" if abs(obs - exp) <= exp * 0.5 else "✗"
            print(f"  '{char}': {obs:5.2f}% vs {exp:5.2f}% {match_status}")

    return quality_score, chi_squared


def crack_vigenere(ciphertext):
    """Attempts to crack a Vigenère-like XOR cipher."""

    print("=== INICIANDO CRIPTOANÁLISE AVANÇADA ===")

    # 1. Find probable key lengths.
    key_lengths = find_key_length(ciphertext)
    print("Tamanhos prováveis da chave:")
    for length, ic in key_lengths:
        print(f"  {length}: IC = {ic:.4f}")

    results = []  # To store results for each tested key length.

    # 2. Attempt to crack for each probable key length.
    for key_length, ic in key_lengths:
        print(f"\n--- Testando chave de tamanho {key_length} ---")

        # Divide ciphertext into groups based on key position.
        groups = [ciphertext[i::key_length] for i in range(key_length)]

        # Find each character of the key.
        key_chars = []
        for i, group in enumerate(groups):
            if group:
                key_char = crack_key_position(group)
                key_chars.append(key_char)
                print(
                    f"  Posição {i}: '{key_char}' (grupo de {len(group)} chars)")
            else:
                key_chars.append('?')

        key = ''.join(key_chars)

        original_candidate_key = key
        for l in range(1, len(key) // 2 + 1):
            if len(key) % l == 0:
                substring = key[:l]
                repetitions = len(key) // l

                if substring * repetitions == key:
                    print(
                        f"      -> Chave candidata '{original_candidate_key}' simplificada para '{substring}'")
                    key = substring
                    break

        # Decrypt the ciphertext with the derived candidate key.
        decrypted = decrypt(ciphertext, key)

        # Advanced quality analysis of the decrypted text.
        quality_score, chi_squared = analyze_frequency_match(decrypted)

        # Evaluate readability: percentage of "valid" characters (printable, alpha, space, common punctuation).
        readable = sum(1 for c in decrypted if c.isprintable()
                       and (c.isalpha() or c.isspace() or c in '.,!?'))
        readability = readable / len(decrypted)

        # Combined score to rank results: weights quality, readability, and original IC for key length.
        combined_score = (quality_score * 0.6) + \
            (readability * 0.4) + (ic * 0.1)

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

    # 3. Return the best result based on the combined score.
    best = max(results, key=lambda x: x['combined_score'])
    print("\n" + "="*60)
    print("MELHOR RESULTADO:")
    print("="*60)
    print(f"Chave encontrada: '{best['key']}'")
    print(f"Tamanho: {best['key_length']}")
    print(f"Score combinado: {best['combined_score']:.3f}")

    # Show detailed frequency analysis for the best decrypted text.
    analyze_frequency_match(best['decrypted'], show_details=True)

    return best


def decrypt(encrypted_text, key):
    """Decrypts a string using the XOR cipher with a key"""

    decrypted_str = ''
    for i in range(len(encrypted_text)):
        # Decrypts each character of the encrypted text
        # using the corresponding character from the key (repeating the key if necessary)
        decrypted_str += chr(ord(encrypted_text[i]) ^ ord(key[i % len(key)]))

    return decrypted_str


def encrypt(plain_text, key):
    """Encrypts a string using the XOR cipher with a key"""

    encrypted_str = ''
    for i in range(len(plain_text)):
        # Encrypts each character of the original text
        # using the corresponding character from the key (repeating the key if necessary)
        encrypted_str += chr(ord(plain_text[i]) ^ ord(key[i % len(key)]))

    return encrypted_str


def frequency(string):
    """Simplified version of a frequency function."""
    counter = Counter(string)
    total = len(string)
    freq_dict = {}

    for char, count in counter.most_common():
        percentage = (count / total) * 100
        freq_dict[percentage] = [(hex(ord(char)), char, count)]

    return freq_dict


def main():
    """Main function to demonstrate the integrated cryptanalysis."""

    print("===== VIGENÈRE CIPHER - ANÁLISE E QUEBRA =====")

    try:
        # Attempt to load plaintext from a file. Adapt path as needed.
        # Ensure 'assets/exemplopt.txt' exists or change the path.
        with open("assets/exemplopt.txt", "r", encoding='utf-8') as file:
            plain_text = file.read()

        # Define the encryption key.
        key = "kháé"

        # Encrypt the plaintext.
        encrypted_text = encrypt(plain_text, key)
        print(f"\nTexto original carregado: {len(plain_text)} caracteres")
        print(f"Chave usada: '{key}'")
        print(f"Texto cifrado: {encrypted_text[:100]}...")

        # # Perform frequency analysis on the ciphertext
        # print("\n=== ANÁLISE DE FREQUÊNCIA ===")
        # freq_encrypted = frequency(encrypted_text)
        # print(f"Frequência: '{freq_encrypted}'")

        # Attempt to crack the cipher.
        print("\n=== TENTATIVA DE QUEBRA ===")
        result = crack_vigenere(encrypted_text)

        print("\n=== RESULTADO FINAL ===")
        print(f"Chave descoberta: '{result['key']}'")
        print(f"Chave original:   '{key}'")
        print(f"Sucesso: {'SIM' if result['key'] == key else 'PARCIAL'}")
        print("\nTexto descriptografado:")
        print(result['decrypted'][:200] +
              "..." if len(result['decrypted']) > 200 else result['decrypted'])

    except FileNotFoundError:
        print("Arquivo não encontrado! Testando com exemplo...")

        # Example test
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
