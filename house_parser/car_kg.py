import httpx
from parsel import Selector
from bot import dp, types
from aiogram import Router
from aiogram.filters import Command

car_router = Router()


class HouseCrawler:
    MAIN_URL = "https://www.house.kg/snyat"
    BASE_URL = "https://www.house.kg"

    async def get_page(self):
        async with httpx.AsyncClient() as client:
            response = await client.get(self.MAIN_URL)
            if response.status_code == 200:
                self.page_content = response.text
                return response
            else:
                return None

    async def get_title(self):
        page_response = await self.get_page()
        if page_response:
            html = Selector(self.page_content)
            title = html.css("title::text").get()
            return title
        else:
            return None

    async def get_property_links(self):
        page_response = await self.get_page()
        if page_response:
            html = Selector(self.page_content)
            if html.css('.property-list .property-item a::attr(href)').get():
                links = html.css('.property-list .property-item a::attr(href)').getall()
                full_links = [self.BASE_URL + link for link in links]
                return full_links
            else:
                return None
        else:
            return None


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
