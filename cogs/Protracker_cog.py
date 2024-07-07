import aiohttp
import disnake
from disnake.ext import commands
from fake_useragent import UserAgent
from bs4 import BeautifulSoup as BS
class Protracker(commands.Cog):
    def __init__(self,bot):
        self.bot = bot

    @commands.slash_command()
    async def itembuild(self, inter, hero, pos):
        item_list = await tracker(hero, pos)
        print(item_list)
        count = 0
        embed = disnake.Embed()
        for items in item_list:
            # Создаем один общий Embed
            count+=1
            if count == 1:
                await inter.send("Starting Items")
            elif count == 2:
                await inter.send("Early Game (00:00 - 12:00)")
            elif count == 3:
                await inter.send("Mid Game (12:00 - 35:00)")
            elif count == 4:
                await inter.send("Late Game (35:00+)")
            for x, b in zip(items[0::2], items[1::2]):
                embed.title = b  # Добавляем поле в Embed
                embed.set_image(url=x)  # Устанавливаем изображение в Embed
                await inter.send(embed=embed)


async def tracker(hero,pos):
    aw = " "
    for i in hero.split(" "):
        i = i[0].upper() + i[1:].lower()
        aw.join(i)
    url = f"https://dota2protracker.com/hero/{hero}/new"
    positions = {"carry": 1,
                 "mid": 2,
                 "offlane": 3,
                 "pos 4": 4,
                 "pos 5": 5
                 }
    if pos.lower() in positions:
        pos = positions.get(pos.lower())
    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(url, headers= {"UserAgent":UserAgent().random}) as response:
                r = await aiohttp.StreamReader.read(response.content)
                pos = int(pos)
                soup = BS(r, "html.parser")
                block = soup.find("div",class_="flex flex-col lg:flex-row gap-2")
                post = block.find_all("div", class_="flex gap-2 items-center text-sm lg:text-lg")
                count =1
                for i in post:
                    if i.find("span") == None:
                        count+=1
                    else:
                        break
                if pos == count:
                    block = soup.find("div", class_="flex flex-col tabs-navigation contentR gap-2")
                    jj = block.find("div", class_="flex flex-col 2md:flex-row tabs-players gap-2 flex-1")
                    aa = jj.find("div", class_="flex flex-col")
                    yy = aa.find("div", class_="grid grid-cols-1 2md:grid 2md:grid-cols-2 gap-2 text-sm")
                    cc = yy.find_all("div",
                                     class_="flex flex-col p-4 gap-2 rounded-md bg-d-gray-5 border-[1px] border-solid border-d-gray-8 col-span-2")
                    items_lists = []
                    for i in cc:
                        vv = i.find("div", class_="flex")
                        print(vv.get_text())
                        gg = i.find_all("div", class_="flex justify-center text-xs text-white")
                        dd = i.find_all("div",
                                        class_="w-[32px] h-[24px] text-xs text-white text-shadow font-medium text-right rounded-md")
                        block_list = []
                        for b, x in zip(dd, gg):
                            b = "https://dota2protracker.com" + b.get("style")[22:-30]
                            block_list.append(b)
                            block_list.append(x.get_text()[1:-1])

                        items_lists.append(block_list)

                    return items_lists
                else:
                    bb = soup.find_all("div",class_="flex flex-col tabs-navigation contentR hidden gap-2")
                    bb = bb[pos-1]
                    jj = bb.find("div",class_="flex flex-col 2md:flex-row tabs-players gap-2 flex-1")
                    aa = jj.find("div",class_="flex flex-col")
                    yy = aa.find("div",class_="grid grid-cols-1 2md:grid 2md:grid-cols-2 gap-2 text-sm")
                    cc = yy.find_all("div",class_="flex flex-col p-4 gap-2 rounded-md bg-d-gray-5 border-[1px] border-solid border-d-gray-8 col-span-2")
                    items_lists = []
                    for i in cc:
                        vv = i.find("div", class_="flex")
                        print(vv.get_text())
                        gg = i.find_all("div", class_="flex justify-center text-xs text-white")
                        dd = i.find_all("div",class_="w-[32px] h-[24px] text-xs text-white text-shadow font-medium text-right rounded-md")
                        block_list = []
                        for b, x in zip(dd, gg):
                            b = "https://dota2protracker.com" + b.get("style")[22:-30]
                            block_list.append(b)
                            block_list.append(x.get_text()[1:-1])

                        items_lists.append(block_list)

                    return items_lists
    except AttributeError:
        error = "Нет такого героя!"
        return error


def setup(bot):
    bot.add_cog(Protracker(bot))