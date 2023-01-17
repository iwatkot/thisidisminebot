import json
import logging
import sys
import os

from aiogram import Bot, Dispatcher, executor, types
from decouple import config

LOG_FILE = 'logs/main_log.txt'
USERS_FILE = 'users.json'
users = json.load(open(USERS_FILE))
TOKEN = config('TOKEN')
try:
    os.mkdir('./logs')
except FileExistsError:
    pass

logging.basicConfig(level=logging.INFO, filename=LOG_FILE, filemode='a',
                    format="%(asctime)s %(levelname)s %(message)s")
logging.getLogger().addHandler(logging.StreamHandler(sys.stdout))

bot = Bot(token=TOKEN)
dp = Dispatcher(bot=bot)


@dp.message_handler()
async def message_handler(message: types.Message):
    # Handles the all messages.
    user_data = message.from_user
    user_id = user_data.id
    logging.info(f"{user_id}: {message['text']}")
    if user_id not in users:
        users.append(user_id)
        json.dump(users, open(USERS_FILE, 'w'))
    userinfo = "_Here's information about your telegram account:_\n\n"
    userinfo += "*ID:* `{}`\n".format(user_data['id'])
    userinfo += "*Language:* {}\n".format(user_data['language_code'])
    userinfo += "*Username:* `{}`\n".format(user_data['username'])
    userinfo += "*First name:* `{}`\n".format(user_data['first_name'])
    userinfo += "*Last name:* `{}`\n".format(user_data['last_name'])
    if user_data['is_premium']:
        premium_info = 'Yes'
    else:
        premium_info = 'No'
    userinfo += "*Premium user:* {}\n".format(premium_info)
    await message.reply(userinfo, parse_mode='MarkdownV2')


if __name__ == "__main__":
    executor.start_polling(dp)
