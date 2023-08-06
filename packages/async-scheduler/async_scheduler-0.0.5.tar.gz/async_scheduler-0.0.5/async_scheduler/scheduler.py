"""Планировщик"""

import asyncio
import typing
import logging
from asyncio import get_running_loop

from crontab import CronTab


log = logging.getLogger('scheduler')


class Job:
    """
    Задание
    """

    _cb = None  # # Функция которая будет выполнена по расписанию
    _async_cb = None  # # Короутина которая будет выполнена по расписанию
    _executor = None  # # Диспетчер (executor) для выполнения блокируезего кода
    _schedule_entry = None  # # Раписание
    _last_scheduled = None  # # Дата-время последнего запуска задачи
    _delay = None  # # Задержка выполнения в секундах
    _is_active = True
    _is_stopped = False
    _once = False
    _loop = None

    on_stopped = None

    def __init__(
            self, schedule_entry: str, loop=None, once=False,
            cb: typing.Callable = None, async_cb: typing.Callable = None, delay=0, executor=None
    ):
        self._schedule_entry = CronTab(schedule_entry)
        self._cb = cb
        self._async_cb = async_cb
        self._executor = executor

        self._loop = loop or get_running_loop()
        self._once = once
        self._delay = delay

    def _on_stopped(self):
        """
        Иницировать событие on_stopped
        """

        log.debug(f'_on_stopped() fired!')

        # Если событие on_stopped еще не происходило
        if not self._is_stopped:
            # Помечаем экземпляр как остановившийся
            # и что событие on_stopped уже произошло
            self._is_stopped = True

            # Если определен обработчик события, то вызываем этот обработчик
            log.debug(f'_on_stopped(): on_stopped={self.on_stopped}')
            if self.on_stopped:
                # Если обработчк - корутина, то создаем задачу
                if isinstance(self.on_stopped, typing.Coroutine):
                    log.debug(f'_on_stopped(): run on_stopped() as coroutine')
                    self._loop.create_task(self.on_stopped)

                # Если обработчк - функция, то вызываем ее
                if isinstance(self.on_stopped, typing.Callable):
                    log.debug(f'_on_stopped(): run on_stopped() as function')
                    self.on_stopped()

    async def run(self, is_first_run=True):
        """
        Запустить задание
        """

        log.debug(f'run() fired!')

        if not self._is_active:
            self._on_stopped()
            return

        if not is_first_run:
            log.debug(f'run() type(cb)={type(self._cb)}')
            if self._async_cb:
                log.debug(f'run() async_cb={self._async_cb} fired as coroutine')
                asyncio.create_task(self._async_cb())

            if self._cb:
                log.debug(f'run() cb={self._cb} fired as function')
                if self._executor:
                    self._loop.run_in_executor(self._executor, self._cb)
                else:
                    self._cb()

            if self._once:
                self._is_active = False
                return

        delay = self._schedule_entry.next(default_utc=False)
        log.debug(f'delay={delay}')
        if delay:
            await asyncio.sleep(delay + self._delay)
            asyncio.create_task(self.run(is_first_run=False))

    def stop(self):
        log.debug(f'stop() fired!')
        self._is_active = False

    @property
    def is_stopped(self):
        return self._is_stopped


class AsyncScheduler:
    """
    Планировщик
    """

    __state = {}  # # Общее состояние экземпляров класса
    _jobs = {}
    _stopped_jobs = []
    _loop = None

    def __init__(self, loop=None):
        # Создаем моностейт
        self.__dict__ = self.__state

        self._loop = loop or get_running_loop()

    def _on_job_stop_handler(self):
        """
        Обработчик события on_stopped
        Производит удаление уже остановившихся заданий
        """
        log.debug('Job stopped fired')
        new_stopped_jobs_list = []
        for idx in range(len(self._stopped_jobs)):
            if not self._stopped_jobs[idx].is_stopped:
                new_stopped_jobs_list.append(self._stopped_jobs[idx])
        self._stopped_jobs = new_stopped_jobs_list

    def delete_job(self, job_id):
        log.debug(f'delete_job() fired! job_id={job_id}')
        job = self._jobs.pop(job_id)

        # Перемещаем задание в отдельный список,
        # что бы дать ему возможность аккуратно завершиться...
        self._stopped_jobs.append(job)

        # ... и затем останавливаем его
        job.stop()

    async def create_and_run_job(
            self, job_id: str, schedule: str, cb: typing.Callable,
            delay=0, once: bool = False, executor=None
    ):
        """
        Создать и запустить задание
        """

        # Если задание уже существует....
        if job_id in self._jobs:
            # ...то сперва удаляем его
            self.delete_job(job_id)

        # Создаем новое задание
        self._jobs[job_id] = Job(
            schedule_entry=schedule, cb=cb, once=once, delay=delay, executor=executor)

        self._jobs[job_id].on_stopped = self._on_job_stop_handler

        # Запускаем новое заание
        self._loop.create_task(self._jobs[job_id].run())

    async def create_and_run_async_job(
            self, job_id: str, schedule: str, cb: typing.Callable,
            delay=0, once: bool = False
    ):
        """
        Создать и запустить асинхронное задание
        """

        # Если задание уже существует....
        if job_id in self._jobs:
            # ...то сперва удаляем его
            self.delete_job(job_id)

        # Создаем новое задание
        self._jobs[job_id] = Job(schedule_entry=schedule, async_cb=cb, once=once, delay=delay)

        self._jobs[job_id].on_stopped = self._on_job_stop_handler

        # Запускаем новое заание
        self._loop.create_task(self._jobs[job_id].run())
