"""Module with all the cryptanalysis logic."""

from collections import Counter
# Imports the decrypt function from the neighboring module
from src.cipher import decrypt

# --- Language Frequency Maps ---

# Expected relative frequencies of letters in Portuguese (source: pt.wikipedia.org)
PORTUGUESE_FREQ = {
    'a': 14.63, 'b': 1.04, 'c': 3.88, 'd': 4.99, 'e': 12.57, 'f': 1.02, 'g': 1.30,
    'h': 1.28, 'i': 6.18, 'j': 0.40, 'k': 0.02, 'l': 2.78, 'm': 4.74, 'n': 5.05,
    'o': 10.73, 'p': 2.52, 'q': 1.20, 'r': 6.53, 's': 7.81, 't': 4.34, 'u': 4.63,
    'v': 1.67, 'w': 0.01, 'x': 0.21, 'y': 0.01, 'z': 0.47,
    ' ': 15.0, '.': 0.5, ',': 0.3, '\n': 0.2, '!': 0.1, '?': 0.1, ':': 0.1, ';': 0.05
}

# Expected relative frequencies of letters in English.
ENGLISH_FREQ = {
    'a': 8.167, 'b': 1.492, 'c': 2.782, 'd': 4.253, 'e': 12.702, 'f': 2.228,
    'g': 2.015, 'h': 6.094, 'i': 6.966, 'j': 0.153, 'k': 0.772, 'l': 4.025,
    'm': 2.406, 'n': 6.749, 'o': 7.507, 'p': 1.929, 'q': 0.095, 'r': 5.987,
    's': 6.327, 't': 9.056, 'u': 2.758, 'v': 0.978, 'w': 2.360, 'x': 0.150,
    'y': 1.974, 'z': 0.074,
    ' ': 13.0  # Space frequency is also high in English
}

# Master dictionary to select language profile
LANGUAGE_PROFILES = {
    'pt': PORTUGUESE_FREQ,
    'en': ENGLISH_FREQ
}

# --- Cryptanalysis Functions ---


def index_of_coincidence(text):
    """Calculates the Index of Coincidence (IC) for a given text."""
    n = len(text)
    if n <= 1:
        return 0
    counter = Counter(text)
    return sum(count * (count - 1) for count in counter.values()) / (n * (n - 1))


def find_key_length(ciphertext, max_length=15):
    """
    Estimates the most probable key length(s) by calculating the average IC.
    """
    ic_scores = {}
    for key_length in range(1, max_length + 1):
        groups = [ciphertext[i::key_length] for i in range(key_length)]
        avg_ic = sum(index_of_coincidence(group)
                     for group in groups if group) / key_length
        ic_scores[key_length] = avg_ic
    return sorted(ic_scores.items(), key=lambda x: x[1], reverse=True)[:3]


def crack_key_position(cipher_group, language='pt'):
    """Find the key character for a specific position using frequency analysis for the given language."""

    expected_freq = LANGUAGE_PROFILES.get(language, PORTUGUESE_FREQ)

    best_key_char = None
    best_score = float('-inf')

    for key_byte in range(256):
        decrypted = ''.join(chr(ord(c) ^ key_byte) for c in cipher_group)
        char_count = Counter(decrypted.lower())
        total_chars = len(decrypted)
        observed_freq = {char: (count / total_chars) *
                         100 for char, count in char_count.items()}

        score = 0
        chi_squared = 0
        for char, expected in expected_freq.items():
            observed = observed_freq.get(char, 0)
            if expected > 0:
                diff = abs(observed - expected)
                chi_squared += diff**2 / expected
        frequency_score = max(0, 100 - chi_squared)
        score += frequency_score

        penalties = 0
        non_printable_count = sum(1 for c in decrypted if not c.isprintable())
        penalties += non_printable_count * 10
        alpha_ratio = sum(1 for c in decrypted if c.isalpha()) / \
            total_chars if total_chars > 0 else 0
        if alpha_ratio < 0.6:
            penalties += (0.6 - alpha_ratio) * 50

        final_score = score - penalties
        if final_score > best_score:
            best_score = final_score
            best_key_char = chr(key_byte)

    return best_key_char


def analyze_frequency_match(text, language='pt', show_details=False):
    """
    Analyzes how well text frequencies match the standard for the given language.
    """
    lang_freq = LANGUAGE_PROFILES.get(language, PORTUGUESE_FREQ)

    char_count = Counter(text.lower())
    total = len(text)
    observed_freq = {char: (count / total) * 100 for char,
                     count in char_count.items()}
    chi_squared = 0
    matches = 0

    for char in lang_freq:
        expected = lang_freq[char]
        observed = observed_freq.get(char, 0)
        if expected > 0:
            chi_squared += ((observed - expected) ** 2) / expected
        if abs(observed - expected) <= expected * 0.5:
            matches += 1

    quality_score = matches / len(lang_freq)

    if show_details:
        print(f"\n--- Frequency Analysis ({language.upper()}) ---")
        print(f"Chi-squared: {chi_squared:.2f} (lower is better)")
        print(f"Quality Score: {quality_score:.3f}")
        print(f"Approximate Matches: {matches}/{len(lang_freq)}")

    return quality_score, chi_squared


def crack_vigenere(ciphertext, language='pt'):
    """Attempts to crack a Vigenère-like XOR cipher for a specific language."""
    print(f"=== INICIANDO CRIPTOANÁLISE (IDIOMA: {language.upper()}) ===")
    key_lengths = find_key_length(ciphertext)
    print("Prováveis tamanhos de chave:")
    for length, ic in key_lengths:
        print(f"  {length}: IC = {ic:.4f}")

    results = []
    for key_length, ic in key_lengths:
        print(f"\n--- Testando chave de tamanho {key_length} ---")
        groups = [ciphertext[i::key_length] for i in range(key_length)]
        key_chars = []
        for i, group in enumerate(groups):
            if group:
                key_char = crack_key_position(group, language=language)
                key_chars.append(key_char)
                print(
                    f"  Posição {i}: '{key_char}' (grupo de {len(group)} chars)")

        if not all(key_chars):
            continue

        key = ''.join(key_chars)

        # Checks if the found key is a repeating pattern (e.g., 'keykeykey') and simplifies it.
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

        decrypted = decrypt(ciphertext, key)
        quality_score, chi_squared = analyze_frequency_match(
            decrypted, language=language)

        readable = sum(1 for c in decrypted if c.isprintable()
                       and (c.isalpha() or c.isspace() or c in '.,!?'))
        readability = readable / len(decrypted) if len(decrypted) > 0 else 0
        combined_score = (quality_score * 0.6) + \
            (readability * 0.4) + (ic * 0.1)

        results.append({
            'key': key, 'decrypted': decrypted, 'combined_score': combined_score,
            'key_length': key_length
        })

    if not results:
        return {'key': '', 'decrypted': '', 'combined_score': -1, 'key_length': 0}

    best = max(results, key=lambda x: x['combined_score'])
    print("\n" + "="*60)
    print("MELHOR RESULTADO:")
    print(f"Chave encontrada: '{best['key']}'")
    print(f"Tamanho: {best['key_length']}")
    print(f"Score combinado: {best['combined_score']:.3f}")
    analyze_frequency_match(
        best['decrypted'], language=language, show_details=True)

    return best
