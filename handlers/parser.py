import httpx
from parsel import Selector
from bot import dp, types
from aiogram import Router
from aiogram.filters import Command
from house_parser.car_kg import HouseCrawler
car_router = Router()



@car_router.message(Command("links"))
async def links(message: types.Message):
    crawler = HouseCrawler()
    title = await crawler.get_title()
    if title:
        link = await crawler.get_property_links()
        if link:
            await message.answer(f"Имя: {title}, ссылка {link}")
        else:
            await message.answer("Не удалось найти ссылки на объекты")
    else:
        await message.answer("Не удалось получить заголовок страницы")
