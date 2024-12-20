# RUSSIAN_ALPHABET_LOWER = "абвгдеёжзийклмнопрстуфхцчшщъыьэюя"
# RUSSIAN_ALPHABET_UPPER = "АБВГДЕЁЖЗИЙКЛМНОПРСТУФХЦЧШЩЪЫЬЭЮЯ"
# ENGLISH_ALPHABET_LOWER = "abcdefghijklmnopqrstuvwxyz"
# ENGLISH_ALPHABET_UPPER = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
# numbers_all = "0123456789"
#
# ALPHABETS = {
#     **{char: RUSSIAN_ALPHABET_LOWER for char in RUSSIAN_ALPHABET_LOWER},
#     **{char: RUSSIAN_ALPHABET_UPPER for char in RUSSIAN_ALPHABET_UPPER},
#     **{char: ENGLISH_ALPHABET_LOWER for char in ENGLISH_ALPHABET_LOWER},
#     **{char: ENGLISH_ALPHABET_UPPER for char in ENGLISH_ALPHABET_UPPER},
#     **{char: numbers_all for char in numbers_all},
# }
#
#
# def shift_char(char, shift_size):
#     if char in ALPHABETS:
#         alphabet = ALPHABETS[char]
#         idx = alphabet.index(char)
#         print(f"idx - {idx}, shift_size - {shift_size}, len - {len(alphabet)}")
#         return alphabet[(idx + shift_size) % len(alphabet)]
#     return char
#
#
# def caesar_cipher(text, shift_size):
#     return ''.join(shift_char(char, shift_size) for char in text)
#
#
# # Пример использования
# text = input("Введите слово для шифра: ")
# shift_size = int(input("Введите число для смещения: "))
#
# encrypted = caesar_cipher(text, shift_size)
# decrypted = caesar_cipher(encrypted, -shift_size)
#
# print(f"Original: {text}")
# print(f"Encrypted: {encrypted}")
# print(f"Decrypted: {decrypted}")


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

# Частотное распределение букв для русского и английского языков
FREQUENCY_RU = {
    'о': 0.1118, 'е': 0.0875, 'а': 0.0764, 'и': 0.0709, 'н': 0.0678, 'т': 0.0609,
    'с': 0.0497, 'л': 0.0496, 'в': 0.0438, 'р': 0.0423, 'к': 0.033, 'м': 0.0317,
    'д': 0.0309, 'п': 0.0247, 'ы': 0.0236, 'у': 0.0222, 'б': 0.0201, 'я': 0.0196,
    'ь': 0.0184, 'г': 0.0172, 'з': 0.0148, 'ч': 0.014, 'й': 0.0121, 'ж': 0.0101,
    'х': 0.0095, 'ш': 0.0072, 'ю': 0.0047, 'ц': 0.0039, 'э': 0.0036, 'щ': 0.003,
    'ф': 0.0021, 'ё': 0.002, 'ъ': 0.0002
}

FREQUENCY_EN = {
    'e': 0.12702, 't': 0.09056, 'a': 0.08167, 'o': 0.07507, 'i': 0.06966, 'n': 0.06749,
    's': 0.06327, 'h': 0.06094, 'r': 0.05987, 'd': 0.04253, 'l': 0.04025, 'c': 0.02782,
    'u': 0.02758, 'm': 0.02406, 'w': 0.0236, 'f': 0.02228, 'g': 0.02015, 'y': 0.01974,
    'p': 0.01929, 'b': 0.01492, 'v': 0.00978, 'k': 0.00772, 'j': 0.00153, 'x': 0.0015,
    'q': 0.00095, 'z': 0.00074
}


def shift_char(char, shift_size):
    if char in ALPHABETS:
        alphabet = ALPHABETS[char]
        idx = alphabet.index(char)
        return alphabet[(idx + shift_size) % len(alphabet)]
    return char


def caesar_cipher(text, shift_size):
    return ''.join(shift_char(char, shift_size) for char in text)


def calculate_frequency(text, alphabet):
    counts = {}
    total_letters = len(text)

    for char in text:
        if char in alphabet:
            counts[char] = counts.get(char, 0) + 1

    return {char: count / total_letters for char, count in counts.items()}


def crack_caesar_cipher(text):
    text = text.lower()
    alphabet = RUSSIAN_ALPHABET_LOWER if any(c in RUSSIAN_ALPHABET_LOWER for c in text) else ENGLISH_ALPHABET_LOWER
    frequency_map = FREQUENCY_RU if alphabet == RUSSIAN_ALPHABET_LOWER else FREQUENCY_EN

    best_shift = None
    best_decrypted = None
    best_correlation = -float('inf')

    for shift in range(len(alphabet)):
        decrypted = caesar_cipher(text, -shift)
        freq = calculate_frequency(decrypted, alphabet)

        correlation = sum(frequency_map.get(char, 0) * freq.get(char, 0) for char in freq)

        if correlation > best_correlation:
            best_correlation = correlation
            best_shift = shift
            best_decrypted = decrypted

    return best_decrypted, best_shift


def main():
    while True:
        print("\nВыберите действие:")
        print("1. Зашифровать текст")
        print("2. Дешифровать текст")
        print("3. Взломать шифр через частотный анализ")
        print("4. Выход")

        choice = input("Введите номер действия: ")

        if choice == '1':
            text = input("Введите текст для шифрования: ")
            shift_size = int(input("Введите число для смещения: "))
            encrypted = caesar_cipher(text, shift_size)
            print(f"Зашифрованный текст: {encrypted}")

        elif choice == '2':
            text = input("Введите текст для дешифрования: ")
            shift_size = int(input("Введите число для смещения: "))
            decrypted = caesar_cipher(text, -shift_size)
            print(f"Дешифрованный текст: {decrypted}")

        elif choice == '3':
            text = input("Введите зашифрованный текст для взлома: ")
            decrypted, shift = crack_caesar_cipher(text)
            if decrypted:
                print(f"Взломано: {decrypted} (сдвиг: {shift})")
            else:
                print("Не удалось взломать шифр.")

        elif choice == '4':
            print("Выход из программы.")
            break

        else:
            print("Неверный выбор. Попробуйте снова.")


# Запуск программы
if __name__ == "__main__":
    main()

