class Rotor:
    def __init__(self, wiring, notch, ring_setting=1):
        self.wiring = wiring
        self.notch = [ord(n) - 65 for n in notch]  # Множественные выемки
        self.ring_setting = ring_setting - 1  # Смещение кольца
        self.position = 0  # Текущая позиция ротора

    def set_position(self, pos):
        self.position = ord(pos.upper()) - 65

    def encode_forward(self, c):
        offset = (ord(c) - 65 + self.position - self.ring_setting) % 26
        encoded = (ord(self.wiring[offset]) - 65 - self.position + self.ring_setting) % 26
        return chr(encoded + 65)

    def encode_backward(self, c):
        offset = (ord(c) - 65 + self.position - self.ring_setting) % 26
        index = (self.wiring.index(chr(offset + 65)) - self.position + self.ring_setting) % 26
        return chr(index + 65)

    def rotate(self):
        self.position = (self.position + 1) % 26
        return self.position in self.notch


class Reflector:
    def __init__(self, wiring):
        self.wiring = wiring

    def reflect(self, c):
        return self.wiring[ord(c) - 65]


class Plugboard:
    def __init__(self, connections):
        self.connections = {a: b for a, b in connections}
        self.connections.update({b: a for a, b in connections})

    def swap(self, c):
        return self.connections.get(c, c)


class EnigmaMachine:
    def __init__(self, rotors, reflector, plugboard_settings):
        self.rotors = rotors
        self.reflector = reflector
        self.plugboard = plugboard_settings

    def encrypt(self, message):
        encrypted_message_list = []
        for char in message:
            if char.isalpha():
                char = char.upper()
                char = self.plugboard.swap(char)
                for rotor in self.rotors:
                    char = rotor.encode_forward(char)
                char = self.reflector.reflect(char)
                for rotor in reversed(self.rotors):
                    char = rotor.encode_backward(char)
                char = self.plugboard.swap(char)
                encrypted_message_list.append(char)
                self.advance_rotors()
            else:
                encrypted_message_list.append(char)
        return ''.join(encrypted_message)

    def advance_rotors(self):
        # Реализация "двойного шага"
        rotate_next = self.rotors[0].rotate()
        if rotate_next:
            rotate_next = self.rotors[1].rotate()
            if rotate_next:
                self.rotors[2].rotate()


# Настройка машины
rotor1 = Rotor("EKMFLGDQVZNTOWYHXUSPAIBRCJ", "Q", ring_setting=1)  # Ротор I
rotor2 = Rotor("AJDKSIRUXBLHWTMCQGZNPYFVOE", "E", ring_setting=1)  # Ротор II
rotor3 = Rotor("BDFHJLCPRTXVZNYEIWGAKMUSQO", "V", ring_setting=1)  # Ротор III
reflectorB = Reflector("YRUHQSLDPXNGOKMIEBFZCWVJAT")  # UKW-B
plugboard = Plugboard([('A', 'M'), ('F', 'I'), ('N', 'V'), ('P', 'S'), ('T', 'U'), ('W', 'Z')])

# Создание машины
enigma = EnigmaMachine([rotor3, rotor2, rotor1], reflectorB, plugboard)

# Шифрование
plaintext = "HELLO"
encrypted_message = enigma.encrypt(plaintext)
print("Зашифрованное сообщение:", encrypted_message)
