from flask import Flask, request
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ContextTypes
from Runner import Runner as UpdatedRunner
import os
from dotenv import load_dotenv

app = Flask(__name__)
load_dotenv()

TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")

class TelegramBot:
    def __init__(self):
        self.application = None
        self.bot = None
        self.Runner = None

    def main(self):
        """Start the bot."""
        self.application = ApplicationBuilder().token(TELEGRAM_TOKEN).build()
        self.bot = self.application.bot
        self.Runner = UpdatedRunner()

        # Register handlers
        self.application.add_handler(
            CommandHandler("paste", self.receive_paste))
        self.application.add_handler(CommandHandler(
            "start", self.start_command, filters=filters.ChatType.PRIVATE))
        self.application.add_handler(CommandHandler(
            "help", self.help_command, filters=filters.ChatType.PRIVATE))
        self.application.add_handler(MessageHandler(
            filters.TEXT & ~filters.COMMAND & filters.ChatType.PRIVATE, self.receive_paste))

        # Start polling
        self.application.run_polling()

    async def start_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
        """Send a message when the command /start is issued."""
        await self.Runner.just_answer(update, context, "start")

    async def help_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
        """Send a message when the command /help is issued."""
        await self.Runner.just_answer(update, context, "help")

    async def receive_paste(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
        """Receive the code to send to pastebin."""
        await self.Runner.process_paste(update, context)


if __name__ == '__main__':
    bot = TelegramBot()
    bot.main()
