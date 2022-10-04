def encrypt_vigenere(plaintext: str, keyword: str) -> str:
    """
    Encrypts plaintext using a Vigenere cipher.

    >>> encrypt_vigenere("PYTHON", "A")
    'PYTHON'
    >>> encrypt_vigenere("python", "a")
    'python'
    >>> encrypt_vigenere("ATTACKATDAWN", "LEMON")
    'LXFOPVEFRNHR'
    """
    ciphertext = ""
    key_sequence = ""
    while len(key_sequence) < len(plaintext):
        key_sequence += keyword
    key_sequence = key_sequence[: len(plaintext)]
    for i in range(len(plaintext)):
        shift = ord(key_sequence[i]) - (65 if ord(key_sequence[i]) < 97 else 97)
        c = ord(plaintext[i])
        if ord("a") <= c <= ord("z"):  # ord(a) = 97 ord(z) = 122
            c = (c - 97 + shift) % 26 + 97
        if ord("A") <= c <= ord("Z"):  # ord(A) = 65 ord(Z) =
            c = (c - 65 + shift) % 26 + 65
        ciphertext += chr(c)
    return ciphertext


def decrypt_vigenere(ciphertext: str, keyword: str) -> str:
    """
    Decrypts a ciphertext using a Vigenere cipher.

    >>> decrypt_vigenere("PYTHON", "A")
    'PYTHON'
    >>> decrypt_vigenere("python", "a")
    'python'
    >>> decrypt_vigenere("LXFOPVEFRNHR", "LEMON")
    'ATTACKATDAWN'
    """
    plaintext = ""
    for i in range(len(ciphertext)):
        n = ord(ciphertext[i])
        g_shift = ord(keyword[i % len(keyword)])

        upc_s = 65
        upc_e = 65 + 25

        lwc_s = 97
        lwc_e = 97 + 25

        shift = 0
        if upc_s <= g_shift <= upc_e:
            shift = upc_e - g_shift + 1
        elif lwc_s <= g_shift <= lwc_e:
            shift = lwc_e - g_shift + 1

        if upc_s <= n <= upc_e:
            if n + shift > upc_e:
                n = upc_s + (n + shift) - upc_e - 1
            else:
                n += shift

        if lwc_s <= n <= lwc_e:
            if n + shift > lwc_e:
                n = lwc_s + (n + shift) - lwc_e - 1
            else:
                n += shift
        plaintext += chr(n)

    return plaintext
