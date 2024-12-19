import random
from math import gcd
import secrets

bit_length = 8  # Set a smaller bit length for testing, such as 8 bits.

def mod_inverse(a: int, m: int) -> int:
    m0, x0, x1 = m, 0, 1
    while a > 1:
        if m != 0:
            q = a // m
            a, m = m, a % m
            x0, x1 = x1 - q * x0, x0
    if x1 < 0:
        x1 += m0
    return x1

def is_prime(n: int) -> bool:
    if n < 2:
        return False
    elif n == 2:
        return True
    else:
        for i in range(2, int(n**0.5) + 1):
            if n % i == 0:
                return False
    return True

def generate_keypair(keysize: int) -> tuple:
    n_min = 1 << (keysize - 1)
    n_max = (1 << keysize) - 1
    primes = [2]

    for i in range(3, n_max + 1, 2):
        for p in primes:
            if i % p == 0:
                break
        else:
            primes.append(i)

    while primes:
        p = random.choice(primes)
        primes.remove(p)
        q = None
        for q_candidate in primes:
            if n_min <= p * q_candidate <= n_max:
                q = q_candidate
                break
        if q:
            break

    n = p * q
    phi = (p - 1) * (q - 1)

    e = random.randrange(1, phi)
    while gcd(e, phi) != 1:
        e = random.randrange(1, phi)

    d = mod_inverse(e, phi)
    return ((e, n), (d, n))

def encrypt_message(message: str, public_key: tuple) -> list:
    e, n = public_key
    return [pow(ord(c), e, n) for c in message]

def decrypt_message(ciphertext: list, private_key: tuple) -> str:
    d, n = private_key
    return ''.join([chr(pow(c, d, n)) for c in ciphertext])

if __name__ == "__main__":
    print('RSA Encryption')
    keysize = bit_length  # Use a smaller keysize for testing (e.g., 8 bits).
    print(f'Bit length: {bit_length}')
    public_key, private_key = generate_keypair(keysize)

    print(f'Public key: {public_key}')
    print(f'Private key: {private_key}')
    print('=' * 10)

    message = input("Enter a message: ")
    print([ord(c) for c in message])

    encrypted_message = encrypt_message(message, public_key)
    print("Encrypted message:", ''.join([str(i) for i in encrypted_message]))

    decrypted_message = decrypt_message(encrypted_message, private_key)
    print("Decrypted message:", decrypted_message)
