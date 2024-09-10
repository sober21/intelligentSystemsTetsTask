"""Проверяется, что лог-файлы соответствуют заданному формату"""
"""Проверяется процент проигнорированных сообщений"""
import re


def test_server_logfile(logfile: str) -> None:
    with open(logfile, encoding="utf-8", mode="r") as file:
        log = file.read()
        list_log_chunk = log.strip().split("\n\n\n")
        pattern = (
            '\d\d\d\d-\d\d-\d\d;\s\d\d:\d\d:\d\d\.\d\d\d;\s\[\d+\] PING;\s\d\d:\d\d:\d\d\.\d\d\d;\s\[\d+/\d+\] PONG \(\d+\)\.|'
            '\d\d\d\d-\d\d-\d\d;\s\d\d:\d\d:\d\d\.\d\d\d;\s\[\d+\] PING;\s\(проигнорировано\);\s\(проигнорировано\)\.')
        for chunk in list_log_chunk:
            if re.fullmatch(pattern, chunk):
                continue
            else:
                print(chunk)
                break
        else:
            print("Тест лог-файла сервера успешно завершён")
    return None


def test_client_logfile(logfile: str) -> None:
    with open(logfile, encoding="utf-8", mode="r") as file:
        log = file.read()
        list_log_chunk = log.strip().split("\n\n\n")
        pattern = (
            '\d\d\d\d-\d\d-\d\d;\s\d\d:\d\d:\d\d\.\d\d\d;\s\[\d+\] PING;\s\d\d:\d\d:\d\d\.\d\d\d;\s\[\d+/\d+\] PONG \(\d+\)\.|'
            '\d\d\d\d-\d\d-\d\d;\s\d\d:\d\d:\d\d\.\d\d\d;\s\[\d+\] PING;\s\d\d:\d\d:\d\d\.\d\d\d;\s\(таймаут\)\.|'
            '\d\d\d\d-\d\d-\d\d;\s;\s;\s\d\d:\d\d:\d\d\.\d\d\d;\s\[\d+\] keepalive\.')
        for chunk in list_log_chunk:
            if re.fullmatch(pattern, chunk):
                continue
            else:
                print(chunk)
                break
        else:
            print("Тест лог-файла клиента успешно завершён")
    return None


def test_10_percent_ignor(logfile):
    with open(logfile, encoding="utf-8", mode="r") as file:
        log = file.read()
        list_log_chunk = log.strip().split("\n\n\n")
        pattern = (
            '\d\d\d\d-\d\d-\d\d;\s\d\d:\d\d:\d\d\.\d\d\d;\s\[\d+\] PING;\s\(проигнорировано\);\s\(проигнорировано\)\.')
        count_ignor_chunk = 0
        for chunk in list_log_chunk:
            if re.fullmatch(pattern, chunk):
                count_ignor_chunk += 1

        print(f"Процент проигнорированных сообщений: {round(len(list_log_chunk) / count_ignor_chunk, 1)}%")
    return None


if __name__ == '__main__':
    test_client_logfile("путь_к_файлу/client_1.log")
    test_client_logfile("путь_к_файлу/client_2.log")
    test_server_logfile("путь_к_файлу/server.log")
    test_10_percent_ignor("путь_к_файлу/server.log")
