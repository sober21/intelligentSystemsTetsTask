Тестовое задание от "Интеллектуальные системы"



Что сделано?

1. Использовались Python 3.10 и asyncio.
2. Сервер слушает TCP порт. 2 клиента в разных процессах.
3. Интервалы соблюдены. Формат сообщений, формат логов тоже.
4. "keepalive" отправляются каждые 5 секунд.
5. 10% запросов игнорируются сервером.
6. Сервер был запущен на 5 минут.
7. Есть тесты.


Что не так?

1. Возможно в server.py в строке 52 нужно было использовать асинхронную функция sleep().
   Я не стал этого делать, потому что функция data_received не асинхронная.
2. Не уложился в недельный срок.


Уточнение: в логах сервера не записаны сообщения keepalive
(логично было бы их записать, чтобы следить за номерами ответов от сервера),
потому что это не указано в ТЗ.


Что можно улучить?

1. Я бы убрал настройку логирования из класса Client и перенёс 
бы эту логику в отдельный модуль.
2. Корявая реализация перехвата сообщения "keepalive". Возможны неправильные 
логи.