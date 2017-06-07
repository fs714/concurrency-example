import asyncio

print('running async test')

async def say_boo():
    i = 0
    while True:
        await asyncio.sleep(0)
        print('...boo {0}'.format(i))
        i += 1

async def say_baa():
    i = 0
    while True:
        await asyncio.sleep(0)
        print('...baa {0}'.format(i))
        i += 1

# OPTION 1: wrap in Task object
# -> automatically attaches to event loop and executes
boo = asyncio.ensure_future(say_boo())
baa = asyncio.ensure_future(say_baa())

loop = asyncio.get_event_loop()
loop.run_forever()