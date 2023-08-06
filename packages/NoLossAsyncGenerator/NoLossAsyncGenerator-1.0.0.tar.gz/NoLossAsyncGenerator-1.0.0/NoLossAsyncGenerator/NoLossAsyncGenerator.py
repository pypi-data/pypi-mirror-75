'''
Asynchronous generator without any data loss in case that handling one message costs too much time.
'''
import asyncio


async def no_data_loss_async_generator(raw_async_generator):
    q = asyncio.Queue()

    async def yield2q(raw_async_generator, q: asyncio.Queue):
        async for msg in raw_async_generator:
            q.put_nowait(msg)

    asyncio.create_task(yield2q(raw_async_generator, q))
    while True:
        msg = await q.get()
        yield msg


def no_data_loss_async_generator_decorator(async_generator_function):
    async def g(*args, **kwargs):
        async for msg in no_data_loss_async_generator(async_generator_function(*args, **kwargs)):
            yield msg

    return g


if __name__ == '__main__':

    async def test_no_data_loss_async_generator():
        async def g():
            n = 0
            while True:
                yield n
                n += 1
                await asyncio.sleep(1)

        m = 0
        async for n in no_data_loss_async_generator(g()):
            print(n)
            m += 1
            if m <= 5:
                await asyncio.sleep(2)


    async def test_no_data_loss_async_generator_decorator():
        @no_data_loss_async_generator_decorator
        async def g():
            n = 0
            while True:
                yield n
                n += 1
                await asyncio.sleep(1)

        m = 0
        async for n in g():
            print(n)
            m += 1
            if m <= 5:
                await asyncio.sleep(2)


    asyncio.run(test_no_data_loss_async_generator())
