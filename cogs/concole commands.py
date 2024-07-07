import disnake
from disnake.ext import commands
import threading
import asyncio
import json
from time import sleep


class Console(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.stop_event = threading.Event()
        console_thread = threading.Thread(target=self.run_console_comm, daemon=True)
        console_thread.start()

    async def console_comm(self):
        sleep(3.8)
        while not self.stop_event.is_set():
            print("Введите команду: ", end='')
            botchan = self.bot.get_channel(1216378623301521468)
            testchan = self.bot.get_channel(1217847449205346334)
            channel = self.bot.get_channel(922028793101680690) #всяко-говно
            command = str(input())
            if command == "stop":
                print("Остановка бота...")
                self.stop_event.set()
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
            elif command.startswith("send_do"):
                message = command[8:]
                asyncio.run_coroutine_threadsafe(channel.send(message), self.bot.loop)
            elif command.startswith("send_in"):
                bb = command.split(" ")
                channel = self.bot.get_channel(int(bb[1]))
                asyncio.run_coroutine_threadsafe(channel.send(" ".join(bb[2:])), self.bot.loop)
            elif command.startswith("endbet"):
                with open("data/bets.json", "r") as file:
                    bets = json.load(file)
                with open("data/data.json", "r") as f:
                    rate = json.load(f)
                reason = command.split()[1]
                num = command.split()[2]
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