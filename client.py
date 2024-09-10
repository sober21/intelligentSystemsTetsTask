import asyncio
import datetime
import random
import logging

from log_file_name import get_unique_filename


class Client:
    id_client = 0

    @classmethod
    def set_id_client(cls):
        cls.id_client += 1

    def __init__(self):
        self.keepalive_message = ""
        self.logger = None
        self.logfile_name = ""
        self.file_handler = None
        self.formatter = None
        self.reader = None
        self.writer = None
        self.request_num = 0
        self.set_id_client()
        self.id_client = Client.id_client
        self.logging_setup()

    # Настройка логирования
    def logging_setup(self):
        # Привязываем к экземпляру класса экземпляр getLogger'а
        self.logger = logging.getLogger(__name__ + '.Client' + str(self.id_client))
        self.logger.setLevel(logging.INFO)
        # Меняем название логфайла, если такой уже есть.
        self.logfile_name = get_unique_filename("client_1.log")
        self.file_handler = logging.FileHandler(self.logfile_name, mode="a")
        self.file_handler.setLevel(logging.INFO)
        self.formatter = logging.Formatter('%(message)s')
        self.file_handler.setFormatter(self.formatter)
        self.logger.addHandler(self.file_handler)

    # Получение сообщения "keepalive"
    async def receipt_keepalive(self, timeout):
        try:
            response = await asyncio.wait_for(self.reader.readuntil(), timeout)
            time_received = datetime.datetime.now().strftime('%H:%M:%S.%f')[:-3]
            cur_date = datetime.datetime.now().strftime('%Y-%m-%d')
            response = response.decode().strip()

        except asyncio.TimeoutError:
            pass
        else:
            self.write_log(cur_date=cur_date, time_received=time_received, response=response)

    @staticmethod
    async def async_sleep(time_sleep):
        await asyncio.sleep(time_sleep)

    async def random_sleep(self):
        time_sleep = random.uniform(0.3, 3.0)
        await asyncio.gather(self.async_sleep(time_sleep), self.receipt_keepalive(time_sleep))

    async def send_requests(self, reader, writer):
        while True:
            # Случайная задержка
            await self.random_sleep()
            message = f"[{self.request_num}] PING\n"
            time_send = datetime.datetime.now().strftime('%H:%M:%S.%f')[:-3]
            cur_date = datetime.datetime.now().strftime('%Y-%m-%d')
            self.request_num += 1
            writer.write(message.encode())
            message = message.strip()

            try:
                response = await asyncio.wait_for(self.reader.readuntil(), 1.9)
                time_received = datetime.datetime.now().strftime('%H:%M:%S.%f')[:-3]
                response = response.decode().strip()

                if "keepalive" in response:
                    self.write_log(cur_date=cur_date, time_received=time_received, response=response)
                    response = await asyncio.wait_for(self.reader.readuntil(), 1.5)
                    time_received = datetime.datetime.now().strftime('%H:%M:%S.%f')[:-3]
                    response = response.decode().strip()

                self.write_log(cur_date=cur_date, time_send=time_send, message=message, time_received=time_received,
                               response=response)

            except asyncio.TimeoutError:
                response = "(таймаут)"
                time_received = datetime.datetime.now().strftime('%H:%M:%S.%f')[:-3]
                self.write_log(cur_date=cur_date, time_send=time_send, message=message, time_received=time_received,
                               response=response)

    # Запись логов
    def write_log(self, cur_date, time_send="", message="", time_received="", response=""):
        self.logger.info(f"{cur_date};\n"
                         f"{time_send};\n"
                         f"{message};\n"
                         f"{time_received};\n"
                         f"{response}.\n\n")

    async def main(self):
        reader, writer = await asyncio.open_connection('127.0.0.1', 8000)
        self.reader = reader
        self.writer = writer
        await self.send_requests(reader, writer)


if __name__ == '__main__':
    client1 = Client()
    client2 = Client()


    async def run_clients():
        await asyncio.gather(client1.main(), client2.main())


    asyncio.run(run_clients())
