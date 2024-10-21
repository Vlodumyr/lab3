from flask import Flask, request, jsonify, render_template
from flask_cors import CORS
import base64
from urllib.parse import quote, unquote
import codecs
import string
import random
import re

app = Flask(__name__)
CORS(app)

MORSE_CODE_DICT = { 'A':'.-', 'B':'-...', 'C':'-.-.', 'D':'-..', 'E':'.', 'F':'..-.',
                    'G':'--.', 'H':'....', 'I':'..', 'J':'.---', 'K':'-.-', 'L':'.-..',
                    'M':'--', 'N':'-.', 'O':'---', 'P':'.--.', 'Q':'--.-', 'R':'.-.',
                    'S':'...', 'T':'-', 'U':'..-', 'V':'...-', 'W':'.--', 'X':'-..-',
                    'Y':'-.--', 'Z':'--..',
                    'А':'.-', 'Б':'-...', 'В':'.--', 'Г':'....', 'Ґ':'--.', 'Д':'-..',
                    'Е':'.', 'Є':'..-..', 'Ж':'...-', 'З':'--..', 'И':'-.--', 'І':'..',
                    'Ї':'.---.', 'Й':'.---', 'К':'-.-', 'Л':'.-..', 'М':'--', 'Н':'-.',
                    'О':'---', 'П':'.--.', 'Р':'.-.', 'С':'...', 'Т':'-', 'У':'..-',
                    'Ф':'..-.', 'Х':'----', 'Ц':'-.-.', 'Ч':'---.', 'Ш':'--.-', 'Щ':'--.--',
                    'Ю':'..--', 'Я':'.-.-', 'Ь':'-..-',
                    '1':'.----', '2':'..---', '3':'...--',
                    '4':'....-', '5':'.....', '6':'-....', '7':'--...', '8':'---..',
                    '9':'----.', '0':'-----', ', ':'--..--', '.':'.-.-.-', '?':'..--..',
                    '/':'-..-.', '-':'-....-', '(':'-.--.', ')':'-.--.-'}


def encode_morse(text):
    return ' '.join(MORSE_CODE_DICT.get(char.upper(), '') for char in text)


def decode_morse(morse_code):
    morse_dict = {v: k for k, v in MORSE_CODE_DICT.items()}
    return ''.join(morse_dict.get(code, '') for code in morse_code.split())


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/encode-decode', methods=['GET'])
def encode_decode():
    return render_template('encode-decode.html')


@app.route('/converter', methods=['GET'])
def converter():
    return render_template('converter.html')


@app.route('/regexp-generator', methods=['GET'])
def regexp_generator():
    return render_template('regexp-generator.html')


@app.route('/password-generator', methods=['GET'])
def password_generator():
    return render_template('password-generator.html')


@app.route('/encode', methods=['POST'])
def encode():
    data = request.json
    text = data.get('text', '')
    format = data.get('format', 'base64')

    if format == 'base64':
        encoded = base64.b64encode(text.encode('utf-8')).decode('utf-8')
    elif format == 'url':
        encoded = quote(text)
    elif format == 'rot13':
        encoded = codecs.encode(text, 'rot_13')
    elif format == 'hex':
        encoded = text.encode('utf-8').hex()
    elif format == 'morse':
        encoded = encode_morse(text)
    else:
        return jsonify({'error': 'Непідтримуваний формат'}), 400

    return jsonify({'encoded': encoded})


@app.route('/decode', methods=['POST'])
def decode():
    data = request.json
    text = data.get('text', '')
    format = data.get('format', 'base64')

    try:
        if format == 'base64':
            decoded = base64.b64decode(text).decode('utf-8')
        elif format == 'url':
            decoded = unquote(text)
        elif format == 'rot13':
            decoded = codecs.decode(text, 'rot_13')
        elif format == 'hex':
            decoded = bytes.fromhex(text).decode('utf-8')
        elif format == 'morse':
            decoded = decode_morse(text)
        else:
            return jsonify({'error': 'Непідтримуваний формат'}), 400
    except Exception as e:
        return jsonify({'error': str(e)}), 400

    return jsonify({'decoded': decoded})


# @app.route('/convert', methods=['POST'])
# def convert_number():
#     data = request.json
#     number = data.get('number', '')
#     from_base = data.get('from_base', 10)
#     to_base = data.get('to_base', 2)
#
#     try:
#         # Конвертуємо вхідне число в десяткову систему
#         decimal_num = int(str(number), from_base)
#
#         # Конвертуємо з десяткової в цільову систему
#         if to_base == 2:
#             result = bin(decimal_num)[2:]  # Видаляємо префікс '0b'
#         elif to_base == 8:
#             result = oct(decimal_num)[2:]  # Видаляємо префікс '0o'
#         elif to_base == 16:
#             result = hex(decimal_num)[2:]  # Видаляємо префікс '0x'
#         else:
#             return jsonify({'error': 'Непідтримувана система числення'}), 400
#
#         return jsonify({'result': result})
#     except ValueError:
#         return jsonify({'error': 'Невірний формат числа'}), 400


@app.route('/convert', methods=['POST'])
def convert_number():
    data = request.json
    number = data.get('number', '')

    try:
        from_base = int(data.get('from_base', 10))  # Перетворюємо на int
        to_base = int(data.get('to_base', 10))  # Перетворюємо на int
    except ValueError:
        return jsonify({'error': 'Невірний формат системи числення'}), 400

    try:
        # Конвертуємо вхідне число в десяткову систему
        decimal_num = int(str(number), from_base)

        # Конвертуємо з десяткової в цільову систему
        if to_base == 2:
            result = bin(decimal_num)[2:]  # Видаляємо префікс '0b'
        elif to_base == 8:
            result = oct(decimal_num)[2:]  # Видаляємо префікс '0o'
        elif to_base == 10:
            result = str(decimal_num)  # Пряме перетворення в десяткову
        elif to_base == 16:
            result = hex(decimal_num)[2:]  # Видаляємо префікс '0x'
        else:
            return jsonify({'error': 'Непідтримувана система числення'}), 400

        return jsonify({'result': result})
    except ValueError:
        return jsonify({'error': 'Невірний формат числа'}), 400


@app.route('/generate_regex', methods=['POST'])
def generate_regex():
    data = request.json
    pattern = data.get('pattern', '')
    test_string = data.get('test_string', '')

    try:
        regex = re.compile(pattern)
        matches = regex.findall(test_string)
        return jsonify({
            'is_valid': True,
            'matches': matches
        })
    except re.error as e:
        return jsonify({
            'is_valid': False,
            'error': str(e)
        })


# @app.route('/generate_password', methods=['POST'])
# def generate_password():
#     data = request.json
#     length = data.get('length', 12)
#     use_uppercase = data.get('use_uppercase', True)
#     use_lowercase = data.get('use_lowercase', True)
#     use_digits = data.get('use_digits', True)
#     use_special = data.get('use_special', True)
#
#     characters = ''
#     if use_uppercase:
#         characters += string.ascii_uppercase
#     if use_lowercase:
#         characters += string.ascii_lowercase
#     if use_digits:
#         characters += string.digits
#     if use_special:
#         characters += string.punctuation
#
#     if not characters:
#         return jsonify({'error': 'Виберіть хоча б один тип символів'}), 400
#
#     password = ''.join(random.choice(characters) for _ in range(length))
#     return jsonify({'password': password})


@app.route('/generate_password', methods=['POST'])
def generate_password():
    data = request.json
    length = data.get('length', 12)  # length - рядок тут, але ми його перетворимо нижче
    try:
        length = int(length)  # Перетворюємо в int
    except ValueError:
        return jsonify({'error': 'Довжина пароля повинна бути цілим числом'}), 400

    use_uppercase = data.get('use_uppercase', True)
    use_lowercase = data.get('use_lowercase', True)
    use_digits = data.get('use_digits', True)
    use_special = data.get('use_special', True)

    characters = ''
    if use_uppercase:
        characters += string.ascii_uppercase
    if use_lowercase:
        characters += string.ascii_lowercase
    if use_digits:
        characters += string.digits
    if use_special:
        characters += string.punctuation

    if not characters:
        return jsonify({'error': 'Виберіть хоча б один тип символів'}), 400

    password = ''.join(random.choice(characters) for _ in range(length))
    return jsonify({'password': password})


if __name__ == '__main__':
    app.run(debug=True)
