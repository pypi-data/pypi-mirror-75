'''Высокоуровневый API для доступа к Битрикс24'''

import urllib.parse
import asyncio
import aiohttp
import time
import itertools
import more_itertools

from tqdm import tqdm

import fast_bitrix24.correct_asyncio

BITRIX_URI_MAX_LEN = 5820

##########################################
#
#   SemaphoreWrapper class
#
##########################################


class SemaphoreWrapper():
    '''
    Используется для контроля скорости доступа к серверам Битрикс.

    Основная цель - вести учет количества запросов, которые можно передать
    серверу Битрикс без получения ошибки 503.

    Используется как контекстный менеджер, оборачивающий несколько
    последовательных запросов к серверу.

    Свойства:
    - release_task - указатель на задачу, которая увеличивает счетчик количества
    доступных запросов к серверу Битрикс. Должна выполняться параллельно
    с другими задачами в цикле asyncio.

    Методы:
    - __init__(self, pool_size: int, cautious: bool)/
    - acquire(self)
    '''


    def __init__(self, pool_size: int, cautious: bool):
        '''
        Создает объект SemaphoreWrapper.
        
        Параметры:
        - pool_size: int - размер пула доступных запросов.
        - cautious: bool - если равно True, то при старте количество
        доступных запросов равно нулю, а не pool_size. Другими словами,
        при подачи очереди запросов к серверу они будут подаваться без
        начального "взрыва", исчерпывающего изначально доступный пул
        запросов. 
        '''

        if cautious:
            self._stopped_time = time.monotonic()
            self._stopped_value = 0
        else:
            self._stopped_time = None
            self._stopped_value = None
        self._REQUESTS_PER_SECOND = 2
        self._pool_size = pool_size

    async def __aenter__(self):
        self._sem = asyncio.BoundedSemaphore(self._pool_size)
        if self._stopped_time:
            '''
-----v-----------------------------v---------------------
     ^ - _stopped_time             ^ - current time
     |-------- time_passed --------|
     |- step -|- step -|- step |          - add_steps (whole steps to add)
                               |- step -| - additional 1 step added
                                   |-aw-| - additional waiting time
            '''
            time_passed = time.monotonic() - self._stopped_time

            # сколько шагов должно было пройти
            add_steps = time_passed / self._REQUESTS_PER_SECOND // 1

            # сколько шагов могло пройти с учетом ограничений + еще один
            real_add_steps = min(self._pool_size - self._stopped_value,
                                 add_steps + 1)

            # добавляем пропущенные шаги
            self._sem._value += real_add_steps

            # ждем время, излишне списанное при добавлении дополнительного шага
            await asyncio.sleep((add_steps + 1) / self._REQUESTS_PER_SECOND - time_passed)

            self._stopped_time = None
            self._stopped_value = None

        self.release_task = asyncio.create_task(self._release_sem())

    async def __aexit__(self, a1, a2, a3):
        self._stopped_time = time.monotonic()
        self._stopped_value = self._sem._value
        self.release_task.cancel()

    async def _release_sem(self):
        while True:
            if self._sem._value < self._sem._bound_value:
                self._sem.release()
            await asyncio.sleep(1 / self._REQUESTS_PER_SECOND)

    async def acquire(self):
        '''
        Вызов acquire() должен предшествовать любому обращению
        к серверу Bitrix. Он возвращает True, когда к серверу
        можно осуществить запрос.

        Использование:
        ```
        await self.aquire()
        # теперь можно делать запросы
        ...
        ```
        '''
        return await self._sem.acquire()


##########################################
#
#   Bitrix class
#
##########################################


class Bitrix:
    '''
    Класс, оборачивающий весь цикл запросов к серверу Битрикс24.

    Методы:
    - __init__(self, webhook: str, custom_pool_size=50, cautious=False, autobatch=True)
    - get_all(self, method: str, details=None)
    - get_by_ID(self, method: str, ID_list, details=None)
    - def post(self, method: str, item_list)
    '''

    def __init__(self, webhook: str, custom_pool_size=50, cautious=False, autobatch=True):
        '''
        Создает объект класса Bitrix.

        Параметры:
        - webhook: str - URL вебхука, полученного от сервера Битрикс
        
        - custom_pool_size: int = 50 - размер пула запросов. По умолчанию 50 запросов - 
        это размер, указанный в официальной документации Битрикс24
        на июль 2020 г. (https://dev.1c-bitrix.ru/rest_help/rest_sum/index.php)
        
        - cautious: bool = False - стартовать, считая, что пул запросов уже
        исчерпан, и нужно контролировать скорость запросов с первого запроса
        
        - autobatch: bool = True - автоматически объединять списки запросов в батчи
        '''
        self.webhook = webhook
        self._sw = SemaphoreWrapper(custom_pool_size, cautious)
        self._autobatch = autobatch

    async def _request(self, session, method, params=None, pbar=None):
        await self._sw.acquire()
        url = f'{self.webhook}{method}?{_bitrix_url(params)}'
        async with session.get(url) as response:
            r = await response.json(encoding='utf-8')
        if pbar:
            pbar.update(len(r['result']))
        return r['result'], (r['total'] if 'total' in r.keys() else None)


    async def _request_list(self, method, item_list, real_len=None, real_start=0, preserve_IDs=False):
        if not real_len:
            real_len = len(item_list)

        if (self._autobatch) and (method != 'batch'):

            batch_size = 50
            while True:
                batch = [{
                    'halt': 0,
                    'cmd': {
                        item['ID'] if preserve_IDs else f'cmd{i}': 
                        f'{method}?{_bitrix_url(item)}'
                        for i, item in enumerate(next_batch)
                    }}
                    for next_batch in more_itertools.chunked(item_list, batch_size)
                ]
                uri_len = len(self.webhook + 'batch' +
                              urllib.parse.urlencode(batch[0]))
                if uri_len > BITRIX_URI_MAX_LEN:
                    batch_size = int(
                        batch_size // (uri_len / BITRIX_URI_MAX_LEN))
                else:
                    break

            method = 'batch'
            item_list = batch

        async with self._sw, aiohttp.ClientSession(raise_for_status=True) as session:
            tasks = [asyncio.create_task(self._request(session, method, i))
                     for i in item_list]
            results = []
            with tqdm(total=real_len, initial=real_start) as pbar:
                for x in asyncio.as_completed((*tasks, self._sw.release_task)):
                    r, __ = await x
                    if method == 'batch':
                        if preserve_IDs:
                            r = r['result'].items()
                        else:
                            r = list(r['result'].values())
                            if type(r[0]) == list:
                                r = list(itertools.chain(*r))
                    results.extend(r)
                    pbar.update(len(r))
                    if all([t.done() for t in tasks]):
                        break
            return results

    async def _get_paginated_list(self, method, params=None):
        async with self._sw, aiohttp.ClientSession(raise_for_status=True) as session:
            results, total = await self._request(session, method, params)
            if not total or total <= 50:
                return results
            remaining_results = await self._request_list(method, [
                _merge_dict({'start': start}, params)
                for start in range(len(results), total, 50)
            ], total, len(results))

            # дедуплицируем по id
            dedup_results = results
            for r in remaining_results:
                if r['ID'] not in [dr['ID'] for dr in dedup_results]:
                    dedup_results.append(r)

#           а более элегантный механизм ниже (через построение set()) не работает,
#           так как результаты содержат вложенные списки, которые не хэшируются
#           results = [dict(t) for t in {
#                tuple(d.items()) for d in list(itertools.chain(results, remaining_results))
#            }]
            return dedup_results

    def get_all(self, method: str, params=None):
        '''
        Получить полный список сущностей по запросу method.

        Под капотом использует параллельные запросы и автоматическое построение
        батчей, чтобы ускорить получение данных. Также самостоятельно
        обратывает постраничные ответы сервера, чтобы вернуть полный список.

        Параметры:
        - method - метод REST API для запроса к серверу
        - params - параметры для передачи методу. Используется именно тот формат,
            который указан в документации к REST API Битрикс24

        Возвращает полный список сущностей, имеющихся на сервере,
        согласно заданным методу и параметрам.
        '''

        return asyncio.run(self._get_paginated_list(method, params))

    def get_by_ID(self, method: str, ID_list, params=None):
        '''
        Получить список сущностей по запросу method и списку ID.

        Используется для случаев, когда нужны не все сущности,
        имеющиеся в базе, а конкретный список поименованных ID.
        Например, все контакты, привязанные к сделкам.

        Параметры:
        - method - метод REST API для запроса к серверу
        - ID_list - список ID
        - params - параметры для передачи методу. Используется именно тот
            формат, который указан в документации к REST API Битрикс24

        Возвращает список кортежей вида:

            [
                (ID, <результат запроса>), 
                (ID, <результат запроса>), 
                ...
            ]

        Вторым элементом каждого кортежа будет результат выполнения запроса
        относительно этого ID. Это может быть, например, список связанных
        сущностей или пустой список, если не найдено ни одной привязанной
        сущности.
        '''

        return asyncio.run(self._request_list(
            method,
            [_merge_dict({'ID': ID}, params) for ID in ID_list] if params else
            [{'ID': ID} for ID in set(ID_list)],
            preserve_IDs=True
        ))

    def call(self, method: str, item_list):
        '''
        Вызвать метод REST API по списку.

        Параметры:
        - method - метод REST API
        - item_list - список параметров вызываемого метода

        Возвращает список ответов сервера для каждого из элементов item_list.
        '''
        return asyncio.run(self._request_list(method, item_list))


##########################################
#
#   internal functions
#
##########################################


def _bitrix_url(data):
    parents = list()
    pairs = list()

    def renderKey(parents):
        depth, outStr = 0, ''
        for x in parents:
            s = "[%s]" if (depth > 0 or isinstance(x, int)) and x!='[]' else "%s"
            outStr += s % str(x)
            depth += 1
        return outStr

    def r_urlencode(data):
        if isinstance(data, list) or isinstance(data, tuple):
            for i in range(len(data)):
                parents.append('[]')
                r_urlencode(data[i])
                parents.pop()
        elif isinstance(data, dict):
            for key, value in data.items():
                parents.append(key)
                r_urlencode(value)
                parents.pop()
        else:
            pairs.append((renderKey(parents), str(data)))

        return pairs
    return urllib.parse.urlencode(r_urlencode(data))


def _merge_dict(d1, d2):
    d3 = d1.copy()
    if d2:
        d3.update(d2)
    return d3
