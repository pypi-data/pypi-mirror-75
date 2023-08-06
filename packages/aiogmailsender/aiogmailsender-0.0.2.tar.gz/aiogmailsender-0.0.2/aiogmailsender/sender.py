import asyncio
import types
import logging

import aiosmtplib


class Notifier:
    def notify_failure(self, exception):
        raise RuntimeError('no implementation')

    def notify_success(self):
        raise RuntimeError('no implementation')


class NoopNotifier(Notifier):

    def notify_failure(self, exception):
        pass

    def notify_success(self):
        pass


class ClientFactory:
    def __init__(self, username, password, **options):
        self.username = username
        self.password = password
        self.options = options

    async def new_client(self):
        return await Client.create(self.username, self.password, **self.options)


class Client:
    def __init__(self):
        self.username = None
        self.password = None

        self.retry = 0
        self.backoff = 0
        self.backoff_limit = 0
        self.notifier = None

        self.conn = None

    @classmethod
    async def create(cls, username, password, retry=5, backoff=30, backoff_limit=300, notifier=NoopNotifier()):
        logging.debug('create a client')
        self = cls()
        self.username = username
        self.password = password

        self.retry = retry
        self.backoff = backoff
        self.backoff_limit = backoff_limit
        self.notifier = notifier

        await self.connect()
        return self

    async def send(self, message):
        retry = self.retry
        backoff = self.backoff

        while True:
            try:
                if not self.conn.is_connected:
                    await self.connect()
                logging.debug('%s: try to send a message (%s)', self, message['Subject'])
                result = await self.conn.send_message(message)
                self.notifier.notify_success()
                logging.debug('%s: successfully sent a message (%s)', self, message['Subject'])

                return result
            except aiosmtplib.errors.SMTPServerDisconnected as e:
                self.notifier.notify_failure(e)

                if retry <= 0:
                    self._raise(e)
                logging.debug('SMTP server is disconnected')
                logging.debug('retry (%s left)', retry - 1)
                retry -= 1

            except (aiosmtplib.errors.SMTPDataError, aiosmtplib.errors.SMTPSenderRefused) as e:
                self.notifier.notify_failure(e)

                if e.code != 421:
                    self._raise(e)
                if retry <= 0:
                    self._raise(e)
                logging.debug('421 occurred while sending email: %s', e.args)
                logging.debug('sleep (%s seconds) and retry (%s left)', backoff, retry - 1)
                await asyncio.sleep(backoff)

                retry -= 1
                backoff *= 2
                if self.backoff_limit < backoff:
                    backoff = self.backoff_limit

            except Exception as e:
                self._raise(e)

    async def connect(self):
        logging.debug('try to connect')
        conn = aiosmtplib.SMTP(hostname='smtp.gmail.com', port=587, start_tls=True)
        await conn.connect()
        await conn.login(self.username, self.password)
        self.conn = conn

    def __del__(self):
        self.conn.close()

    def _raise(self, e):
        self.conn.close()
        raise e


class Task:
    def __init__(self, message):
        self.message = message
        self.event = asyncio.Event()
        self.result = None
        self.exception = None

    async def get_result(self):
        await self.event.wait()

        if self.exception:
            raise self.exception
        return self.result

    def set_result(self, result):
        self.result = result
        self.event.set()

    def set_exception(self, exception):
        self.exception = exception
        self.event.set()


class Pool:
    def __init__(self):
        self.size = 0
        self.clients = None

    @classmethod
    async def create(cls, size, client_factory):
        self = cls()
        self.size = size
        self.clients = asyncio.Queue()

        async def _create():
            client = await client_factory.new_client()
            self.clients.put_nowait(client)

        await asyncio.gather(*[_create() for _ in range(size)])
        return self

    async def handle(self, task):
        client = await self.clients.get()

        async def _handle():
            try:
                result = await client.send(task.message)
                task.set_result(result)
            except Exception as exception:
                task.set_exception(exception)
            self.clients.put_nowait(client)

        asyncio.create_task(_handle())


class LooperController(Notifier):
    def __init__(self, looper):
        self.looper = looper

    def notify_failure(self, exception):
        if isinstance(exception, aiosmtplib.errors.SMTPSenderRefused):
            if exception.code == 421:
                self.looper.pause()

    def notify_success(self):
        self.looper.resume()


class Looper(Notifier):
    def __init__(self):
        self.rate_limit = None
        self.pool = None
        self.is_paused = False
        self.resume_event = None

        self.tasks = asyncio.Queue()
        self.lock = asyncio.Lock()

    @classmethod
    async def create(cls, username, password, rate_limit=60, pool_size=2, **options):
        self = cls()
        self.rate_limit = rate_limit
        self.pool = await Pool.create(pool_size,
                                      ClientFactory(username, password, notifier=LooperController(self), **options))

        self.is_paused = False
        self.resume_event = asyncio.Event()

        return self

    def post(self, task):
        self.tasks.put_nowait(task)

    async def loop(self):
        logging.debug('start to loop')
        while True:
            if self.is_paused:
                await self.wait_for_resume()
                continue

            task = await self.tasks.get()
            await self.pool.handle(task)

            if self.rate_limit > 0:
                await asyncio.sleep(60 / self.rate_limit)

    async def wait_for_resume(self):
        await self.resume_event.wait()

    def pause(self):
        if self.is_paused:
            return

        logging.debug('looper pause')
        self.is_paused = True
        self.resume_event.clear()

    def resume(self):
        if not self.is_paused:
            return

        logging.debug('looper resume')
        self.is_paused = False
        self.resume_event.set()


NS = types.SimpleNamespace()


class Sender:
    def __init__(self):
        self.looper = None

    @classmethod
    async def create(cls, username, password, **options):
        self = cls()

        looper = await Looper.create(username, password, **options)
        asyncio.create_task(looper.loop())
        self.looper = looper
        return self

    def send(self, message):
        task = Task(message)
        self.looper.post(task)

        return asyncio.create_task(task.get_result())
