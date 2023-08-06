"""Демонстранционное приложение"""

import asyncio
from concurrent.futures import ThreadPoolExecutor
import logging

from async_scheduler import AsyncScheduler


def my_handler():
    print('my_handler fired!')


async def my_async_once_handler():
    print('my_async_once_handler fired!')
    await asyncio.sleep(.1)


async def my_async_handler():
    print('my_async_handler fired!')
    await asyncio.sleep(.1)


async def my_async_handler_with_delay():
    print('my_async_handler_with_delay fired!')
    await asyncio.sleep(.1)


async def main(async_loop):
    print('Starting.... ', end='')
    s = AsyncScheduler()

    # Создаем задание с расписанием запуска каждые пять секунд
    # Для большей инсформации см. https://github.com/josiahcarlson/parse-crontab
    await s.create_and_run_job('my_handler', '*/5 * * * * * *', my_handler, executor=th_executor)

    # Создаем асинхронное одноразовое задание, которое должно быть выполнено через 7 секунд
    await s.create_and_run_async_job(
        'my_async_once_handler', '*/7 * * * * * *', my_async_once_handler, once=True)

    # Создаем асинхронное задание, которое должно быть выполнено каждые 3 секунды
    await s.create_and_run_async_job('my_async_handler', '*/3 * * * * * *', my_async_handler)

    # Создаем асинхронное задание, которое должно быть выполнено каждые 3 секунды
    # c задержкой в 1 секунду
    await s.create_and_run_async_job(
        'my_async_handler_with_delay', '*/3 * * * * * *', my_async_handler_with_delay, delay=1)

    print('done.')
    await asyncio.sleep(30)

    print('Stopping.... ', end='')
    s.delete_job('my_handler')
    s.delete_job('my_async_handler')
    print('done.')

    # Ждем 5 секунд для аккуратного завершения задания и очистки памяти.
    # Хотя в демонстрационном приложении, этого, в принципе, можно и не делать
    await asyncio.sleep(5)

    async_loop.stop()

if __name__ == '__main__':
    logging.basicConfig(level=logging.DEBUG)

    th_executor = ThreadPoolExecutor(max_workers=3)

    loop = asyncio.get_event_loop()
    loop.create_task(main(loop))
    loop.run_forever()
