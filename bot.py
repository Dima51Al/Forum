import logging
from telegram import Update, ReplyKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ContextTypes
from main import generate_task, split_gen
from dotenv import load_dotenv
import os

load_dotenv()
TOKEN = os.getenv("API_TOKEN")

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

keyboard = ReplyKeyboardMarkup(
    [["Сгенерировать вопрос"]],
    resize_keyboard=True
)


# обработчик команды /start
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "Здравствуйте! Нажмите кнопку ниже для генерации вопроса.",
        reply_markup=keyboard
    )
    logger.info(f"Пользователь {update.message.from_user.username} запустил команду /start")


# обработчик нажатия кнопки
async def handle_button(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_message = update.message.text
    logger.info(f"Пользователь {update.message.from_user.username} нажал: {user_message}")

    if user_message == "Сгенерировать вопрос":
        try:
            req = split_gen()
            res1 = req[0] if len(req) > 0 else "Default Response 1"
            res2 = req[1] if len(req) > 1 else "Default Response 2"

            context.user_data["correct_answer"] = res2

            await update.message.reply_text(res1)
        except Exception as e:
            logger.error(f"Ошибка в split_gen: {e}")
            await update.message.reply_text("Ошибка генерации вопроса. Попробуйте позже.")
    else:

        correct_answer = context.user_data.get("correct_answer")
        if correct_answer:
            if user_message.strip().lower() == str(correct_answer).strip().lower():
                await update.message.reply_text("Ответ правильный! Нажмите кнопку для следующего вопроса.")
            else:
                await update.message.reply_text(
                    "Ответ неправильный. Попробуйте еще раз или нажмите кнопку для нового вопроса.")
        else:
            await update.message.reply_text("Пожалуйста, сначала нажмите кнопку 'Сгенерировать вопрос'.")


def main():
    application = ApplicationBuilder().token(TOKEN).build()

    application.add_handler(CommandHandler('start', start))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_button))

    application.run_polling()


if __name__ == '__main__':
    main()
