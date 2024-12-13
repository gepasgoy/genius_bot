import aiohttp
import asyncio
from disnake.ext import commands
import socket
import threading
from fake_useragent import UserAgent

class serv(commands.Cog):
    def __init__(self, bot, url):
        self.bot = bot
        self.url = url
        self.user_agent = UserAgent()

    @commands.Cog.listener()
    async def on_ready(self):
        print("hii")
        # Запуск асинхронной задачи для отправки запросов
        asyncio.create_task(self.send_request_periodically())

    async def send_request_periodically(self):
        """
        Асинхронная функция для отправки запроса каждые 20 минут.
        """
        while True:
            try:
                headers = {"User-Agent": self.user_agent.random}
                async with aiohttp.ClientSession(headers=headers) as session:
                    async with session.get(self.url) as response:
                        if response.status == 200:
                            print(f"Успешный запрос! Ответ: {await response.text()}")
                        else:
                            print(f"Ошибка: {response.status}")
            except Exception as e:
                print(f"Произошла ошибка: {e}")

            # Ждём 20 минут (20 * 60 секунд)
            await asyncio.sleep(20 * 60)

def start_server():
    # Создаем сокет
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # Указываем IP-адрес и порт для прослушивания (в данном случае 8080)
    host = '0.0.0.0'
    port = 8080

    # Связываем сокет с адресом и портом
    server_socket.bind((host, port))

    # Запускаем прослушивание
    server_socket.listen(5)
    print(f"Сервер запущен и прослушивает порт {port}...")

    while True:
        # Ожидаем подключения
        client_socket, address = server_socket.accept()
        print(f"Подключение от {address}")

        # Получаем данные от клиента
        data = client_socket.recv(1024).decode()
        print(f"Данные от клиента: {data}")

        # Отправляем ответ клиенту
        response = "HTTP/1.1 200 OK\n\nПривет, клиент!"
        client_socket.send(response.encode())

        # Закрываем соединение с клиентом
        client_socket.close()

# Функция для запуска сервера в отдельном потоке
def run_server_in_thread():
    server_thread = threading.Thread(target=start_server)
    server_thread.daemon = True  # Устанавливаем поток как "демон"
    server_thread.start()
    print("Сервер работает в фоновом потоке.")

# Основная программа продолжает работать
print("Основной поток продолжает выполняться...")

def setup(bot):
    url = "https://geniusbot-cbwuqmiv.b4a.run/"
    bot.add_cog(serv(bot, url))
    run_server_in_thread()
