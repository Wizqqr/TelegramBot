from aiogram.fsm.context import FSMContext
from keyboards.choice_kb import service_kb
from bookservice.bookservice import BookService
from aiogram import types, F, Router

callback_router = Router()


@callback_router.callback_query(F.data == 'address')
async def address(callback: types.CallbackQuery):
    await callback.message.answer(text = 'наш адресс : тут близко')


@callback_router.callback_query(F.data == 'phone')
async def phone(callback: types.CallbackQuery):
    await callback.message.answer(text = 'наш телефон : 0996123456789')


quality_responses = {
    'excellent': "You've chosen Excellent",
    'good': "You've chosen good",
    'bad': "You've chosen bad",
    'normal': "You've chosen normal"
}
cleanable_responses = {
    'low': "You've chosen low",
    'medium': "You've chosen medium",
    'high': "You've chosen high"
    }

@callback_router.callback_query(F.data.in_(('excellent', 'good', 'bad', 'normal')))
async def choose_quality(callback: types.CallbackQuery, state: FSMContext):
    quality = callback.data
    await update_quality(callback, state, quality)


async def update_quality(callback: types.CallbackQuery, state: FSMContext, quality: str):
    await callback.answer(quality_responses[quality])
    await state.update_data({'quality': quality})
    await state.set_state(BookService.cleanable)
    await callback.message.answer(f'You chose "{quality}". Could you rate our service?', reply_markup=service_kb())


@callback_router.callback_query(F.data.in_(('low', 'high', 'medium')))
async def finish(callback: types.CallbackQuery, state: FSMContext):
    cleanable = callback.data
    await update_finish(callback,state,cleanable)


async def update_finish(callback: types.CallbackQuery, state:FSMContext, cleanable:str):
    await callback.answer(cleanable_responses[cleanable])
    await state.update_data({'cleanable': cleanable})
    await state.set_state(BookService.last)
    await callback.message.answer('Thank you for finishing! \nWould you like to write some cmment?')


