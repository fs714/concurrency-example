# import asyncio
#
# async def compute(x, y):
#     print("Compute %s + %s ..." % (x, y))
#     await asyncio.sleep(1.0)
#     return x + y
#
# async def print_sum(x, y):
#     for i in range(10):
#         result = await compute(x, y)
#         print("%s + %s = %s" % (x, y, result))
#
# loop = asyncio.get_event_loop()
# loop.run_until_complete(print_sum(1,2))


# asyncio.ensure_future(print_sum(1, 2))
# asyncio.ensure_future(print_sum(3, 4))
# asyncio.ensure_future(print_sum(5, 6))
# loop.run_forever()



import asyncio

async def display_date(who, num):
    i = 0
    while True:
        if i > num:
            return
        print('{}: Before loop {}'.format(who, i))
        await asyncio.sleep(1)
        i += 1

loop = asyncio.get_event_loop()
asyncio.ensure_future(display_date('AAA', 4))
asyncio.ensure_future(display_date('BBB', 6))
loop.run_forever()
