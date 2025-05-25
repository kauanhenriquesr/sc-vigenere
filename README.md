# Criptoanálise da Cifra de Vigenère

Este programa implementa a cifra de Vigenère com funcionalidades de criptografia, descriptografia e criptoanálise (quebra da cifra). O sistema suporta textos em português e inglês.

## Requisitos

- Python 3.x

## Como Usar

O programa pode ser executado:

### 1. Para criptografar um arquivo
```bash
python __main__.py --crypt <caminho_do_arquivo> <String da chave>
```
Exemplo:
```bash
python __main__.py --crypt assets/exemplopt.txt chave
```

### 2. Descriptografar um arquivo
```bash
python __main__.py --decrypt <caminho_do_arquivo> <String da Chave>
```
Exemplo:
```bash
python __main__.py --decrypt assets/exemplopt.txt chave
```

### 3. Quebrar uma cifra
```bash
python __main__.py --crack <caminho_do_arquivo> <pt ou en>
```
Exemplo:
```bash
python __main__.py --crack assets/exemplopt.txt pt
```

### 4. Ver ajuda
```bash
python __main__.py --help
```