from typing import List
from telebot.types import ReplyKeyboardMarkup, InlineKeyboardMarkup, InlineKeyboardButton, KeyboardButton
from config import ui_config

class Keyboard:
    """Базовый класс для клавиатур"""
    
    @staticmethod
    def create_reply_keyboard(buttons: List[str], row_width: int = 2, resize: bool = True, one_time: bool = True) -> ReplyKeyboardMarkup:
        """Создание обычной клавиатуры"""
        markup = ReplyKeyboardMarkup(resize_keyboard=resize, one_time_keyboard=one_time, row_width=row_width)
        markup.add(*buttons)
        return markup
    
    @staticmethod
    def create_inline_keyboard(buttons: List[dict], row_width: int = 2) -> InlineKeyboardMarkup:
        """Создание инлайн-клавиатуры"""
        markup = InlineKeyboardMarkup(row_width=row_width)
        for button in buttons:
            markup.add(InlineKeyboardButton(
                text=button['text'],
                callback_data=button.get('callback_data', ''),
                url=button.get('url', None)
            ))
        return markup

    @staticmethod
    def get_phone_keyboard() -> ReplyKeyboardMarkup:
        """Создает клавиатуру с кнопкой запроса номера телефона"""
        keyboard = ReplyKeyboardMarkup(resize_keyboard=True)
        button = KeyboardButton("📞 Поделиться номером", request_contact=True)
        keyboard.add(button)
        return keyboard

class MainMenuKeyboard(Keyboard):
    """Клавиатура главного меню"""
    
    @classmethod
    def get_keyboard(cls) -> ReplyKeyboardMarkup:
        buttons = [
            f"{ui_config.EMOJIS['level']} Дізнатися рівень англійської",
            f"{ui_config.EMOJIS['money']} Купити курс",
            f"{ui_config.EMOJIS['calendar']} Записатись на пробний урок",
            f"{ui_config.EMOJIS['phone']} Зв'язатись з менеджером"
        ]
        return cls.create_reply_keyboard(buttons, row_width=1)

class LevelSelectionKeyboard(Keyboard):
    """Клавиатура выбора уровня"""
    
    @classmethod
    def get_keyboard(cls) -> ReplyKeyboardMarkup:
        buttons = [
            f"A1 (Початковий) {ui_config.EMOJIS['level']}", 
            f"A2 (Елементарний) {ui_config.EMOJIS['level']}",
            f"B1 (Середній) {ui_config.EMOJIS['level']}", 
            f"B2+ (Вище середнього) {ui_config.EMOJIS['level']}",
            f"C1 (Просунутий) {ui_config.EMOJIS['level']}", 
            f"C2 (Вільне володіння) {ui_config.EMOJIS['level']}",
            f"{ui_config.EMOJIS['test']} Дізнатися рівень англійської"
        ]
        return cls.create_reply_keyboard(buttons, row_width=2)

class TestKeyboard(Keyboard):
    """Клавиатура для тестирования"""
    
    @classmethod
    def get_answer_keyboard(cls, answers: List[str]) -> ReplyKeyboardMarkup:
        return cls.create_reply_keyboard(answers, row_width=1)

class SurveyKeyboard(Keyboard):
    """Клавиатуры для опроса"""
    
    @staticmethod
    def get_motivation_keyboard() -> ReplyKeyboardMarkup:
        buttons = ["1", "2", "3", "4", "5"]
        return Keyboard.create_reply_keyboard(buttons)
    
    @staticmethod
    def get_time_keyboard() -> ReplyKeyboardMarkup:
        buttons = ["1-2 години", "3-4 години", "5-7 годин"]
        return Keyboard.create_reply_keyboard(buttons)
    
    @staticmethod
    def get_budget_keyboard() -> ReplyKeyboardMarkup:
        buttons = [
            "100-300 грн",
            "300-500 грн",
            "500-700 грн",
            "Я поки не знаю, хочу розібратися"
        ]
        return Keyboard.create_reply_keyboard(buttons)
    
    @staticmethod
    def get_goal_keyboard() -> ReplyKeyboardMarkup:
        buttons = [
            "Для роботи",
            "Для подорожей",
            "Для переїзду",
            "Для навчання",
            "Для розвитку особистих навичок",
            "Інше"
        ]
        return Keyboard.create_reply_keyboard(buttons, row_width=2)
    
    @staticmethod
    def get_start_preference_keyboard() -> ReplyKeyboardMarkup:
        keyboard = ReplyKeyboardMarkup(resize_keyboard=True)
        keyboard.add("Хочу почати відразу")
        keyboard.add("Спочатку пробне заняття")
        return keyboard
    
    @staticmethod
    def get_payment_keyboard() -> ReplyKeyboardMarkup:
        keyboard = ReplyKeyboardMarkup(resize_keyboard=True)
        keyboard.add("Оплата одразу за курс")
        keyboard.add("Оплата частинами")
        keyboard.add("Оплата за кожне заняття")
        return keyboard
    
    @staticmethod
    def get_start_choice_keyboard() -> ReplyKeyboardMarkup:
        buttons = [
            "Так, я готовий розпочати навчання негайно",
            "Ні, хочу спочатку пройти пробне заняття"
        ]
        return Keyboard.create_reply_keyboard(buttons)
    
    @staticmethod
    def get_ninth_question_keyboard() -> ReplyKeyboardMarkup:
        buttons = [
            "Так, мені потрібна допомога",
            "Ні, я впевнений у своїх знаннях"
        ]
        return Keyboard.create_reply_keyboard(buttons)
