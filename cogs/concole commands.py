import subprocess
import disnake
from disnake.ext import commands
import threading
import asyncio
import json
from time import sleep
from os import path


class Console(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.stop_event = threading.Event()
        console_thread = threading.Thread(target=self.run_console_comm, daemon=True)
        console_thread.start()

    async def kick_all_from_voice(self):
        for guild in self.bot.guilds:
            for channel in guild.voice_channels:
                for member in channel.members:
                    await member.move_to(None)
        print("Все пользователи кикнуты из голосовых каналов.")

    async def console_comm(self):
        sleep(5.5)
        while not self.stop_event.is_set():
            print("Введите команду: ", end='')
            botchan = self.bot.get_channel(1216378623301521468)
            testchan = self.bot.get_channel(1217847449205346334)
            channel = self.bot.get_channel(922028793101680690) #всяко-говно
            command = str(input())
            if command == "stop":
                print("Остановка бота...")
                botchan = self.bot.get_channel(1216378623301521468)
                self.stop_event.set()
                asyncio.run_coroutine_threadsafe(botchan.send(f"Выключение бота через 15 секунд"), self.bot.loop)
                await asyncio.sleep(15)
                asyncio.run_coroutine_threadsafe(self.kick_all_from_voice(), self.bot.loop)
                await asyncio.sleep(3)
                asyncio.run_coroutine_threadsafe(self.bot.close(), self.bot.loop)
                print("Бот успешно остановлен!")

            elif command == "servers":
                jj = []
                for guild in self.bot.guilds:
                    jj.append(guild.name)
                print(f"Количество серверов: {len(jj)}, сервера: {jj}")

            elif command == "exit":
                print("Консоль закрыта")
                break

            elif command == "restart":
                asyncio.run_coroutine_threadsafe(self.bot.close(), self.bot.loop)
                subprocess.run(["python", "bot.py"])

            elif command.startswith("send_do"):
                message = command[8:]
                asyncio.run_coroutine_threadsafe(channel.send(message), self.bot.loop)

            elif command.startswith("send_in"):
                bb = command.split(" ")
                channel = self.bot.get_channel(int(bb[1]))
                asyncio.run_coroutine_threadsafe(channel.send(" ".join(bb[2:])), self.bot.loop)

            elif command.startswith("add"):
                bb = command.split(" ")

                if not bb[-1].isdigit():
                    bb.append("0")

                if bb[-3] == "in":
                    if path.isfile(f"{bb[-2]}"):
                        with open(f"data/{bb[-2]}.json") as f:
                            boba = json.load(f)
                        boba[bb[1]] = bb[-1]
                    else:
                        print("нет такого файла")
                else:
                    with open("data/data.json", "r") as f:
                        self.rating = json.load(f)
                    with open("data/data_messages.json", "r") as k:
                        self.data_messages = json.load(k)
                    with open('data/time_data.json', 'r') as f:
                        self.data_time = json.load(f)
                    self.rating[f"<@{bb[1]}>"] = 0
                    self.data_time[f"<@{bb[1]}>"] = [0, 0]
                    self.data_messages[f"<@{bb[1]}>"] = 0
                    with open('data/time_data.json', 'w') as f:
                        json.dump(self.data_time, f, indent=4)
                    with open('data/data.json', 'w') as f:
                        json.dump(self.rating, f, indent=4)
                    with open('data/data_messages.json', 'w') as f:
                        json.dump(self.data_messages, f, indent=4)

            elif command.startswith("aboba"):
                bb = command.split(" ")
                with open(f"data/{bb[1:]}.json", "r") as f:
                    boba = json.load(f)

                for guild in self.bot.guilds:
                    for man in guild.members:
                        if man.bot:
                            continue
                        boba[f"<@{man.id}>"] = 0

                with open(f"data/{bb[1:]}","w") as f:
                    json.dump(boba, f, indent=4)

            elif command.startswith("endbet"):
                with open("data/bets.json", "r") as file:
                    bets = json.load(file)
                with open("data/data.json", "r") as f:
                    rate = json.load(f)
                reason = " ".join(command.split()[1:-1])
                print(reason)
                num = command.split()[-1]
                try:
                    bet = bets[reason]["bet"]
                    len_a = len([x for x in bets[reason]["participants"].values() if x == "author"])
                    len_h = len([x for x in bets[reason]["participants"].values() if x == "human"])
                    budget_a = len_a * bet
                    budget_h = len_h * bet
                    winners = []
                    if int(num) == 1:
                        bb = bets[reason]["author_id"]
                        for x in bets[reason]["participants"]:
                            if bets[reason]["participants"][x] == "author":
                                rate[f"<@{int(x)}>"] += budget_h / len_a
                                winners.append(f"<@{x}>")
                            else:
                                rate[f"<@{int(x)}>"] -= bet
                        gg = "\n".join(winners)
                        rate[f"<@{bb}>"] += bet
                        rate[f"<@{bets[reason]['human_id']}>"] -= bet
                        with open("data/data.json", "w") as f:
                            json.dump(rate, f, indent=4)
                        asyncio.run_coroutine_threadsafe(botchan.send(f"Спор по поводу {reason} закончился победой <@{bb}>"), self.bot.loop)
                        asyncio.run_coroutine_threadsafe(botchan.send(embed=disnake.Embed(title="Победители:", description=gg)), self.bot.loop)
                    elif int(num) == 2:
                        bb = bets[reason]["human_id"]
                        for x in bets[reason]["participants"]:
                            if bets[reason]["participants"][x] == "human":
                                rate[f"<@{int(x)}>"] += budget_a / len_h
                                winners.append(f"<@{x}>")
                            else:
                                rate[f"<@{int(x)}>"] -= bet
                        gg = "\n".join(winners)
                        rate[f"<@{bb}>"] += bet
                        rate[f"<@{bets[reason]['author_id']}>"] -= bet
                        with open("data/data.json", "w") as f:
                            json.dump(rate, f, indent=4)
                        asyncio.run_coroutine_threadsafe(botchan.send(f"Спор по поводу {reason} закончился победой <@{bb}>"), self.bot.loop)
                        asyncio.run_coroutine_threadsafe(botchan.send(embed=disnake.Embed(title="Победители:", description=gg)), self.bot.loop)
                    elif int(num) == 0:
                        asyncio.run_coroutine_threadsafe(botchan.send(f"Спор по поводу {reason} закончился ничьей или был завершён по другой причине."), self.bot.loop)
                    bets.pop(reason)
                    with open("data/bets.json", "w") as f:
                        json.dump(bets, f, indent=4)
                except KeyError:
                    if reason not in bets:
                        print("Нет такого спора.")

            else:
                print(f"Неизвестная команда")

    def run_console_comm(self):
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        loop.run_until_complete(self.console_comm())


def setup(bot):
    bot.add_cog(Console(bot))