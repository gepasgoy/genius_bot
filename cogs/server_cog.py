from disnake.ext import commands
import socket
import threading


class serv(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        print("hii")



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
    bot.add_cog(serv(bot))
    run_server_in_thread()