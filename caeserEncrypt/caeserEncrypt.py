RUSSIAN_ALPHABET_LOWER = "абвгдеёжзийклмнопрстуфхцчшщъыьэюя"
RUSSIAN_ALPHABET_UPPER = "АБВГДЕЁЖЗИЙКЛМНОПРСТУФХЦЧШЩЪЫЬЭЮЯ"
ENGLISH_ALPHABET_LOWER = "abcdefghijklmnopqrstuvwxyz"
ENGLISH_ALPHABET_UPPER = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
numbers_all = "0123456789"

ALPHABETS = {
    **{char: RUSSIAN_ALPHABET_LOWER for char in RUSSIAN_ALPHABET_LOWER},
    **{char: RUSSIAN_ALPHABET_UPPER for char in RUSSIAN_ALPHABET_UPPER},
    **{char: ENGLISH_ALPHABET_LOWER for char in ENGLISH_ALPHABET_LOWER},
    **{char: ENGLISH_ALPHABET_UPPER for char in ENGLISH_ALPHABET_UPPER},
    **{char: numbers_all for char in numbers_all},
}


def shift_char(char, shift_size):
    if char in ALPHABETS:
        alphabet = ALPHABETS[char]
        idx = alphabet.index(char)
        print(f"idx - {idx}, shift_size - {shift_size}, len - {len(alphabet)}")
        return alphabet[(idx + shift_size) % len(alphabet)]
    return char


def caesar_cipher(text, shift_size):
    return ''.join(shift_char(char, shift_size) for char in text)


# Пример использования
text = input("Введите слово для шифра: ")
shift_size = int(input("Введите число для смещения: "))

encrypted = caesar_cipher(text, shift_size)
decrypted = caesar_cipher(encrypted, -shift_size)

print(f"Original: {text}")
print(f"Encrypted: {encrypted}")
print(f"Decrypted: {decrypted}")
