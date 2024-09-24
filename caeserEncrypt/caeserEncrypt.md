# Скрипт для шифрования с помощью шифра Цезаря

## Как работает скрипт?

1. Создаются массивы, в которых содержатся символы из русского и английского алфавита, а также массив с цифрами

```python
RUSSIAN_ALPHABET_LOWER = "абвгдеёжзийклмнопрстуфхцчшщъыьэюя"
RUSSIAN_ALPHABET_UPPER = "АБВГДЕЁЖЗИЙКЛМНОПРСТУФХЦЧШЩЪЫЬЭЮЯ"
ENGLISH_ALPHABET_LOWER = "abcdefghijklmnopqrstuvwxyz"
ENGLISH_ALPHABET_UPPER = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
numbers_all = "0123456789"
```
2. Генерация словаря, где каждому символу присваивается его значение из алфавита:
```python 
{char: RUSSIAN_ALPHABET_LOWER for char in RUSSIAN_ALPHABET_LOWER}
```
*пример:*
```bash
'а': 'абвгдеёжзийклмнопрстуфхцчшщъыьэюя'
'б': 'абвгдеёжзийклмнопрстуфхцчшщъыьэюя'
```
3. Применение оператора ** для объединения словарей в один:
```python
{
    **{char: RUSSIAN_ALPHABET_LOWER for char in RUSSIAN_ALPHABET_LOWER},
    **{char: RUSSIAN_ALPHABET_UPPER for char in RUSSIAN_ALPHABET_UPPER},
    **{char: ENGLISH_ALPHABET_LOWER for char in ENGLISH_ALPHABET_LOWER},
    **{char: ENGLISH_ALPHABET_UPPER for char in ENGLISH_ALPHABET_UPPER},
}
```
4. Нахождение алфавита и шифрование с помощью шифра Цезаря:
```python
if char in ALPHABETS:
    alphabet = ALPHABETS[char]  # Находим алфавит для текущего символа
    idx = alphabet.index(char)  # Находим индекс символа в алфавите
    return alphabet[(idx + shift) % len(alphabet)]  # Сдвигаем символ циклично
```
В этом коде происходит вычисление по количеству символов в самом алфавите и затем вычисление по введённому индексу.
*К примеру слово дурачьё:*
```commandline
idx - 4, shift_size - 5, len - 33
idx - 20, shift_size - 5, len - 33
idx - 17, shift_size - 5, len - 33
idx - 0, shift_size - 5, len - 33
idx - 24, shift_size - 5, len - 33
idx - 29, shift_size - 5, len - 33
idx - 6, shift_size - 5, len - 33
idx - 9, shift_size - -5, len - 33
idx - 25, shift_size - -5, len - 33
idx - 22, shift_size - -5, len - 33
idx - 5, shift_size - -5, len - 33
idx - 29, shift_size - -5, len - 33
idx - 1, shift_size - -5, len - 33
idx - 11, shift_size - -5, len - 33
```
Где **idx** - это индекс символа в алфавите, а **shift_size** - размер сдвига, при дешифровке он отрицательный, чтобы вернутсья к прошлому значению.

