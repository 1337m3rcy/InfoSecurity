import secrets

rc5_const = {
    16: (0xB7E1, 0x9E37),
    32: (0xB7E15163, 0x9E3779B9),
    64: (0xB7E151628AED2A6B, 0x9E3779B97F4A7C15),
}

class RC5:
    def __init__(self, w: int, r: int, key: bytes):
        self.w = w
        self.r = r
        self.key = key
        self.u = w // 8
        self.b = len(key)

        self.L = self._key_align(key)
        self._key_extend()
        self._mix()

    def _modular_add(self, a: int, b: int) -> int:
        return (a + b) % pow(2, self.w)

    def _modular_sub(self, a: int, b: int) -> int:
        return (a - b) % pow(2, self.w)

    def _left_rotate(self, x: int, n: int) -> int:
        n = n % self.w
        mod = pow(2, self.w)
        return ((x << n) & (mod - 1)) | (x >> (self.w - n))

    def _right_rotate(self, x: int, n: int) -> int:
        n = n % self.w
        mod = pow(2, self.w)
        return (x >> n) | ((x << (self.w - n)) & (mod - 1))

    def _key_align(self, key: bytes) -> list:
        padding = (self.u - len(key) % self.u) % self.u
        key += b"\x00" * padding

        return [
            int.from_bytes(key[i: i + self.u], "little")
            for i in range(0, len(key), self.u)
        ]

    def _key_extend(self) -> None:
        p, q = rc5_const[self.w]
        self.S = [p]
        for i in range(1, 2 * self.r + 2):
            self.S.append(self._modular_add(self.S[i - 1], q))

    def _mix(self) -> None:
        A = B = 0
        len_S = len(self.S)
        len_L = len(self.L)
        iterations = 3 * max(len_L, len_S)

        for i in range(iterations):
            idx_S = i % len_S
            idx_L = i % len_L

            A = self.S[idx_S] = self._left_rotate((self.S[idx_S] + A + B) % pow(2, self.w), 3)
            B = self.L[idx_L] = self._left_rotate((self.L[idx_L] + A + B) % pow(2, self.w), (A + B) % self.w)

    def encrypt_block(self, block: int) -> int:
        A = block >> self.w
        B = block & (pow(2, self.w) - 1)

        A = self._modular_add(A, self.S[0])
        B = self._modular_add(B, self.S[1])

        for i in range(1, self.r + 1):
            A = self._modular_add(self._left_rotate(A ^ B, B), self.S[2 * i])
            B = self._modular_add(self._left_rotate(B ^ A, A), self.S[2 * i + 1])

        return (A << self.w) | B

    def decrypt_block(self, block: int) -> int:
        A = block >> self.w
        B = block & (pow(2, self.w) - 1)

        for i in range(self.r, 0, -1):
            B = self._right_rotate(self._modular_sub(B, self.S[2 * i + 1]), A) ^ A
            A = self._right_rotate(self._modular_sub(A, self.S[2 * i]), B) ^ B

        A = self._modular_sub(A, self.S[0])
        B = self._modular_sub(B, self.S[1])

        return (A << self.w) | B

    def encrypt_message(self, iv: int, plaintext: str) -> str:
        encrypted = []
        iv = self.encrypt_block(iv)

        # Сохраняем длину сообщения
        plaintext_bytes = plaintext.encode("utf-8")
        length = len(plaintext_bytes)

        for i in range(0, length, self.u * 2):
            chunk = plaintext_bytes[i: i + self.u * 2]
            if len(chunk) < self.u * 2:
                chunk = chunk.ljust(self.u * 2, b"\x00")
            block = int.from_bytes(chunk, "little")
            cipher_block = self.encrypt_block(block ^ iv)
            encrypted.append(cipher_block.to_bytes(self.u * 2, "little"))
            iv = cipher_block

        return length.to_bytes(4, "little") + b"".join(encrypted)  # Включаем длину в начало

    def decrypt_message(self, iv: int, ciphertext: bytes) -> str:
        decrypted = []
        iv_encrypted = self.encrypt_block(iv)

        # Извлекаем длину исходного сообщения
        length = int.from_bytes(ciphertext[:4], "little")
        ciphertext = ciphertext[4:]

        for i in range(0, len(ciphertext), self.u * 2):
            chunk = ciphertext[i: i + self.u * 2]
            block = int.from_bytes(chunk, "little")
            decrypted_block = self.decrypt_block(block) ^ iv_encrypted
            decrypted.append(decrypted_block.to_bytes(self.u * 2, "little"))
            iv_encrypted = block

        # Обрезаем дополняющие нули до исходной длины
        return b"".join(decrypted)[:length].decode("utf-8")


# Пример использования
if __name__ == "__main__":
    w = 32  # Размер блока в битах
    r = 12  # Количество раундов
    key = secrets.token_bytes(16)  # Случайный ключ длиной 16 байт

    rc5 = RC5(w, r, key)

    decrypted_file = "output_file.txt"

    iv = secrets.randbits(w * 2)  # Генерация случайного IV
    plaintext = input("Введите сообщение для шифрования: ")

    ciphertext = rc5.encrypt_message(iv, plaintext)
    print("Зашифрованное сообщение:", ciphertext.hex())

    decrypted_text = rc5.decrypt_message(iv, ciphertext)
    print("Расшифрованное сообщение:", decrypted_text)

