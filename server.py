import asyncio
import logging
import random
import datetime
import time

# Настройка логирования
logging.basicConfig(filename='server.log', level=logging.INFO, format='%(message)s')


class EchoServerProtocol(asyncio.Protocol):
    client_id = 0
    clients = {}
    response_num = 0

    def __init__(self):
        self.keepalive_task = None
        self.transport = None

    def connection_made(self, transport):
        self.transport = transport
        EchoServerProtocol.client_id += 1
        EchoServerProtocol.clients[transport] = EchoServerProtocol.client_id

        if len(self.clients) == 1:
            # Запускаем задачу для отправки keepalive каждый 5 секунд
            self.keepalive_task = asyncio.create_task(self.send_keepalive())

    def connection_lost(self, exc):
        del EchoServerProtocol.clients[self.transport]

    async def send_keepalive(self):
        while EchoServerProtocol.clients:
            await asyncio.sleep(5)
            keepalive_message = f"[{EchoServerProtocol.response_num}] keepalive\n"
            for transport in EchoServerProtocol.clients:
                transport.write(keepalive_message.encode())
            self.set_response_num()

    def data_received(self, data):
        time_of_receipt_of_request = datetime.datetime.now().strftime('%H:%M:%S.%f')[:-3]
        cur_date = datetime.datetime.now().strftime('%Y-%m-%d')
        message = data.decode().strip()
        request_num = int(message.split()[0][1:-1])

        # Игнорирование 10% сообщений
        if random.random() < 0.1:
            response_message = f"(проигнорировано)"
            time_of_receipt_of_answer = "(проигнорировано)"


        else:
            time.sleep(random.uniform(0.1, 1.0))  # Случайная задержка
            time_of_receipt_of_answer = datetime.datetime.now().strftime('%H:%M:%S.%f')[:-3]
            response_message = f"[{EchoServerProtocol.response_num}/{request_num}] PONG ({self.clients[self.transport]})\n"
            self.transport.write(response_message.encode())
            self.set_response_num()

        # Запись в лог
        logging.info(f"{cur_date};\n"
                     f"{time_of_receipt_of_request};\n"
                     f"{message};\n"
                     f"{time_of_receipt_of_answer};\n"
                     f"{response_message.strip()};\n\n")

    @classmethod
    def set_client_id(cls):
        cls.client_id += 1

    @classmethod
    def set_response_num(cls):
        cls.response_num += 1


async def main():
    loop = asyncio.get_running_loop()
    server = await loop.create_server(lambda: EchoServerProtocol(), '127.0.0.1', 8000)
    try:
        # Даём серверу 5 минут
        await asyncio.sleep(300)
    finally:
        server.close()
        await server.wait_closed()


if __name__ == '__main__':
    asyncio.run(main())
