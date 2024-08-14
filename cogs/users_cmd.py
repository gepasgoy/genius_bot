import disnake
from disnake.ext import commands
from random import randint
import json


class CMDUsers(commands.Cog):

    def __init__(self, bot):
        self.bot = bot
        self.help_embed = disnake.Embed(
            title="Лист команд:",
            color=229281
        )
        self.help_rating_embed = disnake.Embed(
            title="Как устроена система рейтинга:",
            description=f"На сервере присутствует <@1217538387007901857>, который регулирует твой социальный рейтинг. Это, можно сказать, валюта-показатель, которая показывает твой статус на сервере. "
                        f"Рейтинг можно получать разными способами:Активность, ставки, коды, помощь серверу."
                        f"```ansi\n[2;31m[0m[2;31mАдминистратор и модераторы могут управлять чужим рейтингом и имеют полное право понизить его если участник сервера провинился.[0m\n"
                        f"```\n**За рейтинг полагаются роли:**"
        )
        with open("data/data.json", "r") as f:
            self.rating = json.load(f)
        with open("data/data_messages.json", "r") as k:
            self.data_messages = json.load(k)
        with open('data/time_data.json', 'r') as f:
            self.data_time = json.load(f)

    @commands.Cog.listener()
    async def on_ready(self):
        print(f"Bot {self.bot.user} is ready to work!")
        await self.bot.change_presence(activity=disnake.Game("Nothing"))

    @commands.Cog.listener()
    async def on_button_click(self,inter: disnake.MessageInteraction):
        if inter.component.custom_id == 'button1':
            await inter.send(embed=self.help_embed)
        elif inter.component.custom_id == "button":
            await inter.response.edit_message(embed=self.help_rating_embed, view=None)

    @commands.Cog.listener()
    async def on_member_join(self,member):
        normis = member.guild.get_role(1253372831094407269)
        await member.add_roles(normis)
        boba = await self.bot.fetch_user(member.id)
        button1 = disnake.ui.Button(label="Ознакомиться", style=disnake.ButtonStyle.success, custom_id="button1")
        action_row = disnake.ui.ActionRow(button1)
        embed = disnake.Embed(
            title="Добро пожаловать на сервер!",
            description=f"Если ты играешь в доту, то тебе нужно ознакомится с командой `/buff` на нашем сервере.\nСоветую использовать `/commands`."
        )
        embed.set_author(
            name="Деград-отряд",
            icon_url="https://cdn.discordapp.com/icons/898250287221997598/ee7b2bbb5f9418c11cc1ecd25ae0b596.webp?size=128"
        )
        await boba.send(embed=embed, components=action_row)
        if member.bot:
            return
        self.rating[f"<@{member.id}>"] = 0
        self.data_time[f"<@{member.id}>"] = 0
        self.data_messages[f"<@{member.id}>"] = 0
        with open('data/time_data.json', 'w') as f:
            json.dump(self.data_time, f, indent=4)
        with open('data/data.json', 'w') as f:
            json.dump(self.rating, f, indent=4)
        with open('data/data_messages.json', 'w') as f:
            json.dump(self.data_messages, f, indent=4)

    @commands.Cog.listener()
    async def on_member_remove(self,member):
        if member.bot:
            return
        try:
            self.rating.pop(f"<@{member.id}>")
            self.data_time.pop(f"<@{member.id}>")
            self.data_messages.pop(f"<@{member.id}>")
        except:
            print("Нет такого человека в базе данных.")
        with open('data/time_data.json', 'w') as f:
            json.dump(self.data_time, f, indent=4)
        with open('data/data.json', 'w') as f:
            json.dump(self.rating, f, indent=4)
        with open('data/data_messages.json', 'w') as f:
            json.dump(self.data_messages, f, indent=4)

    @commands.command()
    async def profile(self, ctx):
        bb = randint(0, 2)
        if bb == 1:
            await ctx.reply("Hiii:3")
        else:
            await ctx.reply("Иди нахуй, сука")

    @commands.slash_command(description="Очистить последние n сообщений")
    @commands.has_any_role(1089868546286289006,910982734074249237)
    async def clear(self, inter, n: int, bot_only: bool = False):
        await inter.response.defer(ephemeral=True)

        # Получаем последние n сообщений в канале
        messages = await inter.channel.history(limit=n).flatten()

        if bot_only:
            # Фильтруем только сообщения бота
            messages = [msg for msg in messages if msg.author == self.bot.user]

        # Удаляем сообщения
        if messages:
            await inter.channel.delete_messages(messages)
            await inter.send(f"Удалено {len(messages)} сообщений.")
        else:
            await inter.send("Нет сообщений для удаления.")

    @commands.slash_command(description="Лист команд")
    async def commands(self,inter):
        self.help_embed.add_field("`/rate`", "Эта команда позволяет узнать нынешний рейтинг всех участников сервера")
        self.help_embed.add_field("`/mymessages`", "Количество написанных тобой сообщений")
        self.help_embed.add_field("`/myid`", "Заносит твой id стима или доты в базу данных, чтобы ты мог пользоваться командой `/buff`")
        self.help_embed.add_field("`/buff`", "Эта команда берёт статистику твоего аккаунта в доте с сайта DOTABUFF")
        self.help_embed.add_field("`!profile`", "Местный аналог монеточки")
        self.help_embed.add_field("`/itembuild`", f"```ansi\n[2;31mвременно не работает[0m\n```")
        self.help_embed.add_field("`/bet`", "Позволяет ставить рейтинг на какие-нибудь ситуации. В этих спорах также могут принять участие и другие люди. **Чтобы завершить спор, вам нужно обратиться к <@495953464128569366>.**")
        self.help_rating_embed.add_field("`Нормис`", "Эта роль есть у каждого,кто имеет положительный рейтинг.\n```ansi\n[2;34m[0;34m[0;45mПо правам - обычный пользователь дискорда, за исключением того, что полностью мутится можно только с 35 рейтинга.[0m[0;34m[0m[2;34m[0m[2;40m[0m[2;41m[0m\n```")
        self.help_rating_embed.add_field("`Опущеннец`", "Эту роль имеют люди с отрицательным рейтингом.\n```ansi\n[2;40mПо правам - пользователь с немного урезанными правами.Если рейтинг пользователя опустится ниже -100, то он отправится в тайм-аут[0m[2;40m[0m[2;41m[0m\n```")
        self.help_rating_embed.add_field("`Почётный`", f"Эту роль имеют только самые почётные дегенераты на сервере.\n```ansi\n[2;41mЛюди с этой ролью обладают расширенными правами.Роль достигается со 100 рейтинга.[0m[2;40m[0m[2;41m[0m\n```")

        button = disnake.ui.Button(label="Система рейтинга ➡️", style=disnake.ButtonStyle.blurple, custom_id="button")
        action_row = disnake.ui.ActionRow(button)
        await inter.send(embed=self.help_embed,components=action_row,ephemeral=True)


def setup(bot):
    bot.add_cog(CMDUsers(bot))
