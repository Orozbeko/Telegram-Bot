from aiogram import Router, F, types
from aiogram.filters import Command

shop_router = Router()

@shop_router.message(Command("shop"))
async def show_categories(message: types.Message):
    kb = types.ReplyKeyboardMarkup(
        keyboard=[
            [
                types.KeyboardButton(text="Диаметр-35см"),
                types.KeyboardButton(text="Диаметр-30см")
            ],
            [
                types.KeyboardButton(text="Диаметр-25см"),
            ]
        ],
        resize_keyboard=True
    )
    await message.answer("пиццы по размеру:", reply_markup=kb)
types_pizza= ("Диаметр-35см", "Диаметр-30с", "Диаметр-25см")


@shop_router.message(F.text.lower().in_(types_pizza))
async def show_triller(message: types.Message):
    type_pizza = message.text
    kb = types.ReplyKeyboardRemove()
    await message.answer(f"Пиццы с диаметром: {type_pizza}", reply_markup=kb)