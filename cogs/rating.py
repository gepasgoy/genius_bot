import json
import disnake
from disnake.ext import commands
import time
import asyncio
import random

class BetView(disnake.ui.View):
    def __init__(self, author_id, human_id, bet, reason):
        super().__init__()
        self.author_id = author_id
        self.human_id = human_id
        self.bet = bet
        self.reason = reason
        with open("data/data.json", "r") as f:
            self.rating = json.load(f)

    @disnake.ui.button(label="Поучаствовать на стороне начавшего спор", style=disnake.ButtonStyle.success)
    async def participate_author(self, button: disnake.ui.Button, inter: disnake.MessageInteraction):
        self.add_participant(inter.author.id, 'author')
        if self.human_id != inter.author.id and self.author_id != inter.author.id:
            await inter.response.send_message(f"Вы поучаствовали на стороне <@{self.author_id}>.", ephemeral=True)
        else:
            await inter.response.send_message(f"Думаешь самый умный? Лови -3 рейтинга.", ephemeral=True)
            self.rating[f"<@{inter.author.id}>"] -= 3
            with open("data/data.json", "w") as file:
                json.dump(self.rating, file, indent=4)


    @disnake.ui.button(label="Поучаствовать на стороне другого человека", style=disnake.ButtonStyle.danger)
    async def participate_human(self, button: disnake.ui.Button, inter: disnake.MessageInteraction):
        self.add_participant(inter.author.id, 'human')
        if self.human_id != inter.author.id and self.author_id != inter.author.id:
            await inter.response.send_message(f" вы поучаствовали на стороне <@{self.human_id}>.", ephemeral=True)
        else:
            await inter.response.send_message(f"Думаешь самый умный? Лови -3 рейтинга.", ephemeral=True)
            self.rating[f"<@{inter.author.id}>"] -= 3
            with open("data/data.json", "w") as file:
                json.dump(self.rating, file, indent=4)

    def add_participant(self, user_id, side):
        with open("data/bets.json", "r") as file:
            try:
                bets = json.load(file)
            except json.JSONDecodeError:
                bets = {}
        if self.reason in bets:
            if user_id == bets[self.reason]["author_id"] or user_id == bets[self.reason]["author_id"]:
                return None
            else:
                bets[self.reason]['participants'][str(user_id)] = side

        with open("data/bets.json", "w") as file:
            json.dump(bets,file,indent=4)


def create_bet(author_id, human_id, bet, reason):
    with open("data/bets.json", "r") as file:
        try:
            bets = json.load(file)
        except json.JSONDecodeError:
            bets = {}

    if reason not in bets:
        bets[reason] = {
            'author_id': author_id,
            'human_id': human_id,
            'bet': bet,
            'participants': {}
        }

        with open("data/bets.json", "w") as file:
            json.dump(bets, file, indent=4)


class Rating(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.t1 = time.time()
        self.last_mess_time = {}
        self.censored_words = ["женщина"]
        with open("data/data.json", "r") as f:
            self.rating = json.load(f)
        with open("data/data_messages.json", "r") as k:
            self.data_messages = json.load(k)
        with open('data/time_data.json', 'r') as f:
            self.data_time = json.load(f)
        self.channel = None
        self.t3 = {}  # Объявляем список как атрибут класса
        self.trigger = 0

    def reload_rate(self):
        del self.rating
        with open("data/data.json","r") as f:
            self.rating = json.load(f)
        return self.rating

    @commands.Cog.listener()
    async def on_ready(self):
        self.cha = self.bot.get_channel(922028793101680690)
        self.channel = self.bot.get_channel(1012106016332189747)

    @commands.Cog.listener()
    async def on_message(self, message):
        if message.author.bot:
            return

        bb = "<@" + str(message.author.id) + ">"
        self.data_messages[bb] += 1

        if bb in self.last_mess_time:
            last_mes_time = self.last_mess_time[bb]
            cur_time = time.time()
            time_dif = cur_time - last_mes_time

            if time_dif < 0.8:
                await message.channel.send("Не спамь!")
                await message.delete()
                channels_to_mute = [channel for channel in message.guild.channels if channel.type == disnake.ChannelType.text and channel.name not in ["правила", "for-tests"]]
                for channel in channels_to_mute:
                    await channel.set_permissions(message.author, send_messages=False, reason="Спам")

                await asyncio.sleep(60)

                for channel in channels_to_mute:
                    await channel.set_permissions(message.author, send_messages=True, reason="Конец мута")

        self.last_mess_time[bb] = time.time()

        for censored_word in self.censored_words:
            for x in message.content.lower().split():
                if x == censored_word:
                    await message.channel.send("Не говори так!")
                    break

        if self.data_messages[bb] % 50 == 0:
            self.rating[bb] += 3
            await message.reply(f"{bb}, поздравляю тебя, ты уже написал целых {self.data_messages[bb]} сообщения(й), за это я награжу тебя. Продолжай в том же духе!")
            await message.reply(f"{bb} получил +5 рейтинга за свою активность, истинный дегенерат!")
            if self.rating[bb] == 100:
                await message.reply(file=disnake.File("imgs/catwoman.jpg"))
            else:
                await message.reply(file=disnake.File("imgs/5soc.jpg"))

            with open('data/data.json', 'w') as f:
                json.dump(self.rating, f, indent=4)

        if message.content.lower() == "геншин импакт говно":
            if self.rating[bb] == 0:
                await message.reply("Поздравляю! ты получил +1 соц.рейтинг")
                self.rating[bb] += 1
                with open('data/data.json', 'w') as f:
                    json.dump(self.rating, f, indent=4)
            else:
                await message.reply("Не много тебе,чепуха?")

        with open('data/data_messages.json', 'w') as k:
            json.dump(self.data_messages, k, indent=4)

    @commands.slash_command()
    @commands.has_any_role(1089868546286289006)
    async def change_trigger(self,inter):
        if self.trigger == 1:
            self.trigger = 0
            await inter.send("Правило отмененно", ephemeral=True)
        else:
            self.trigger = 1
            await inter.send("Правило снова действует", ephemeral=True)

    @commands.slash_command(
        description="Показывает социальный рейтинг участников сервера."
    )
    async def rate(self, inter):
        self.reload_rate()
        rate_sort = {k : v for k, v in sorted(self.rating.items(), reverse=True, key=lambda item: item[1])}
        all_rate = ""
        for key in rate_sort:
            all_rate += " " + key + " - " + str(rate_sort[key]) + "\n"
        embed_rating = disnake.Embed(
            title="Вот рейтинг на сегодня:",
            description=all_rate,
            color=0xffcdd0
        )
        await inter.send(embed=embed_rating)

    @commands.slash_command(description="Узнай,сколько ты настрочил")
    async def mymessages(self, inter):
        bb = "<@" + str(inter.author.id) + ">"
        await inter.send(f"У тебя {self.data_messages[bb]} сообщени{scl(self.data_messages[bb])}")

    @commands.slash_command()
    async def mytime(self, inter):
        with open("data/time_data.json") as f:
            data_time = json.load(f)
        bb = int(data_time["<@" + str(inter.author.id) + ">"]//60)
        embed = disnake.Embed(color=disnake.Color.from_rgb(152,215,44))
        embed.add_field(name="Проведено в голосовых каналах:",value=f"```ansi\n[2;32m{bb} минут{scl(bb,1)}[0m\n```",inline=True)
        embed.add_field(name="До получения рейтинга осталось:", value=f"```ansi\n[2;35m{1440 - bb} минут{scl(1440 - bb,1)}[0m\n```",inline=True)

        await inter.send(embed=embed)

    @commands.slash_command(description="ход жопой")
    @commands.has_any_role(1089868546286289006, 910982734074249237)
    async def change_rate(self, inter, mention, number):
        social_plus = ['imgs/pudge.jpg', 'imgs/rf.jpg', 'imgs/social2.jpg', 'imgs/social_prima.jpg',
                       'imgs/social_valve.']
        social_minus = ['imgs/minus_social.png', 'imgs/minus_social2.jpg', 'imgs/social3.png', 'imgs/social4.png']
        embed_ret = disnake.Embed(
            title="изменение рейтинга",
            description=f'у {mention} рейтинг {self.rating[mention] + int(number)}',
            color=0xffffff
        )
        if int(number) >= 0:
            embed_ret.set_image(file=disnake.File(random.choice(social_plus)))
        elif int(number) < 0 and self.rating[mention] - int(number) < 0:
            embed_ret.set_image(file=disnake.File(random.choice(social_minus)))
        self.rating[mention] += int(number)

        with open('data/data.json', 'w') as f:
            json.dump(self.rating, f, indent=4)
        await inter.send(embed=embed_ret)
        self.reload_rate()

    @commands.slash_command()
    async def bet(self, inter, причина: str, ставка: int, человек: disnake.Member):
        reason = причина
        bet = ставка
        human = человек
        if bet > 5:
            view = BetView(author_id=inter.author.id, human_id=human.id, bet=bet, reason=reason)
            create_bet(inter.author.id,human.id,bet,reason)
            await inter.send(f"<@{inter.author.id}> поспорил с {human.mention} и поставил {bet} рейтинга на то, что {reason}", view=view)
        else:
            await inter.send(f"Ваша ставка должна быть больше 5 рейтинга")

    @commands.Cog.listener()
    async def on_voice_state_update(self, member, before, after):
        if member.mention == "<@724317992367685906>":
            if after.channel and after.channel.id == 1012106016332189747:
                await member.move_to(channel=None)

        if member.bot:
            return

        try:
            # Начало отсчета времени
            if before.channel is None and after.channel is not None:
                self.t1 = time.time()
                self.data_time[member.mention] = self.data_time.get(member.mention, 0)

            # Конец отсчета времени
            elif before.channel is not None and after.channel is None:
                t2 = time.time()
                if member.mention in self.t3 and self.t3[member.mention] is not None:
                    t2 = self.t3[member.mention]  # использовать время, когда пользователь вышел из мута
                self.data_time[member.mention] += t2 - self.t1
                if self.data_time[member.mention] >= 86400:
                    self.data_time[member.mention] -= 86400
                    self.rating[member.mention] += 7
                    await self.cha.send(f"{member.mention} получил 7 рейтинга. Трать дальше свою жизнь впустую!")

            # Пользователь замутился
            if after.self_deaf and after.channel:
                self.t3[member.mention] = time.time()

            # Пользователь размутился
            if before.self_deaf and not after.self_deaf:
                if member.mention in self.t3 and self.t3[member.mention] is not None:
                    self.t1 += time.time() - self.t3[member.mention]
                self.t3[member.mention] = None

            if before.self_deaf != after.self_deaf:
                self.reload_rate()

                await reward(member, self.rating, self.trigger)

            with open('data/time_data.json', 'w') as f:
                json.dump(self.data_time, f, indent=4)
            with open('data/data.json', 'w') as f:
                json.dump(self.rating, f, indent=4)

            self.reload_rate()
            await reward(member,self.rating,0)
        except KeyError:
            self.rating[f"<@{member.id}>"] = 0
            self.data_time[f"<@{member.id}>"] = 0
            self.data_messages[f"<@{member.id}>"] = 0
            with open('data/time_data.json', 'w') as f:
                json.dump(self.data_time, f, indent=4)
            with open('data/data.json', 'w') as f:
                json.dump(self.rating, f, indent=4)
            with open('data/data_messages.json', 'w') as f:
                json.dump(self.data_messages, f, indent=4)


async def reward(member,rating,trigger):
    gg = member.guild
    vip = gg.get_role(1240673696910278686)
    norm = gg.get_role(1253372831094407269)
    shitter = gg.get_role(1253372196592812124)
    if rating[f"<@{member.id}>"] >= 0:
        if norm not in member.roles:
            await member.add_roles(norm)
    else:
        if norm in member.roles:
            await member.remove_roles(norm)

    if rating[f"<@{member.id}>"] >= 100:
        if vip not in member.roles:
            await member.add_roles(vip)
    else:
        if vip in member.roles:
            await member.remove_roles(vip)

    if rating[f"<@{member.id}>"] < 0:
        if shitter not in member.roles:
            await member.add_roles(shitter)
        if rating[f"<@{member.id}>"] <= -100:
            await member.timeout(duration=86400)
            rating[f"<@{member.id}>"] += 10
    else:
        if shitter in member.roles:
            await member.remove_roles(shitter)

    if rating[f"<@{member.id}>"] <= 35 and trigger == 1:
        await member.move_to(channel=None)

with open("data/data_messages.json", 'r') as f:
    data_messages = f.read()

def scl(bb, c = 0):
    if bb % 10 == 1:
        return 'e' if c == 0 else "а"
    elif (bb % 10 >= 2) and (bb % 10 <= 4):
        return 'я' if c == 0 else "ы"
    elif (5 <= (bb % 10) <= 20) or bb % 10 == 0:
        return 'й' if c == 0 else ""


def setup(bot):
    bot.add_cog(Rating(bot))
