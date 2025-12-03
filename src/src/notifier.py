from telegram import Bot
import logging

class TelegramNotifier:
    def __init__(self, token, chat_id):
        self.bot = Bot(token=token)
        self.chat_id = chat_id

    def send(self, message):
        try:
            self.bot.send_message(chat_id=self.chat_id, text=message)
            logging.info("Telegram message sent.")
        except Exception as e:
            logging.exception("Failed to send telegram message: %s", e)
