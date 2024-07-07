import disnake
from disnake.ext import commands
import fake_useragent
import requests
import json
from bs4 import BeautifulSoup


class Buff(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        with open("data/buff_id_data.json", "r") as f:
            self.buff_data = json.load(f)

    @commands.slash_command()
    async def buff(self,inter, id):
        if id in self.buff_data:
            id = self.buff_data[id]
        header = {"user-agent": fake_useragent.UserAgent().random}
        img, tex = parser(id,header)
        embed = disnake.Embed(
            title=tex
        )
        embed.set_thumbnail(url=img)
        await inter.send(embed=embed)

    @commands.slash_command(description="Укажи свой id стима или доты, чтобы ты смог удобно чекать стату")
    async def myid(self,inter,id):
       self.buff_data[f"<@{inter.user.id}>"] = int(id)
       await inter.send("Твой id успешно изменён!")
       with open("data/buff_id_data.json", "w") as f:
           json.dump(self.buff_data, f, indent=4)


def parser(id,header):
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