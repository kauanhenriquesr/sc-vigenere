"""Main entry point for the cryptanalysis application."""

# Import the necessary functions from the new modules
from src.cipher import encrypt
from src.cryptanalysis import crack_vigenere


def run_demonstration(language: str, key: str, filepath: str):
    """Runs the full encryption and cracking demonstration for a given language."""

    print("\n" + "="*50)
    print(f" DEMONSTRAÇÃO PARA O IDIOMA: {language.upper()} ".center(50, "="))
    print("="*50)

    try:
        with open(filepath, "r", encoding='utf-8') as file:
            plain_text = file.read()
    except FileNotFoundError:
        print(f"Erro: Arquivo '{filepath}' não encontrado.")
        return

    # Encrypt the plaintext.
    encrypted_text = encrypt(plain_text, key)
    print(f"\nTexto original carregado: {len(plain_text)} caracteres")
    print(f"Chave usada: '{key}'")

    # Attempt to crack the cipher.
    result = crack_vigenere(encrypted_text, language=language)

    print("\n=== RESULTADO FINAL ===")
    print(f"Chave descoberta: '{result['key']}'")
    print(f"Chave original:   '{key}'")
    print(f"Sucesso: {'SIM' if result['key'] == key else 'PARCIAL'}")
    print("\nTexto descriptografado (amostra):")
    decrypted_text = result['decrypted']
    print(decrypted_text[:200] +
          "..." if len(decrypted_text) > 200 else decrypted_text)


def main():
    """Main function to demonstrate the integrated cryptanalysis for multiple languages."""

    # --- Demonstration for Portuguese ---
    run_demonstration(
        language='pt',
        key="segredo",
        filepath="assets/exemplopt.txt"
    )

    # --- Demonstration for English ---
    run_demonstration(
        language='en',
        key="secret",
        filepath="assets/exemploen.txt"
    )


if __name__ == "__main__":
    main()
