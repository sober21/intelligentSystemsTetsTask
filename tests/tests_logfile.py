"""Проверяется, что лог-файлы соответствуют заданному формату"""
from fileinput import filename

"""Проверяется процент проигнорированных сообщений"""
"""Проверятеся, что количество проигнорированных сообщений в лог-файле сервера равно количеству сообщений без ответа
в лог-файлах клиентов"""
import re
import os


def test_server_logfile(logfile: str) -> None:
    with open(logfile, encoding="utf-8", mode="r") as file:
        log = file.read()
        list_log_chunk = log.strip().split("\n\n\n")
        pattern = (
            r'\d\d\d\d-\d\d-\d\d;\s\d\d:\d\d:\d\d\.\d\d\d;\s\[\d+\] PING;\s\d\d:\d\d:\d\d\.\d\d\d;\s\[\d+/\d+\] PONG \(\d+\);|'
            r'\d\d\d\d-\d\d-\d\d;\s\d\d:\d\d:\d\d\.\d\d\d;\s\[\d+\] PING;\s\(проигнорировано\);\s\(проигнорировано\);')
        for chunk in list_log_chunk:
            if re.fullmatch(pattern, chunk):
                continue
            else:
                print(chunk)
                break
        else:
            print("Лог-файл сервера соответствует формату.")
    return None


def test_client_logfile(logfile: str) -> None:
    with open(logfile, encoding="utf-8", mode="r") as file:
        log = file.read()
        list_log_chunk = log.strip().split("\n\n\n")
        pattern = (
            r'\d\d\d\d-\d\d-\d\d;\s\d\d:\d\d:\d\d\.\d\d\d;\s\[\d+\] PING;\s\d\d:\d\d:\d\d\.\d\d\d;\s\[\d+/\d+\] PONG \(\d+\);|'
            r'\d\d\d\d-\d\d-\d\d;\s\d\d:\d\d:\d\d\.\d\d\d;\s\[\d+\] PING;\s\d\d:\d\d:\d\d\.\d\d\d;\s\(таймаут\);|'
            r'\d\d\d\d-\d\d-\d\d;\s;\s;\s\d\d:\d\d:\d\d\.\d\d\d;\s\[\d+\] keepalive;')
        for chunk in list_log_chunk:
            if re.fullmatch(pattern, chunk):
                continue
            else:
                print(chunk)
                break
        else:
            print("Лог-файл клиента соответствует формату.")
    return None


def test_percent_ignor_message(logfile) -> tuple[int, int]:
    """Считает процент и количество игнорированных сообщений в лог-файле сервера и возвращает результат"""
    with open(logfile, encoding="utf-8", mode="r") as file:
        log = file.read()
        list_log_chunk = log.strip().split("\n\n\n")
        pattern = (
            r'\d\d\d\d-\d\d-\d\d;\s\d\d:\d\d:\d\d\.\d\d\d;\s\[\d+\] PING;\s\(проигнорировано\);\s\(проигнорировано\);')
        count_ignor_message = 0
        for chunk in list_log_chunk:
            if re.fullmatch(pattern, chunk):
                count_ignor_message += 1
        percent = round(len(list_log_chunk) / count_ignor_message, 1)
    return percent, count_ignor_message


def test_timeout_message_client(logfile) -> int:
    """Считает количество сообщений на которые не было ответа(был таймаут) в лог-файле клиента и возвращает результат"""
    with open(logfile, encoding="utf-8", mode="r") as file:
        log = file.read()
        list_log_chunk = log.strip().split("\n\n\n")
        pattern = (
            r'\d\d\d\d-\d\d-\d\d;\s\d\d:\d\d:\d\d\.\d\d\d;\s\[\d+\] PING;\s\d\d:\d\d:\d\d\.\d\d\d;\s\(таймаут\);')
        count_timeout_message = 0
        for chunk in list_log_chunk:
            if re.fullmatch(pattern, chunk):
                count_timeout_message += 1
    return count_timeout_message


if __name__ == '__main__':
    abspath = os.path.abspath(__file__)
    # Если вы на Windows, то прямой слэш "/" надо заменить на обратный "\"
    abspath = '/'.join(abspath.split('/')[:-2])


    test_client_logfile(abspath + "/client_1.log")
    test_client_logfile(abspath + "/client_2.log")
    test_server_logfile(abspath + "/server.log")

    count_ignor_message = test_percent_ignor_message(abspath + "/server.log")
    count_timeout_message_1 = test_timeout_message_client(abspath + "/client_1.log")
    count_timeout_message_2 = test_timeout_message_client(abspath + "/client_2.log")
    print(f"Процент игнорированных сообщений равен {count_ignor_message[0]}%")
    if count_ignor_message[1] == count_timeout_message_1 + count_timeout_message_2:
        print("Количество игнорированных сообщений в лог-файле сервера соответствует сумме сообщений без ответа "
              "в лог-файлах клиентов.")
