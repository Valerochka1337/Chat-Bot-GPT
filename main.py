from aiogram import Bot, executor, Dispatcher, types
import openai
import pandas as pd
from json import loads, dumps
from datetime import timedelta

# Set the OpenAI API key
openai.api_key = "YOUR_TOKEN"

# Initialize the bot and dispatcher
bot = Bot("YOUR_TOKEN")
dp = Dispatcher(bot)

# Load user data from the CSV file
users = pd.read_csv("users.csv", index_col="user_id")


@dp.message_handler(commands=["start"])
async def start_command(message: types.Message):
    """
    Handler for the "/start" command.
    Sends a welcome back message if the user is registered, otherwise registers the user and sends a welcome message.
    """
    global users
    user_id = message.from_user.id

    if user_id in users.index:
        await bot.send_message(message.chat.id, "И снова здравствуй, " + message.from_user.first_name + "!")
    else:
        users.loc[user_id] = [2000, 0, message.date, 2000, 0, "[]"]
        await bot.send_message(message.chat.id, "Привет, " + message.from_user.first_name + "!")


@dp.message_handler(commands=["tokens"])
async def tokens_command(message: types.Message):
    """
    Handler for the "/tokens" command.
    Checks if the user is registered and eligible to request tokens.
    If eligible, resets the token count, updates the last request date, and informs the user about token replenishment.
    """
    global users
    user_id = message.from_user.id

    if user_id in users.index:
        if pd.to_datetime(users.loc[user_id, "last_date"]) + timedelta(minutes=3) > message.date:
            await bot.send_message(message.chat.id, "Попробуйте через 3 минуты")
        else:
            users.loc[user_id, "tokens"] = 0
            users.loc[user_id, "last_date"] = message.date
            await bot.send_message(message.chat.id, "Запас токенов пополнен!")
    else:
        await bot.send_message(message.chat.id, "Арр, сначала нужно зарегистрироваться!")


@dp.message_handler()
async def respond(message: types.Message):
    """
    Handler for user messages.
    Generates a response using the OpenAI Chat API and sends it back to the user.
    """
    global users
    user_id = message.from_user.id

    if user_id not in users.index:
        await bot.send_message(message.chat.id, "Аррр, извините, нужно зарегистрироваться сначала!")
    else:
        if users.loc[user_id, 'tokens'] >= users.loc[user_id, 'token_capacity']:
            await bot.send_message(message.chat.id, "Аррр, у вас закончились токены, пополните из запас!")
        else:
            context = loads(users.loc[user_id, "context"]) + [{"role": "user", "content": message.text}]
            context_len = users.loc[user_id, "context_len"] + len(message.text)

            while context_len > users.loc[user_id, "context_capacity"]:
                context_len -= len(context[0]["content"])
                context = context[1:]

            instruction = [{"role": "system", "content": "говори коротко и как пират"}]
            context_with_instructions = instruction + context

            await message.answer_chat_action("typing")

            try:
                response = openai.ChatCompletion.create(
                    model="gpt-3.5-turbo-0613",
                    messages=context_with_instructions,
                    max_tokens=500,
                    n=1,
                    temperature=0.7,
                )
            except:
                await bot.send_message(message.chat.id, "Слишком большая нагрузка на сервер, попробуйте позже")
                return

            text_answer = response.choices[0].message["content"]
            context += [{"role": "assistant", "content": text_answer}]
            context_len += len(text_answer)

            users.loc[user_id, "tokens"] += response["usage"]["total_tokens"]
            users.loc[user_id, "context_len"] = context_len
            users.loc[user_id, "context"] = dumps(context, ensure_ascii=False)

            await bot.send_message(message.chat.id, text_answer)


if __name__ == '__main__':
    # Start the bot
    executor.start_polling(dp)

# Save user data to the CSV file
users.to_csv("users.csv")
