import disnake
from disnake.ext import commands
import fake_useragent
import requests
import json
from bs4 import BeautifulSoup
from cogs.rest.restapi_req import restapi_funcs


class Buff(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.rating = restapi_funcs.get_dict_records("Data", "rate")
        with open("data/data.json", "w") as f:
            json.dump(self.rating,f,indent=4)
        self.data_messages = restapi_funcs.get_dict_records("Data", "messages")
        with open("data/data_messages.json", "w") as f:
            json.dump(self.data_messages,f,indent=4)
        self.data_time = restapi_funcs.get_dict_records("Time", ["time", "circles"], convert_types=[float, int])
        with open('data/time_data.json', 'w') as f:
            json.dump(self.data_time, f, indent=4)
        self.buff_data = restapi_funcs.get_dict_records("Data", "buffID")
        with open("data/buff_id_data.json", "w") as f:
            json.dump(self.buff_data,f,indent=4)

    @commands.slash_command()
    async def buff(self, inter, id):
        await inter.response.defer()
        try:
            if id in self.buff_data:
                id = self.buff_data[id]
                if id == "N/A":
                    await inter.send("Ваш ID указан не верно, попробуйте функцию myid.")
                    return
            header = {"user-agent": fake_useragent.UserAgent().random}
            img, tex = parser(id, header)
            embed = disnake.Embed(
                colour=disnake.Colour.from_rgb(8, 60, 84),
                title=tex
            )
            embed.set_thumbnail(url=img)
            await inter.send(embed=embed)
        except Exception as e:
            print("abb")
            print(e)
            await inter.send("Ошибка! Такого ID нет")

    @commands.slash_command(description="Укажи свой id стима или доты, чтобы ты смог удобно чекать стату")
    async def myid(self, inter, id):
        try:
            self.buff_data[f"<@{inter.user.id}>"] = int(id)
            restapi_funcs.update_field_by_discordid("Data",f"<@{inter.user.id}>","buffID",int(id),increment=False)
            await inter.send("Твой id успешно изменён!")
            with open("data/buff_id_data.json", "w") as f:
                json.dump(self.buff_data, f, indent=4)
        except:
            await inter.send("Возникла ошибка, попробуйте ещё раз.")



def parser(id,header):
    id = int(id)
    url = f"https://ru.dotabuff.com/players/{id}/matches"
    response = requests.get(url, headers=header)
    soup = BeautifulSoup(response.text, "lxml")
    block_img = soup.find("div", class_="header-content-avatar")
    img = block_img.find("img").get("src")
    block = soup.find("div", class_="header-content-secondary")
    all_state = block.find_all("dd")
    all_text = block.find_all("dt")
    gay_sex = " ".join([all_text[0].get_text(), all_state[0].get_text()])
    ultra_gay_Sex = " ".join([all_text[1].get_text(), all_state[1].get_text()])
    Mega_gay_Sex = " ".join([all_text[2].get_text(), all_state[2].get_text()])
    return img, f"{gay_sex} \n{ultra_gay_Sex} \n{Mega_gay_Sex}"

def setup(bot):
    bot.add_cog(Buff(bot))
