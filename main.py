import telegram
from telegram.ext import Updater, CommandHandler
import schedule
import time
import threading
from datetime import datetime
import asyncio

TOKEN = '7255713106:AAEAd9hGWnZZMa6kC38o8xbNRGh_D4oS8b0'


def send_alarm(context):
    job = context.job
    context.bot.send_message(chat_id=job.context, text='⏰ Время просыпаться!')


def set_alarm(update, context):
    chat_id = update.message.chat_id

    try:

        alarm_time = context.args[0]
        alarm_time_obj = datetime.strptime(alarm_time, "%H:%M")
        current_time_obj = datetime.now()


        time_difference = (alarm_time_obj - current_time_obj).seconds
        if time_difference < 0:
            update.message.reply_text("Невозможно установить время в прошлом!")
            return

        context.job_queue.run_once(send_alarm, time_difference, context=chat_id)
        update.message.reply_text(f"Будильник установлен на {alarm_time}!")

    except (IndexError, ValueError):
        update.message.reply_text("Используйте формат: /set <часы:минуты>")

def unset_alarm(update, context):
    job_removed = remove_job_if_exists(str(update.message.chat_id), context)
    text = 'Будильник отключен!' if job_removed else 'Активного будильника нет.'
    update.message.reply_text(text)

def remove_job_if_exists(name, context):
    current_jobs = context.job_queue.get_jobs_by_name(name)
    if not current_jobs:
        return False
    for job in current_jobs:
        job.schedule_removal()
    return True

def main():
     updater = Updater(TOKEN, use_context=True)

        dp = updater.dispatcher
        dp.add_handler(CommandHandler("set", set_alarm, pass_args=True, pass_job_queue=True))
        dp.add_handler(CommandHandler("unset", unset_alarm))


    updater.start_polling()
    updater.idle()


if __name__ == '__main__':
    asyncio.run(main())



