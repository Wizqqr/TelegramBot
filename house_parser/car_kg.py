import httpx
from parsel import Selector
from bot import dp, types
from aiogram import Router
from aiogram.filters import Command

parser_router = Router()


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
        html = Selector(self.page_content)
        links = html.css(".listing a::attr(href)").getall()
        full_links = list(map(lambda x: self.BASE_URL + x, links))
        return full_links[:1]


