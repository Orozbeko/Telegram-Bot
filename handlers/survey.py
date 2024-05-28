from aiogram import Router, F, types
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup


survey_router = Router()


# FSM - Finite State Machine
class PizzaSurvey(StatesGroup):
    name = State()
    age = State()
    half = State()
    type_pizza = State()
    purity = State()

@survey_router.message(Command("opros"))
async def start_survey(message: types.Message, state: FSMContext):
    await state.set_state(PizzaSurvey.name)
    await message.answer("Как вас зовут?")

@survey_router.message(PizzaSurvey.name)
async def process_name(message: types.Message, state: FSMContext):
    name = message.text
    # await message.answer(f"Спасибо, {name}!")
    await state.set_state(PizzaSurvey.age)
    await message.answer("Сколько вам лет?")

@survey_router.message(PizzaSurvey.age)
async def process_age(message: types.Message, state: FSMContext):
    age = message.text
    if not age.isdigit():
        await message.answer("Введите число")
        return
    age = int(age)
    if age < 10 or age > 100:
        await message.answer("Введите возраст от 10 до 100")
        return
    await state.set_state(PizzaSurvey.half)
    await message.answer("Ваш пол?")

@survey_router.message(PizzaSurvey.half)
async def process_gender(message: types.Message, state: FSMContext):
    half = message.text
    await state.update_data(half= half)
    await state.set_state(PizzaSurvey.type_pizza)
    await message.answer("Ваш любимый вид пиццы?")

@survey_router.message(PizzaSurvey.type_pizza)
async def process_genre(message: types.Message, state: FSMContext):
    type_pizza = message.text

    await state.update_data(type_pizza=type_pizza)
    kb = types.ReplyKeyboardMarkup(
        keyboard=[
            [types.KeyboardButton(text="отлично")],
            [types.KeyboardButton(text="хорошо")],
            [types.KeyboardButton(text="плохо")]
        ],
        resize_keyboard=True
    )
    await state.set_state(PizzaSurvey.purity)
    await message.answer("Как вы оцениваете наше заведение?", reply_markup=kb)

purity_assessment = ["плохо", "хорошо", "отлично"]

@survey_router.message(PizzaSurvey.purity, F.text.lower().in_(purity_assessment))
async def process_rating(message: types.Message, state: FSMContext):
    purity = message.text
    purity = purity_assessment.index(purity) + 3
    await state.update_data(purity=purity)
    await message.answer("Спасибо за прохождение опроса")
    data = await state.get_data()
    print(data)
    await database.execute(
        "INSERT INTO surveys (name, age, half, type_pizza, purity) VALUES (?, ?, ?, ?, ?)",
        (data["name"], data["age"], data["half"], data["type_pizza"], data["purity"]),
    )
    await state.clear()
