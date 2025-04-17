from aiogram import Bot, Dispatcher, types
from aiogram.utils import executor
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from config import BOT_TOKEN
from utils import generate_text
from collections import defaultdict

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher(bot)

# Хранилище лимитов
user_requests = defaultdict(int)
FREE_LIMIT = 5

# Меню-кнопки
menu_kb = ReplyKeyboardMarkup(resize_keyboard=True)
menu_kb.add(
    KeyboardButton("✍️ Сгенерировать пост"),
    KeyboardButton("💡 Идея для бизнеса"),
)
menu_kb.add(
    KeyboardButton("😂 Шутка"),
    KeyboardButton("📜 Цитата"),
    KeyboardButton("🎲 Рандом"),
)

@dp.message_handler(commands=['start'])
async def start_cmd(message: types.Message):
    await message.reply(
        "Привет! Я Genix AI 🤖\nВыбери, что хочешь сгенерировать:",
        reply_markup=menu_kb
    )

@dp.message_handler(commands=['donate'])
async def donate_cmd(message: types.Message):
    donate_text = (
        "🙏 Спасибо, что пользуешься Genix AI!\n\n"
        "Ты можешь поддержать проект через:\n"
        "💰 Boosty: https://boosty.to/твоя_ссылка\n"
        "💳 QIWI/СБП: +7 999 XXX XX XX\n\n"
        "После доната напиши мне в Telegram, и я включу тебе безлимит 🚀"
    )
    await message.reply(donate_text)

@dp.message_handler()
async def handle_text(message: types.Message):
    user_id = message.from_user.id

    if user_requests[user_id] >= FREE_LIMIT:
        await message.reply(
            "🔒 Ты использовал лимит из 5 генераций сегодня.\n"
            "Чтобы получить безлимит — воспользуйся командой /donate 💰"
        )
        return

    prompt_map = {
        "✍️ Сгенерировать пост": "Напиши креативный пост для Telegram",
        "💡 Идея для бизнеса": "Предложи уникальную бизнес-идею",
        "😂 Шутка": "Расскажи весёлую и оригинальную шутку",
        "📜 Цитата": "Поделись вдохновляющей цитатой",
        "🎲 Рандом": "Придумай что-нибудь необычное и прикольное",
    }

    user_input = message.text
    prompt = prompt_map.get(user_input, user_input)

    await message.reply("⏳ Генерирую...")
    result = generate_text(prompt)
    await message.reply(result)

    user_requests[user_id] += 1

if __name__ == "__main__":
    executor.start_polling(dp)
