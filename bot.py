import asyncio
import os
import json
from aiogram import Bot, Dispatcher, F
from aiogram.types import Message, ReplyKeyboardMarkup, KeyboardButton, FSInputFile
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.storage.memory import MemoryStorage

TOKEN = os.environ["TELEGRAM_BOT_TOKEN"]
ADMIN_USERNAME = "DESIGNCONNECTER"
ADMIN_ID_FILE = "admin_chat_id.json"


def load_admin_chat_id() -> int | None:
    if os.path.exists(ADMIN_ID_FILE):
        try:
            with open(ADMIN_ID_FILE, "r") as f:
                data = json.load(f)
                return data.get("chat_id")
        except Exception:
            return None
    return None


def save_admin_chat_id(chat_id: int):
    with open(ADMIN_ID_FILE, "w") as f:
        json.dump({"chat_id": chat_id}, f)


bot = Bot(token=TOKEN)
storage = MemoryStorage()
dp = Dispatcher(storage=storage)

admin_chat_id: int | None = load_admin_chat_id()

if admin_chat_id:
    print(f"[ADMIN] Loaded saved admin chat ID: {admin_chat_id}")
else:
    print(f"[ADMIN] No admin registered yet. @{ADMIN_USERNAME} must send /start to the bot.")


class OrderState(StatesGroup):
    waiting_for_details = State()


menu = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="🛒 Заказать дизайн"), KeyboardButton(text="💰 Прайс")],
        [KeyboardButton(text="📢 Портфолио"), KeyboardButton(text="ℹ️ Информация")],
        [KeyboardButton(text="📩 Связаться")]
    ],
    resize_keyboard=True,
    persistent=True
)


@dp.message(F.text == "/start")
async def start(message: Message, state: FSMContext):
    global admin_chat_id
    uname = message.from_user.username or ""
    print(f"[START] from @{uname} (ID: {message.chat.id})")
    if uname.lower() == ADMIN_USERNAME.lower():
        admin_chat_id = message.chat.id
        save_admin_chat_id(admin_chat_id)
        print(f"[ADMIN] Registered admin chat ID: {admin_chat_id}")
        await message.answer(
            "✅ Готово! Теперь все заявки от клиентов будут приходить сюда.",
            reply_markup=menu
        )
        return
    await state.clear()
    gif_path = os.path.join(os.path.dirname(__file__), "welcome.jpg")
    welcome_text = (
        "Привет! 👋\n\n"
        "Я бот-помощник DESIGN CONNECT.\n\n"
        "Помогаю продавцам маркетплейсов создавать/улучшать карточки товаров, "
        "выделяться среди конкурентов и повышать привлекательность товаров для покупателей.\n\n"
        "Что можно заказать:\n\n"
        "✅ Анализ карточки товара\n"
        "✅ Редизайн существующей карточки\n"
        "✅ Создание карточки с нуля\n"
        "✅ Главное фото (CTR-слайд)\n"
        "✅ Инфографику для маркетплейсов\n"
        "✅ Анализ конкурентов\n"
        "✅ Оформление товарной линейки\n\n"
        "Выберите действие ниже:"
    )
    if os.path.exists(gif_path):
        await message.answer_photo(
            FSInputFile(gif_path),
            caption=welcome_text,
            reply_markup=menu
        )
    else:
        await message.answer(welcome_text, reply_markup=menu)


@dp.message(F.text == "💰 Прайс")
async def price(message: Message):
    await message.answer(
        "💰 ПРАЙС\n\n"
        "0️⃣ Главное фото / первый слайд карточки\n"
        "Создание коммерчески сильного первого слайда для маркетплейса\n"
        "Включает: крупное изображение товара, заголовок, иконки выгод, визуальный крючок\n"
        "Цель: мгновенно зацепить покупателя и увеличить CTR\n"
        "💰 По договоренности\n\n"
        "1️⃣ Анализ карточки товара\n"
        "Разбор текущей карточки\n"
        "Выявление ошибок и точек роста\n"
        "💰 По договоренности\n\n"
        "2️⃣ Редизайн существующей карточки\n"
        "Новый дизайн без потери информации\n"
        "Концепция + визуал + текст\n"
        "💰 По договоренности\n\n"
        "3️⃣ Создание карточки с нуля\n"
        "Полный коммерческий дизайн\n"
        "Фото, инфографика, текст, CTA\n"
        "💰 По договоренности\n\n"
        "4️⃣ Инфографика для маркетплейсов\n"
        "Привлекательные блоки с преимуществами\n"
        "Лаконично, читаемо, продающе\n"
        "💰 По договоренности\n\n"
        "5️⃣ Анализ конкурентов\n"
        "Визуальный и коммерческий разбор\n"
        "Точки роста и рекомендации\n"
        "💰 По договоренности\n\n"
        "6️⃣ Полное оформление товарной линейки\n"
        "Комплексный подход к всей линейке\n"
        "Стиль + визуал + инфографика + тексты\n"
        "💰 По договоренности",
        reply_markup=menu
    )


@dp.message(F.text == "📢 Портфолио")
async def channel(message: Message):
    await message.answer(
        "📢 Портфолио: https://t.me/DESIGN_CONNECTER",
        reply_markup=menu
    )


@dp.message(F.text == "📩 Связаться")
async def contact(message: Message):
    await message.answer(
        "📩 Напишите сообщение:\n\n"
        "• описание задачи\n"
        "• идея\n"
        "• вопрос\n"
        "• ссылка или фото",
        reply_markup=menu
    )


@dp.message(F.text == "ℹ️ Информация")
async def info(message: Message):
    await message.answer(
        "ℹ️ DESIGN CONNECT\n\n"
        "Создаю и редизайню карточки товаров для Wildberries и Ozon.\n\n"
        "Моя задача — не просто сделать красивую картинку, а помочь товару привлекать внимание среди конкурентов и увеличивать количество переходов в карточку.\n\n"
        "В работе использую:\n\n"
        "• анализ конкурентов;\n"
        "• коммерческий дизайн;\n"
        "• инфографику для маркетплейсов;\n"
        "• современные визуальные тренды;\n"
        "• нейросети и AI-инструменты;\n"
        "• проработку первого слайда для повышения CTR.\n\n"
        "Услуги:\n\n"
        "✅ Анализ карточки товара\n"
        "✅ Главное фото (CTR-слайд)\n"
        "✅ Редизайн существующей карточки\n"
        "✅ Создание карточки с нуля\n"
        "✅ Инфографика для маркетплейсов\n"
        "✅ Анализ конкурентов\n"
        "✅ Полное оформление товарной линейки\n\n"
        "Работаю с различными категориями товаров:\n\n"
        "• косметика;\n"
        "• товары для дома;\n"
        "• электроника;\n"
        "• инструменты;\n"
        "• спорт и фитнес;\n"
        "• детские товары;\n"
        "• авто- и мототовары;\n"
        "• товары для животных;\n"
        "• и другие ниши.\n\n"
        "Стоимость работ обсуждается индивидуально и зависит от объёма задачи.",
        reply_markup=menu
    )


@dp.message(F.text == "🛒 Заказать дизайн")
async def order_start(message: Message, state: FSMContext):
    await state.set_state(OrderState.waiting_for_details)
    await message.answer(
        "🛒 Опишите ваш заказ:\n\n"
        "• редизайн или с нуля?\n"
        "• ссылка или фото товара\n"
        "• пожелания по стилю\n\n"
        "Отправьте одно сообщение — и я передам заявку дизайнеру.",
        reply_markup=menu
    )


@dp.message(OrderState.waiting_for_details)
async def order_receive(message: Message, state: FSMContext):
    await state.clear()

    user = message.from_user
    username = f"@{user.username}" if user.username else f"(ID: {user.id})"
    name = user.full_name or "Без имени"

    print(f"[ORDER] Received from {name} {username}")
    print(f"[ORDER] admin_chat_id = {admin_chat_id}")

    header = (
        f"📋 НОВАЯ ЗАЯВКА\n\n"
        f"👤 {name} {username}\n\n"
        f"📝 Детали заказа:\n"
    )

    if admin_chat_id:
        print(f"[ORDER] Sending to admin {admin_chat_id}...")
        if message.text:
            await bot.send_message(admin_chat_id, header + message.text)
        elif message.photo:
            caption = header + (message.caption or "")
            await bot.send_photo(admin_chat_id, message.photo[-1].file_id, caption=caption)
        elif message.document:
            caption = header + (message.caption or "")
            await bot.send_document(admin_chat_id, message.document.file_id, caption=caption)
        else:
            await bot.send_message(admin_chat_id, header + "[Медиафайл]")
        print(f"[ORDER] Successfully sent to admin.")
    else:
        print(f"[ORDER] No admin registered — skipping forward.")

    await message.answer(
        "✅ Заявка принята! Дизайнер свяжется с вами в ближайшее время.",
        reply_markup=menu
    )


async def main():
    print("DESIGN CONNECT bot is starting...")
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
