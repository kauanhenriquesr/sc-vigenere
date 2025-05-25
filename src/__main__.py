"""Main entry point for the cryptanalysis application."""

# Import the necessary functions from the new modules
from cipher import encrypt, decrypt
from cryptanalysis import crack_vigenere
import sys

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


def demo():
    """Main function to demonstrate the integrated cryptanalysis for multiple languages."""

    # --- Demonstration for Portuguese ---
    run_demonstration(
        language='pt',
        key="key",
        filepath="assets/exemplopt.txt"
    )

    # --- Demonstration for English ---
    run_demonstration(
        language='en',
        key="key",
        filepath="assets/exemploen.txt"
    )

def help():
    print("="*50)
    print("\nExemplos de uso do programa:")
    print(" - python __main__.py --crypt <filepath> <key>")
    print("     Para criptografar um arquivo com a chave 'key':")
    print("     Exemplo: python __main__.py --crypt assets/exemplopt.txt key\n")
    print(" - python __main__.py --decrypt <filepath> <key>")
    print("     Para descriptografar um arquivo com a chave 'key':")
    print("     Exemplo: python __main__.py --decrypt assets/exemplopt.txt key\n")
    print(" - python __main__.py --crack <filepath> <language>")
    print("     Para quebrar uma cifra com o idioma 'pt':")
    print("     Exemplo: python __main__.py --crack assets/exemplopt.txt pt\n")
    print(" - python __main__.py --help")
    print("     Para ver esta ajuda.")
    print("="*50)
    print()

if __name__ == "__main__":
    args = sys.argv[1:]
    if len(args) == 0 or args[0] not in ["--crypt", "--decrypt", "--crack", "--help"] or len(args) > 3:
        help()
        print("Deseja ver a demonstração exemplo do crack? [S/N]")
        if input().upper() == "S":
            print("Demonstração exemplo do crack de cifra para português e inglês...")
            demo()
            print("="*50)
            sys.exit(1)
    elif args[0] == "--help":
        help()
        sys.exit(1)
    elif args[0] == "--crypt" and len(args) == 3:
        print("Iniciando criptografia...\n")
        filepath = args[1]
        try:
            with open(filepath, "r", encoding='utf-8') as file:
                text = file.read()
        except:
            print(f"Erro: Arquivo '{filepath}' não encontrado.")
            sys.exit(1)
        key = args[2]
        encrypted_text = encrypt(text, key)
        print(encrypted_text)
        sys.exit(1)
    elif args[0] == "--decrypt" and len(args) == 3:
        print("Iniciando descriptografia...\n")
        filepath = args[1]
        try:
            with open(filepath, "r", encoding='utf-8') as file:
                text = file.read()
        except:
            print(f"Erro: Arquivo '{filepath}' não encontrado.")
            sys.exit(1)
        key = args[2]
        decrypted_text = decrypt(text, key)
        print(decrypted_text)
        sys.exit(1)
    elif args[0] == "--crack" and len(args) == 3:
        print("Iniciando quebra de cifra...")
        filepath = args[1]
        try:
            with open(filepath, "r", encoding='utf-8') as file:
                text = file.read()
        except:
            print
        language = args[2]
        if language not in ["pt", "en"]:
            print("Uso do programa: python __main__.py --crack <filepath> <language>\n")
            print("Linguagens disponíveis: pt, en\n")
            print("Exemplo: python __main__.py --crack assets/exemplopt.txt pt")
            sys.exit(1)
        result = crack_vigenere(text, language)
        print(result)
        sys.exit(1)