import re
import requests
from telegram import Update
from telegram.ext import CallbackContext
from BotMessages import get_message
from settings import PASTEBIN_DEV_KEY,PASTEBIN_USER_NAME,PASTEBIN_USER_PASSWORD


class Runner:
    msg_options = {"parse_mode": "HTML", "disable_web_page_preview": True}

    def __init__(self):
        pass

    async def just_answer(self, update: Update, context: CallbackContext, key: str) -> None:
        await context.bot.send_message(
            chat_id=update.message.chat_id,
            text=get_message(key, update.message.from_user.language_code),
            **self.msg_options
        )

    def remove_bot_call(self, message: str) -> str:
        return re.sub(r'^[/][A-Za-z0-9@_-]+\s*', '', message)

    async def process_paste(self, update: Update, context: CallbackContext) -> None:
        message = update.message.text
        username = update.message.from_user.username or update.message.from_user.full_name
        language = update.message.from_user.language_code
        message_id = update.message.message_id
        chat_id = update.message.chat_id

        try:
            login_data = {
                'api_dev_key': PASTEBIN_DEV_KEY,
                'api_user_name': PASTEBIN_USER_NAME,
                'api_user_password': PASTEBIN_USER_PASSWORD
            }
            user_key = self.generateUserKey(login_data)

            data = {
                'api_option': 'paste',
                'api_dev_key': PASTEBIN_DEV_KEY,
                'api_paste_code': message,
                'api_paste_name': "GenAtoZBot",
                'api_user_key': user_key
            }
            paste_url = self.paste(data)

            msg = get_message('sent', language).format(username, paste_url)
            # Correctly await the send_message call
            await context.bot.send_message(chat_id, msg, **self.msg_options)
        except ValueError:
            msg = get_message('paste_empty', language)
            # Correctly await the send_message call
            await context.bot.send_message(chat_id, msg, **self.msg_options)
            return

    def generateUserKey(self, data):
        login = requests.post(
            "https://pastebin.com/api/api_login.php", data=data)
        return login.text

    def paste(self, data):
        r = requests.post("https://pastebin.com/api/api_post.php", data=data)
        return r.text
