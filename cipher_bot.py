#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import logging
from telegram import (
    Update,
    InlineKeyboardButton,
    InlineKeyboardMarkup
)
from telegram.ext import (
    Updater,
    CommandHandler,
    CallbackContext,
    CallbackQueryHandler,
    ConversationHandler,
    MessageHandler,
    Filters
)

#############################################
# ВСТАВЬТЕ СВОЙ ТОКЕН:
#############################################
BOT_TOKEN = "7677992853:AAHC99wqfSUDPCizx8HCE2Bl-shCWpP1_6E"

#############################################
# Логирование
#############################################
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

#############################################
# Алфавиты для русского и английского
#############################################
RUS_UPPER = "АБВГДЕЁЖЗИЙКЛМНОПРСТУФХЦЧШЩЪЫЬЭЮЯ"
RUS_LOWER = "абвгдеёжзийклмнопрстуфхцчшщъыьэюя"
ENG_UPPER = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
ENG_LOWER = "abcdefghijklmnopqrstuvwxyz"

#############################################
# Состояния ConversationHandler
#############################################
CHOOSING_CIPHER = 1
CHOOSING_MODE   = 2
ASK_KEY_OR_AB   = 3
ASK_TEXT        = 4

#############################################
# CallbackData для главного меню
#############################################
CB_VIGENERE = "CB_VIGENERE"
CB_PLAYFAIR = "CB_PLAYFAIR"
CB_AFFINE   = "CB_AFFINE"
CB_HISTORY  = "CB_HISTORY"
CB_THEORY   = "CB_THEORY"

#############################################
# CallbackData для режима (зашифровать/расшифровать)
#############################################
CB_ENCRYPT = "CB_ENCRYPT"
CB_DECRYPT = "CB_DECRYPT"

#############################################
# Утилиты: gcd, modinv
#############################################
def gcd(a, b):
    while b:
        a, b = b, a % b
    return a

def extended_gcd(a, b):
    if a == 0:
        return (b, 0, 1)
    g, y, x = extended_gcd(b % a, a)
    return (g, x - (b // a)*y, y)

def modinv(a, m):
    g, x, _ = extended_gcd(a, m)
    if g != 1:
        return None
    return x % m

#############################################
# Реальные шифры: Виженер, Плейфер, Аффинный
#############################################

def create_mappings_for_text(text):
    """
    Определяем, какие алфавиты использовать на основе &laquo;преимущественного языка&raquo; текста.
    Упрощённо: если видим кириллицу — рус. Если латиницу — англ.
    Можно улучшать под ваши нужды.
    """
    # Проверим, есть ли хотя бы одна буква из русского или английского
    # Если не находим ничего, по умолчанию считаем русский
    ru_count = sum(ch in RUS_UPPER+RUS_LOWER for ch in text)
    en_count = sum(ch in ENG_UPPER+ENG_LOWER for ch in text)
    if ru_count >= en_count:
        upper_alphabet = RUS_UPPER
        lower_alphabet = RUS_LOWER
    else:
        upper_alphabet = ENG_UPPER
        lower_alphabet = ENG_LOWER
    return upper_alphabet, lower_alphabet

def vigenere_cipher(text, key, mode="encrypt"):
    """
    Виженер: подбираем алфавит исходя из языка текста (упрощённо).
    """
    up_alph, low_alph = create_mappings_for_text(text)

    size = len(up_alph)
    # Соберём индексы ключа (с учётом языка ключа)
    # Упрощённо: берём для ключа тот же язык, что и текст (можно улучшить)
    up_alph_key, low_alph_key = create_mappings_for_text(key)

    key_inds = []
    for k in key:
        if k in up_alph_key:
            key_inds.append(up_alph_key.index(k))
        elif k in low_alph_key:
            key_inds.append(low_alph_key.index(k))

    if not key_inds:
        return "Ошибка: недопустимый ключ!"

    res = []
    idx = 0
    for ch in text:
        if ch in up_alph:
            pi = up_alph.index(ch)
            ki = key_inds[idx % len(key_inds)]
            idx += 1
            if mode == "encrypt":
                ci = (pi + ki) % size
            else:
                ci = (pi - ki) % size
            res.append(up_alph[ci])
        elif ch in low_alph:
            pi = low_alph.index(ch)
            ki = key_inds[idx % len(key_inds)]
            idx += 1
            if mode == "encrypt":
                ci = (pi + ki) % size
            else:
                ci = (pi - ki) % size
            res.append(low_alph[ci])
        else:
            # Прочие символы не трогаем
            res.append(ch)
    return "".join(res)

def playfair_cipher(text, key, mode="encrypt"):
    """
    Базовый Плейфер: 
    - если обнаружим преимущественно русские буквы, используем 6x6, filler=Ъ
    - если преимущественно английские, 5x5, filler=X (без 'J')
    """
    # Определим язык текста
    ru_count = sum(ch in RUS_UPPER+RUS_LOWER for ch in text)
    en_count = sum(ch in ENG_UPPER+ENG_LOWER for ch in text)
    if ru_count >= en_count:
        # Русская версия (6x6), filler=Ъ
        filler = 'Ъ'
        # Собираем алфавит 6x6
        alph = RUS_UPPER
        matrix_size = 6
    else:
        # Английская версия (5x5), без 'J'
        filler = 'X'
        # Упрощённо убираем J
        alph = ''.join(ch for ch in ENG_UPPER if ch != 'J')
        matrix_size = 5

    # Создаём матрицу
    used = set()
    matrix = []
    # Добавим key (вверхний регистр, без пробелов)
    key_up = key.upper().replace(' ', '')
    for c in key_up + alph:
        if c not in used and c in alph:
            used.add(c)
            matrix.append(c)
        if len(matrix) == matrix_size*matrix_size:
            break

    def find_pos(ch):
        idx = matrix.index(ch)
        return idx // matrix_size, idx % matrix_size

    # Подготовка текста
    text_up = text.upper().replace(' ', '')

    # Разбиваем на биграммы
    pairs = []
    i = 0
    while i < len(text_up):
        a = text_up[i]
        if i+1 < len(text_up):
            b = text_up[i+1]
        else:
            b = filler
        if a == b:
            pairs.append(a + filler)
            i += 1
        else:
            pairs.append(a + b)
            i += 2
    if len(pairs[-1]) == 1:
        pairs[-1] += filler

    res = []
    for pair in pairs:
        a, b = pair[0], pair[1]
        if a not in matrix or b not in matrix:
            # Символы вне матрицы оставим
            res.append(a)
            res.append(b)
            continue
        r1, c1 = find_pos(a)
        r2, c2 = find_pos(b)
        if r1 == r2:
            # Одна строка
            if mode == "encrypt":
                cA = matrix[r1*matrix_size + (c1+1) % matrix_size]
                cB = matrix[r2*matrix_size + (c2+1) % matrix_size]
            else:
                cA = matrix[r1*matrix_size + (c1-1) % matrix_size]
                cB = matrix[r2*matrix_size + (c2-1) % matrix_size]
        elif c1 == c2:
            # Один столбец
            if mode == "encrypt":
                cA = matrix[((r1+1) % matrix_size)*matrix_size + c1]
                cB = matrix[((r2+1) % matrix_size)*matrix_size + c2]
            else:
                cA = matrix[((r1-1) % matrix_size)*matrix_size + c1]
                cB = matrix[((r2-1) % matrix_size)*matrix_size + c2]
        else:
            # Прямоугольник
            cA = matrix[r1*matrix_size + c2]
            cB = matrix[r2*matrix_size + c1]
        res.append(cA)
        res.append(cB)
    return "".join(res)

def affine_cipher(text, a, b, mode="encrypt"):
    """
    Если текст преимущественно русский — размер алфавита 33, иначе 26.
    """
    try:
        a_int = int(a)
        b_int = int(b)
    except ValueError:
        return "Ошибка: a/b должны быть числами!"

    # Определим язык
    ru_count = sum(ch in RUS_UPPER+RUS_LOWER for ch in text)
    en_count = sum(ch in ENG_UPPER+ENG_LOWER for ch in text)
    if ru_count >= en_count:
        up_alph = RUS_UPPER
        low_alph = RUS_LOWER
    else:
        up_alph = ENG_UPPER
        low_alph = ENG_LOWER

    m = len(up_alph)

    # Проверка gcd
    if gcd(a_int, m) != 1:
        return f"Ошибка: a={a_int} не взаимно просто с {m}!"

    if mode == "decrypt":
        a_inv = modinv(a_int, m)
        if a_inv is None:
            return "Ошибка: не найден обратный элемент!"
    
    res = []
    for ch in text:
        if ch in up_alph:
            x = up_alph.index(ch)
            if mode == "encrypt":
                y = (a_int*x + b_int) % m
            else:
                y = (a_inv*(x - b_int)) % m
            res.append(up_alph[y])
        elif ch in low_alph:
            x = low_alph.index(ch)
            if mode == "encrypt":
                y = (a_int*x + b_int) % m
            else:
                y = (a_inv*(x - b_int)) % m
            res.append(low_alph[y])
        else:
            res.append(ch)
    return "".join(res)

#############################################
# Тексты справок
#############################################
def history_text():
    return (
        "История шифров:\n"
        "1) Виженер — 1586, считался 'неразбиваемым'.\n"
        "2) Плейфер — 1854, биграммный шифр.\n"
        "3) Аффинный — расширение шифра Цезаря.\n"
    )

def theory_text():
    return (
        "Теория шифров:\n"
        "• Виженер: полиалфавитная замена.\n"
        "• Плейфер: матрица букв, шифрование биграмм.\n"
        "• Аффинный: E(x)=(a*x+b) mod m, D(x)=a_inv*(x-b) mod m.\n"
    )

#############################################
# Главное меню: кнопки
#############################################
def start_command(update: Update, context: CallbackContext):
    keyboard = [
        [
            InlineKeyboardButton("Виженер", callback_data=CB_VIGENERE),
            InlineKeyboardButton("Плейфер", callback_data=CB_PLAYFAIR),
        ],
        [
            InlineKeyboardButton("Аффинный", callback_data=CB_AFFINE),
        ],
        [
            InlineKeyboardButton("История", callback_data=CB_HISTORY),
            InlineKeyboardButton("Теория", callback_data=CB_THEORY),
        ]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    update.message.reply_text(
        "Привет! Выберите шифр или справку:",
        reply_markup=reply_markup
    )
    return CHOOSING_CIPHER

def handle_main_menu(update: Update, context: CallbackContext):
    """Обработчик нажатия кнопок главного меню."""
    query = update.callback_query
    query.answer()

    choice = query.data

    if choice == CB_VIGENERE:
        context.user_data["cipher"] = "vigenere"
        return show_mode_menu(query)
    elif choice == CB_PLAYFAIR:
        context.user_data["cipher"] = "playfair"
        return show_mode_menu(query)
    elif choice == CB_AFFINE:
        context.user_data["cipher"] = "affine"
        return show_mode_menu(query)
    elif choice == CB_HISTORY:
        query.edit_message_text(history_text())
        query.message.reply_text("Наберите /start, чтобы вернуться в меню.")
        return ConversationHandler.END
    elif choice == CB_THEORY:
        query.edit_message_text(theory_text())
        query.message.reply_text("Наберите /start, чтобы вернуться в меню.")
        return ConversationHandler.END
    else:
        query.edit_message_text("Неизвестная команда.")
        return CHOOSING_CIPHER

#############################################
# Меню "Зашифровать" / "Расшифровать"
#############################################
def show_mode_menu(query):
    keyboard = [
        [
            InlineKeyboardButton("Зашифровать", callback_data=CB_ENCRYPT),
            InlineKeyboardButton("Расшифровать", callback_data=CB_DECRYPT),
        ]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    query.edit_message_text("Выберите режим:", reply_markup=reply_markup)
    return CHOOSING_MODE

def handle_mode_menu(update: Update, context: CallbackContext):
    query = update.callback_query
    query.answer()

    if query.data == CB_ENCRYPT:
        context.user_data["mode"] = "encrypt"
    else:
        context.user_data["mode"] = "decrypt"

    cipher = context.user_data.get("cipher")
    if cipher == "affine":
        query.edit_message_text("Введите коэффициенты a и b (пример: 5 7).")
    else:
        query.edit_message_text("Введите ключ (строка).")

    return ASK_KEY_OR_AB

#############################################
# Считываем ключ (или a,b) => затем просим текст
#############################################
def handle_key_or_ab(update: Update, context: CallbackContext):
    user_input = update.message.text.strip()
    cipher = context.user_data.get("cipher")
    if cipher == "affine":
        parts = user_input.split()
        if len(parts) != 2:
            update.message.reply_text("Ошибка. Нужно ввести два числа через пробел, например: 5 7")
            return ASK_KEY_OR_AB
        context.user_data["a"] = parts[0]
        context.user_data["b"] = parts[1]
    else:
        context.user_data["key"] = user_input

    update.message.reply_text("Хорошо. Теперь введите текст для обработки:")
    return ASK_TEXT

#############################################
# Считываем текст => шифруем => выводим результат
#############################################
def handle_text(update: Update, context: CallbackContext):
    text = update.message.text
    cipher = context.user_data.get("cipher")
    mode = context.user_data.get("mode")

    if cipher == "vigenere":
        key = context.user_data.get("key", "")
        result = vigenere_cipher(text, key, mode)
    elif cipher == "playfair":
        key = context.user_data.get("key", "")
        result = playfair_cipher(text, key, mode)
    else:
        a = context.user_data.get("a", "1")
        b = context.user_data.get("b", "0")
        result = affine_cipher(text, a, b, mode)

    update.message.reply_text(f"Результат:\n{result}\n\nНаберите /start для нового шифрования.")
    return ConversationHandler.END

#############################################
# /cancel — прерывание диалога
#############################################
def cancel_command(update: Update, context: CallbackContext):
    update.message.reply_text("Операция отменена. Наберите /start для нового выбора.")
    return ConversationHandler.END

#############################################
# Запуск бота
#############################################
def main():
    updater = Updater(BOT_TOKEN, use_context=True)
    dp = updater.dispatcher

    # Создаём ConversationHandler со стейтами
    conv_handler = ConversationHandler(
        entry_points=[CommandHandler("start", start_command)],
        states={
            CHOOSING_CIPHER: [
                CallbackQueryHandler(handle_main_menu),
            ],
            CHOOSING_MODE: [
                CallbackQueryHandler(handle_mode_menu),
            ],
            ASK_KEY_OR_AB: [
                MessageHandler(Filters.text & ~Filters.command, handle_key_or_ab),
            ],
            ASK_TEXT: [
                MessageHandler(Filters.text & ~Filters.command, handle_text),
            ],
        },
        fallbacks=[CommandHandler("cancel", cancel_command)]
    )

    dp.add_handler(conv_handler)

    updater.start_polling()
    updater.idle()

if __name__ == "__main__":
    main()