import tkinter as tk
from tkinter import messagebox, scrolledtext
from tkinter import ttk

############################################
#   Определение русских и английских алфавитов
############################################

russian_alphabet_upper = 'АБВГДЕЁЖЗИЙКЛМНОПРСТУФХЦЧШЩЪЫЬЭЮЯ'
russian_alphabet_lower = 'абвгдеёжзийклмнопрстуфхцчшщъыьэюя'
english_alphabet_upper = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
english_alphabet_lower = 'abcdefghijklmnopqrstuvwxyz'

russian_alphabet_size = len(russian_alphabet_upper)  # 33
english_alphabet_size = len(english_alphabet_upper)  # 26

def create_alphabet_mappings():
    """Создаёт отображения для русского и английского алфавитов."""
    # Русские
    mapping_upper_ru = {char: idx for idx, char in enumerate(russian_alphabet_upper)}
    mapping_lower_ru = {char: idx for idx, char in enumerate(russian_alphabet_lower)}
    reverse_mapping_upper_ru = {idx: char for idx, char in enumerate(russian_alphabet_upper)}
    reverse_mapping_lower_ru = {idx: char for idx, char in enumerate(russian_alphabet_lower)}
    
    # Английские
    mapping_upper_en = {char: idx for idx, char in enumerate(english_alphabet_upper)}
    mapping_lower_en = {char: idx for idx, char in enumerate(english_alphabet_lower)}
    reverse_mapping_upper_en = {idx: char for idx, char in enumerate(english_alphabet_upper)}
    reverse_mapping_lower_en = {idx: char for idx, char in enumerate(english_alphabet_lower)}

    return {
        'Russian': {
            'mapping_upper': mapping_upper_ru,
            'mapping_lower': mapping_lower_ru,
            'reverse_mapping_upper': reverse_mapping_upper_ru,
            'reverse_mapping_lower': reverse_mapping_lower_ru,
            'alphabet_size': russian_alphabet_size,
            'all_letters': 'АБВГДЕЁЖЗИЙКЛМНОПРСТУФХЦЧШЩЪЫЬЭЮЯ',
            'matrix_size_playfair': 6,
            'filler_playfair': 'Ъ'
        },
        'English': {
            'mapping_upper': mapping_upper_en,
            'mapping_lower': mapping_lower_en,
            'reverse_mapping_upper': reverse_mapping_upper_en,
            'reverse_mapping_lower': reverse_mapping_lower_en,
            'alphabet_size': english_alphabet_size,
            'all_letters': 'ABCDEFGHIKLMNOPQRSTUVWXYZ',  # J обычно пропускается
            'matrix_size_playfair': 5,
            'filler_playfair': 'X'
        }
    }

alphabet_mappings = create_alphabet_mappings()

################################################
#   Тексты на русском и английском (интерфейс)
################################################

texts = {
    'Russian': {
        'start_title': "CIPHER",
        'start_button': "Начать",
        'main_menu_title': "Меню приложения",
        'select_language': "Выберите язык / Choose language:",
        'lang_russian': "Русский/Russian",
        'lang_english': "Английский/English",
        'select_cipher': "Выберите шифр:",
        'cipher_vigenere': "Шифр Виженера",
        'cipher_playfair': "Шифр Плейфера",
        'cipher_affine': "Аффинный шифр",
        'history': "Историческая справка",
        'theory': "Теория",
        'names': "Чумаченко, Макарцева и Шишкова",  # Подпись в стартовом окне
        'plaintext': "Открытый текст/Шифртекcт:",
        'key': "Ключ:",
        'coeff_a': "Коэффициент a:",
        'coeff_b': "Коэффициент b:",
        'choose_operation': "Выберите операцию:",
        'encrypt': "Зашифровать",
        'decrypt': "Расшифровать",
        'execute': "Выполнить",
        'copy': "Копировать",
        'paste': "Вставить",
        'result_encrypt': "Зашифрованный текст:",
        'result_decrypt': "Расшифрованный текст:",
        'warning_input': "Введите текст и ключ.",
        'error_invalid_key': "Недопустимый символ в ключе: ",
        'error_a_not_coprime': "Коэффициент 'a' должен быть взаимно прост с ",
        'error_no_inverse': "Не удалось найти обратный коэффициент для 'a'=",
        'error_non_integer': "Коэффициенты 'a' и 'b' должны быть целыми числами.",
        'error_invalid_chars': "Недопустимые символы в тексте: ",

        # Историческая справка (Russian)
        'history_vigenere': """
Шифр Виженера

- Происхождение: Изобретён Блезом Виженером в 1586 году.
- Описание: Полиалфавитный шифр, использующий серию шифров Цезаря с разными сдвигами.
- Применение: Долгое время считался неразгаданным.
""",
        'history_playfair': """
Шифр Плейфера

- Происхождение: Разработан Чарльзом Уитстоном в 1854 году.
- Описание: Биграммный шифр, который шифрует пары букв.
- Применение: Применялся британскими войсками в Первую мировую.
""",
        'history_affine': """
Аффинный шифр

- Происхождение: Расширение шифра Цезаря.
- Описание: Использует линейное преобразование (a*x + b) mod m.
- Применение: Служит примером для понимания более сложных алгоритмов.
""",
        # Теория (Russian)
        'theory_vigenere': """
Теория шифра Виженера

- Использование:
  1. Выберите ключ (строка).
  2. Каждая буква текста сдвигается на позицию ключа (по модулю).
  3. Дешифрование — обратный процесс (вычитание).
""",
        'theory_playfair': """
Теория шифра Плейфера

- Использование:
  1. Формируется матрица (6x6 для русского).
  2. Текст бьётся на биграммы.
  3. Если в одной строке — сдвиг вправо, в одном столбце — сдвиг вниз, иначе прямоугольник.
""",
        'theory_affine': """
Теория аффинного шифра

- Использование:
  1. Коэффициенты a и b.
  2. `E(x) = (a*x + b) mod m`, `D(x) = a_inv*(x - b) mod m`.
  3. a_inv — обратный элемент к a по модулю.
""",
        'select_alphabet': "Выберите алфавит шифрования:",
        'alphabet_russian': "Русский",
        'alphabet_english': "Английский"
    },

    'English': {
        'start_title': "Cipher Application",
        'start_button': "Start",
        'main_menu_title': "Application Menu",
        'select_language': "Choose Language:",
        'lang_russian': "Russian",
        'lang_english': "English",
        'select_cipher': "Choose Cipher:",
        'cipher_vigenere': "Vigenère Cipher",
        'cipher_playfair': "Playfair Cipher",
        'cipher_affine': "Affine Cipher",
        'history': "Historical Background",
        'theory': "Theory",
        'names': " ",  
        'plaintext': "Plaintext/Ciphertext:",
        'key': "Key:",
        'coeff_a': "Coefficient a:",
        'coeff_b': "Coefficient b:",
        'choose_operation': "Choose Operation:",
        'encrypt': "Encrypt",
        'decrypt': "Decrypt",
        'execute': "Execute",
        'copy': "Copy",
        'paste': "Paste",
        'result_encrypt': "Encrypted Text:",
        'result_decrypt': "Decrypted Text:",
        'warning_input': "Please enter text and key.",
        'error_invalid_key': "Invalid character in key: ",
        'error_a_not_coprime': "Coefficient 'a' must be coprime with ",
        'error_no_inverse': "Failed to find inverse coefficient for 'a'=",
        'error_non_integer': "Coefficients 'a' and 'b' must be integers.",
        'error_invalid_chars': "Invalid characters in text: ",

        # Историческая справка (English)
        'history_vigenere': """
Vigenère Cipher

- Origin: Credited to Blaise de Vigenère in 1586.
- Description: A polyalphabetic cipher using different shifts.
- Application: Long considered unbreakable in older cryptography.
""",
        'history_playfair': """
Playfair Cipher

- Origin: Invented by Charles Wheatstone in 1854, named after Lyon Playfair.
- Description: A digram substitution cipher for pairs of letters.
- Application: Used by British forces during WWI.
""",
        'history_affine': """
Affine Cipher

- Origin: An extension of the Caesar cipher.
- Description: Uses a linear function (a*x + b) mod m.
- Application: A basic demonstration of modular arithmetic in cryptography.
""",
        # Теория (English)
        'theory_vigenere': """
Theory of the Vigenère Cipher

- Usage:
  1. Choose a keyword.
  2. Each letter of the text is shifted by the key letter (mod the alphabet).
  3. Decryption is the inverse process (subtracting the key letter).
""",
        'theory_playfair': """
Theory of the Playfair Cipher

- Usage:
  1. Create a 5x5 matrix (English) or 6x6 (Russian).
  2. Split text into digrams; insert filler if needed.
  3. Same row => shift right, same column => shift down, else rectangle swap.
""",
        'theory_affine': """
Theory of the Affine Cipher

- Usage:
  1. Choose coefficients a and b (gcd(a, m)=1).
  2. Encryption: E(x) = (a*x + b) mod m.
  3. Decryption: D(x) = a_inv*(x - b) mod m (where a_inv is inverse of a).
""",
        'select_alphabet': "Choose cipher alphabet:",
        'alphabet_russian': "Russian",
        'alphabet_english': "English"
    }
}


#   Текущий язык интерфейса
current_language = 'Russian'

def update_texts(widgets, texts_dict):
    """Обновляет тексты у всех виджетов в widgets на основе словаря texts_dict."""
    for key, widget in widgets.items():
        if key in texts_dict:
            if isinstance(widget, (tk.Label, tk.Button, ttk.LabelFrame, tk.Radiobutton)):
                widget.config(text=texts_dict[key])

#  Главное меню приложения
def open_main_menu():
    # Скрываем стартовое окно
    start_window.withdraw()

    global root
    root = tk.Toplevel()
    root.title(texts[current_language]['main_menu_title'])
    root.geometry("600x600")

    widgets_menu = {}

    # Выбор языка (радиокнопки)
    widgets_menu['select_language'] = tk.Label(root, text=texts[current_language]['select_language'], font=("Arial", 14))
    widgets_menu['select_language'].pack(pady=10)
    
    language_var = tk.StringVar(value=current_language)
    widgets_menu['lang_russian'] = tk.Radiobutton(root, text=texts[current_language]['lang_russian'], 
                                                  variable=language_var, value='Russian',
                                                  command=lambda: switch_language(language_var.get()))
    widgets_menu['lang_russian'].pack()
    widgets_menu['lang_english'] = tk.Radiobutton(root, text=texts[current_language]['lang_english'], 
                                                  variable=language_var, value='English',
                                                  command=lambda: switch_language(language_var.get()))
    widgets_menu['lang_english'].pack()

    # Выбор шифра
    widgets_menu['select_cipher'] = tk.Label(root, text=texts[current_language]['select_cipher'], font=("Arial", 14))
    widgets_menu['select_cipher'].pack(pady=10)

    def get_selected_language():
        return current_language

    widgets_menu['cipher_vigenere'] = tk.Button(root, text=texts[current_language]['cipher_vigenere'], 
                                                command=lambda: vigenere_cipher(get_selected_language()), width=25)
    widgets_menu['cipher_vigenere'].pack(pady=5)

    widgets_menu['cipher_playfair'] = tk.Button(root, text=texts[current_language]['cipher_playfair'], 
                                                command=lambda: playfair_cipher(get_selected_language()), width=25)
    widgets_menu['cipher_playfair'].pack(pady=5)

    widgets_menu['cipher_affine'] = tk.Button(root, text=texts[current_language]['cipher_affine'],
                                              command=lambda: affine_cipher(get_selected_language()), width=25)
    widgets_menu['cipher_affine'].pack(pady=5)

    # Историческая справка и теория
    widgets_menu['history'] = tk.Button(root, text=texts[current_language]['history'], 
                                        command=lambda: show_history(get_selected_language()), width=25)
    widgets_menu['history'].pack(pady=10)

    widgets_menu['theory'] = tk.Button(root, text=texts[current_language]['theory'],
                                       command=lambda: show_theory(get_selected_language()), width=25)
    widgets_menu['theory'].pack(pady=5)


    def switch_language(new_language):
        """Смена языка интерфейса."""
        global current_language
        current_language = new_language
        root.title(texts[current_language]['main_menu_title'])
        update_texts(widgets_menu, texts[current_language])
        language_var.set(current_language)

    root.protocol("WM_DELETE_WINDOW", start_window.destroy)


#       Шифр Виженера
def vigenere_cipher(ui_language):
    def process_text():
        plaintext = entry_plaintext.get()
        key = entry_key.get()
        if not plaintext or not key:
            messagebox.showwarning(texts[ui_language]['warning_input'])
            return

        cipher_lang = cipher_lang_var.get()
        mappings = alphabet_mappings[cipher_lang]
        mapping_upper = mappings['mapping_upper']
        mapping_lower = mappings['mapping_lower']
        reverse_mapping_upper = mappings['reverse_mapping_upper']
        reverse_mapping_lower = mappings['reverse_mapping_lower']
        alphabet_size = mappings['alphabet_size']

        key_indices = []
        for k in key:
            if k.isupper() and k in mapping_upper:
                key_indices.append(mapping_upper[k])
            elif k.islower() and k in mapping_lower:
                key_indices.append(mapping_lower[k])
            else:
                messagebox.showerror(texts[ui_language]['error_invalid_key'] + k)
                return

        result_text = ''
        for i, char in enumerate(plaintext):
            if char.isupper() and char in mapping_upper:
                pi = mapping_upper[char]
                ki = key_indices[i % len(key_indices)]
                if operation.get() == 'encrypt':
                    ci = (pi + ki) % alphabet_size
                    result_text += reverse_mapping_upper[ci]
                else:
                    ci = (pi - ki) % alphabet_size
                    result_text += reverse_mapping_upper[ci]
            elif char.islower() and char in mapping_lower:
                pi = mapping_lower[char]
                ki = key_indices[i % len(key_indices)]
                if operation.get() == 'encrypt':
                    ci = (pi + ki) % alphabet_size
                    result_text += reverse_mapping_lower[ci]
                else:
                    ci = (pi - ki) % alphabet_size
                    result_text += reverse_mapping_lower[ci]
            else:
                result_text += char

        if operation.get() == 'encrypt':
            messagebox.showinfo(texts[ui_language]['result_encrypt'], result_text)
        else:
            messagebox.showinfo(texts[ui_language]['result_decrypt'], result_text)

    window = tk.Toplevel(root)
    window.title(f"{texts[ui_language]['cipher_vigenere']} ({ui_language})")

    tk.Label(window, text=texts[ui_language]['plaintext']).grid(row=0, column=0, padx=10, pady=10, sticky='e')
    entry_plaintext = tk.Entry(window, width=50)
    entry_plaintext.grid(row=0, column=1, padx=10, pady=10)
    
    tk.Label(window, text=texts[ui_language]['key']).grid(row=1, column=0, padx=10, pady=10, sticky='e')
    entry_key = tk.Entry(window, width=50)
    entry_key.grid(row=1, column=1, padx=10, pady=10)

    # Копировать/Вставить
    copy_button_plain = tk.Button(window, text=texts[ui_language]['copy'], command=lambda: copy_text(entry_plaintext))
    copy_button_plain.grid(row=0, column=2, padx=5, pady=10)
    paste_button_plain = tk.Button(window, text=texts[ui_language]['paste'], command=lambda: paste_text(entry_plaintext))
    paste_button_plain.grid(row=0, column=3, padx=5, pady=10)
    
    copy_button_key = tk.Button(window, text=texts[ui_language]['copy'], command=lambda: copy_text(entry_key))
    copy_button_key.grid(row=1, column=2, padx=5, pady=10)
    paste_button_key = tk.Button(window, text=texts[ui_language]['paste'], command=lambda: paste_text(entry_key))
    paste_button_key.grid(row=1, column=3, padx=5, pady=10)

    tk.Label(window, text=texts[ui_language]['choose_operation']).grid(row=2, column=0, padx=10, pady=10, sticky='e')
    operation = tk.StringVar(value='encrypt')
    tk.Radiobutton(window, text=texts[ui_language]['encrypt'], variable=operation, value='encrypt').grid(row=2, column=1, padx=10, pady=5, sticky='w')
    tk.Radiobutton(window, text=texts[ui_language]['decrypt'], variable=operation, value='decrypt').grid(row=2, column=1, padx=10, pady=5)

    # Алфавит шифрования
    tk.Label(window, text=texts[ui_language]['select_alphabet']).grid(row=3, column=0, padx=10, pady=10, sticky='e')
    cipher_lang_var = tk.StringVar(value='Russian')
    tk.Radiobutton(window, text=texts[ui_language]['alphabet_russian'], variable=cipher_lang_var, value='Russian').grid(row=3, column=1, padx=10, pady=5, sticky='w')
    tk.Radiobutton(window, text=texts[ui_language]['alphabet_english'], variable=cipher_lang_var, value='English').grid(row=3, column=1, padx=10, pady=5)

    tk.Button(window, text=texts[ui_language]['execute'], command=process_text).grid(row=4, column=1, padx=10, pady=20)

    def copy_text(entry):
        window.clipboard_clear()
        window.clipboard_append(entry.get())
    
    def paste_text(entry):
        try:
            text_paste = window.clipboard_get()
            entry.insert(tk.END, text_paste)
        except tk.TclError:
            pass

#  Шифр Плейфера
def playfair_cipher(ui_language):
    def process_text():
        plaintext = entry_plaintext.get().replace(' ', '').upper()
        key = entry_key.get().replace(' ', '').upper()
        if not plaintext or not key:
            messagebox.showwarning(texts[ui_language]['warning_input'])
            return

        cipher_lang = cipher_lang_var.get()
        mappings = alphabet_mappings[cipher_lang]
        all_letters = mappings['all_letters']
        matrix_size = mappings['matrix_size_playfair']
        filler = mappings['filler_playfair']

        matrix = []
        used = set()
        for char in key + all_letters:
            if char not in used and char in all_letters:
                used.add(char)
                matrix.append(char)
            if len(matrix) == matrix_size * matrix_size:
                break

        def find_position(c):
            idx = matrix.index(c)
            return idx // matrix_size, idx % matrix_size

        i = 0
        prepared_text = ''
        while i < len(plaintext):
            a = plaintext[i]
            if i + 1 < len(plaintext):
                b = plaintext[i + 1]
            else:
                b = filler
            if a == b:
                prepared_text += a + filler
                i += 1
            else:
                prepared_text += a + b
                i += 2
        if len(prepared_text) % 2 != 0:
            prepared_text += filler

        result_text = ''
        for i in range(0, len(prepared_text), 2):
            a, b = prepared_text[i], prepared_text[i + 1]
            if a not in matrix or b not in matrix:
                messagebox.showerror(texts[ui_language]['error_invalid_chars'] + f"{a} или {b}")
                return
            row1, col1 = find_position(a)
            row2, col2 = find_position(b)
            if row1 == row2:
                if operation.get() == 'encrypt':
                    result_text += matrix[row1 * matrix_size + (col1 + 1) % matrix_size]
                    result_text += matrix[row2 * matrix_size + (col2 + 1) % matrix_size]
                else:
                    result_text += matrix[row1 * matrix_size + (col1 - 1) % matrix_size]
                    result_text += matrix[row2 * matrix_size + (col2 - 1) % matrix_size]
            elif col1 == col2:
                if operation.get() == 'encrypt':
                    result_text += matrix[((row1 + 1) % matrix_size) * matrix_size + col1]
                    result_text += matrix[((row2 + 1) % matrix_size) * matrix_size + col2]
                else:
                    result_text += matrix[((row1 - 1) % matrix_size) * matrix_size + col1]
                    result_text += matrix[((row2 - 1) % matrix_size) * matrix_size + col2]
            else:
                result_text += matrix[row1 * matrix_size + col2]
                result_text += matrix[row2 * matrix_size + col1]

        if operation.get() == 'encrypt':
            messagebox.showinfo(texts[ui_language]['result_encrypt'], result_text)
        else:
            messagebox.showinfo(texts[ui_language]['result_decrypt'], result_text)
    
    window = tk.Toplevel(root)
    window.title(f"{texts[ui_language]['cipher_playfair']} ({ui_language})")

    tk.Label(window, text=texts[ui_language]['plaintext']).grid(row=0, column=0, padx=10, pady=10, sticky='e')
    entry_plaintext = tk.Entry(window, width=50)
    entry_plaintext.grid(row=0, column=1, padx=10, pady=10)
    
    tk.Label(window, text=texts[ui_language]['key']).grid(row=1, column=0, padx=10, pady=10, sticky='e')
    entry_key = tk.Entry(window, width=50)
    entry_key.grid(row=1, column=1, padx=10, pady=10)

    copy_button_plain = tk.Button(window, text=texts[ui_language]['copy'], command=lambda: copy_text(entry_plaintext))
    copy_button_plain.grid(row=0, column=2, padx=5, pady=10)
    paste_button_plain = tk.Button(window, text=texts[ui_language]['paste'], command=lambda: paste_text(entry_plaintext))
    paste_button_plain.grid(row=0, column=3, padx=5, pady=10)
    
    copy_button_key = tk.Button(window, text=texts[ui_language]['copy'], command=lambda: copy_text(entry_key))
    copy_button_key.grid(row=1, column=2, padx=5, pady=10)
    paste_button_key = tk.Button(window, text=texts[ui_language]['paste'], command=lambda: paste_text(entry_key))
    paste_button_key.grid(row=1, column=3, padx=5, pady=10)
    
    tk.Label(window, text=texts[ui_language]['choose_operation']).grid(row=2, column=0, padx=10, pady=10, sticky='e')
    operation = tk.StringVar(value='encrypt')
    tk.Radiobutton(window, text=texts[ui_language]['encrypt'], variable=operation, value='encrypt').grid(row=2, column=1, padx=10, pady=5, sticky='w')
    tk.Radiobutton(window, text=texts[ui_language]['decrypt'], variable=operation, value='decrypt').grid(row=2, column=1, padx=10, pady=5)

    # Алфавит шифрования
    tk.Label(window, text=texts[ui_language]['select_alphabet']).grid(row=3, column=0, padx=10, pady=10, sticky='e')
    cipher_lang_var = tk.StringVar(value='Russian')
    tk.Radiobutton(window, text=texts[ui_language]['alphabet_russian'], variable=cipher_lang_var, value='Russian').grid(row=3, column=1, padx=10, pady=5, sticky='w')
    tk.Radiobutton(window, text=texts[ui_language]['alphabet_english'], variable=cipher_lang_var, value='English').grid(row=3, column=1, padx=10, pady=5)

    tk.Button(window, text=texts[ui_language]['execute'], command=process_text).grid(row=4, column=1, padx=10, pady=20)

    def copy_text(entry):
        window.clipboard_clear()
        window.clipboard_append(entry.get())

    def paste_text(entry):
        try:
            text_paste = window.clipboard_get()
            entry.insert(tk.END, text_paste)
        except tk.TclError:
            pass


#  Аффинный шифр
def affine_cipher(ui_language):
    from tkinter import messagebox
    
    def gcd(x, y):
        while y:
            x, y = y, x % y
        return x

    def modinv(a, m):
        g, x, _ = extended_gcd(a, m)
        if g != 1:
            return None
        else:
            return x % m

    def extended_gcd(a, b):
        if a == 0:
            return (b, 0, 1)
        g, y, x = extended_gcd(b % a, a)
        return (g, x - (b // a) * y, y)

    def process_text():
        plaintext = entry_plaintext.get()
        a = entry_a.get()
        b = entry_b.get()
        if not plaintext or not a or not b:
            messagebox.showwarning(texts[ui_language]['warning_input'])
            return
        cipher_lang = cipher_lang_var.get()
        try:
            a_int = int(a)
            b_int = int(b)
            mappings = alphabet_mappings[cipher_lang]
            alphabet_size = mappings['alphabet_size']
            if gcd(a_int, alphabet_size) != 1:
                messagebox.showerror(texts[ui_language]['error_a_not_coprime'] + str(alphabet_size) + ".")
                return
            if operation.get() == 'decrypt':
                a_inv = modinv(a_int, alphabet_size)
                if a_inv is None:
                    messagebox.showerror(texts[ui_language]['error_no_inverse'] + f"{a_int}.")
                    return
        except ValueError:
            messagebox.showerror(texts[ui_language]['error_non_integer'])
            return

        if operation.get() == 'encrypt':
            def transform(pi):
                return (a_int * pi + b_int) % alphabet_size
        else:
            a_inv = modinv(a_int, alphabet_size)
            def transform(pi):
                return (a_inv * (pi - b_int)) % alphabet_size
        
        result_text = ''
        mapping_upper = mappings['mapping_upper']
        mapping_lower = mappings['mapping_lower']
        reverse_mapping_upper = mappings['reverse_mapping_upper']
        reverse_mapping_lower = mappings['reverse_mapping_lower']
        
        for char in plaintext:
            if char.isupper() and char in mapping_upper:
                pi = mapping_upper[char]
                ci = transform(pi)
                result_text += reverse_mapping_upper[ci]
            elif char.islower() and char in mapping_lower:
                pi = mapping_lower[char]
                ci = transform(pi)
                result_text += reverse_mapping_lower[ci]
            else:
                result_text += char

        if operation.get() == 'encrypt':
            messagebox.showinfo(texts[ui_language]['result_encrypt'], result_text)
        else:
            messagebox.showinfo(texts[ui_language]['result_decrypt'], result_text)
    
    window = tk.Toplevel(root)
    window.title(f"{texts[ui_language]['cipher_affine']} ({ui_language})")

    tk.Label(window, text=texts[ui_language]['plaintext']).grid(row=0, column=0, padx=10, pady=10, sticky='e')
    entry_plaintext = tk.Entry(window, width=50)
    entry_plaintext.grid(row=0, column=1, padx=10, pady=10)
    
    tk.Label(window, text=texts[ui_language]['coeff_a']).grid(row=1, column=0, padx=10, pady=10, sticky='e')
    entry_a = tk.Entry(window, width=50)
    entry_a.grid(row=1, column=1, padx=10, pady=10)
    
    tk.Label(window, text=texts[ui_language]['coeff_b']).grid(row=2, column=0, padx=10, pady=10, sticky='e')
    entry_b = tk.Entry(window, width=50)
    entry_b.grid(row=2, column=1, padx=10, pady=10)

    copy_button_plain = tk.Button(window, text=texts[ui_language]['copy'], command=lambda: copy_text(entry_plaintext))
    copy_button_plain.grid(row=0, column=2, padx=5, pady=10)
    paste_button_plain = tk.Button(window, text=texts[ui_language]['paste'], command=lambda: paste_text(entry_plaintext))
    paste_button_plain.grid(row=0, column=3, padx=5, pady=10)
    
    copy_button_a = tk.Button(window, text=texts[ui_language]['copy'], command=lambda: copy_text(entry_a))
    copy_button_a.grid(row=1, column=2, padx=5, pady=10)
    paste_button_a = tk.Button(window, text=texts[ui_language]['paste'], command=lambda: paste_text(entry_a))
    paste_button_a.grid(row=1, column=3, padx=5, pady=10)
    
    copy_button_b = tk.Button(window, text=texts[ui_language]['copy'], command=lambda: copy_text(entry_b))
    copy_button_b.grid(row=2, column=2, padx=5, pady=10)
    paste_button_b = tk.Button(window, text=texts[ui_language]['paste'], command=lambda: paste_text(entry_b))
    paste_button_b.grid(row=2, column=3, padx=5, pady=10)

    tk.Label(window, text=texts[ui_language]['choose_operation']).grid(row=3, column=0, padx=10, pady=10, sticky='e')
    operation = tk.StringVar(value='encrypt')
    tk.Radiobutton(window, text=texts[ui_language]['encrypt'], variable=operation, value='encrypt').grid(row=3, column=1, padx=10, pady=5, sticky='w')
    tk.Radiobutton(window, text=texts[ui_language]['decrypt'], variable=operation, value='decrypt').grid(row=3, column=1, padx=10, pady=5)

    # Алфавит шифрования
    tk.Label(window, text=texts[ui_language]['select_alphabet']).grid(row=4, column=0, padx=10, pady=10, sticky='e')
    cipher_lang_var = tk.StringVar(value='Russian')
    tk.Radiobutton(window, text=texts[ui_language]['alphabet_russian'], variable=cipher_lang_var, value='Russian').grid(row=4, column=1, padx=10, pady=5, sticky='w')
    tk.Radiobutton(window, text=texts[ui_language]['alphabet_english'], variable=cipher_lang_var, value='English').grid(row=4, column=1, padx=10, pady=5)

    tk.Button(window, text=texts[ui_language]['execute'], command=process_text).grid(row=5, column=1, padx=10, pady=20)

    def copy_text(entry):
        window.clipboard_clear()
        window.clipboard_append(entry.get())

    def paste_text(entry):
        try:
            text_paste = window.clipboard_get()
            entry.insert(tk.END, text_paste)
        except tk.TclError:
            pass

#################################
#  Историческая справка
#################################
def show_history(ui_language):
    def show_cipher_history(cipher_name):
        history_dict = {
            "Vigenère": texts[ui_language]['history_vigenere'],
            "Playfair": texts[ui_language]['history_playfair'],
            "Affine": texts[ui_language]['history_affine']
        }
        info_text = history_dict.get(cipher_name, "Information not available.")
        text_area.configure(state='normal')
        text_area.delete(1.0, tk.END)
        text_area.insert(tk.END, info_text)
        text_area.configure(state='disabled')

    window = tk.Toplevel(root)
    window.title(texts[ui_language]['history'])

    tk.Label(window, text=texts[ui_language]['history'], font=("Arial", 14)).pack(pady=5)
    tk.Button(window, text=texts[ui_language]['cipher_vigenere'], command=lambda: show_cipher_history("Vigenère")).pack(pady=2)
    tk.Button(window, text=texts[ui_language]['cipher_playfair'], command=lambda: show_cipher_history("Playfair")).pack(pady=2)
    tk.Button(window, text=texts[ui_language]['cipher_affine'], command=lambda: show_cipher_history("Affine")).pack(pady=2)

    text_area = scrolledtext.ScrolledText(window, wrap=tk.WORD, width=80, height=20)
    text_area.pack(padx=10, pady=10)
    text_area.configure(state='disabled')


#  Теория
def show_theory(ui_language):
    def show_cipher_theory(cipher_name):
        theory_dict = {
            "Vigenère": texts[ui_language]['theory_vigenere'],
            "Playfair": texts[ui_language]['theory_playfair'],
            "Affine": texts[ui_language]['theory_affine']
        }
        theory_text = theory_dict.get(cipher_name, "Information not available.")
        text_area.configure(state='normal')
        text_area.delete(1.0, tk.END)
        text_area.insert(tk.END, theory_text)
        text_area.configure(state='disabled')

    window = tk.Toplevel(root)
    window.title(texts[ui_language]['theory'])

    tk.Label(window, text=texts[ui_language]['theory'], font=("Arial", 14)).pack(pady=5)
    tk.Button(window, text=texts[ui_language]['cipher_vigenere'], command=lambda: show_cipher_theory("Vigenère")).pack(pady=2)
    tk.Button(window, text=texts[ui_language]['cipher_playfair'], command=lambda: show_cipher_theory("Playfair")).pack(pady=2)
    tk.Button(window, text=texts[ui_language]['cipher_affine'], command=lambda: show_cipher_theory("Affine")).pack(pady=2)

    text_area = scrolledtext.ScrolledText(window, wrap=tk.WORD, width=80, height=20)
    text_area.pack(padx=10, pady=10)
    text_area.configure(state='disabled')

#  Стартовое окно
start_window = tk.Tk()
start_window.title(texts[current_language]['start_title'])
start_window.geometry("600x400")

# Виджеты стартового окна
label_title = tk.Label(start_window, text=texts[current_language]['start_title'], font=("Arial", 20))
label_title.pack(expand=True)

button_start = tk.Button(start_window, text=texts[current_language]['start_button'], command=open_main_menu, width=15, height=2, font=("Arial", 14))
button_start.pack()

label_names = tk.Label(start_window, text=texts[current_language]['names'], font=("Arial", 10))
label_names.pack(side="bottom", anchor="e", padx=10, pady=10)

start_window.mainloop()
