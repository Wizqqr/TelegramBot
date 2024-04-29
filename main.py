import asyncio
from aiogram import Bot, types
from aiogram.filters import Command
import logging
from bot import dp,bot, set_my_menu, database
from handlers.start import start_router
from handlers.callback import callback_router
from handlers.menu import menu_router
from handlers.service import service_router
from handlers.shop import shop_router
from handlers.parser import car_router


async def on_startup(bot: Bot):
    await database.create_tables()
async def main():
    await set_my_menu()
    dp.include_router(start_router)
    dp.include_router(callback_router)
    dp.include_router(menu_router)
    dp.include_router(service_router)
    dp.include_router(shop_router)
    dp.include_router(car_router)
    dp.startup.register(on_startup)

    await dp.start_polling(bot)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    asyncio.run(main())
