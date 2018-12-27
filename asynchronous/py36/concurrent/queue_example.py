import queue
import time
from multiprocessing import Pool, Manager
from multiprocessing.pool import ThreadPool


def func(q, i, a, b, c):
    time.sleep(2)
    q.put({'Index': i, 'Result': a + b + c})
    print('a: ' + str(a) + ', b: ' + str(b) + ', c: ' + str(c))
    return a + b + c


if __name__ == "__main__":
    a = list(range(0, 10))
    b = list(range(10, 20))
    c = list(range(20, 30))

    print('Thread pool execution')
    q = queue.Queue()
    pool = ThreadPool(processes=3)
    result = {}
    for i in range(0, len(a)):
        r = pool.apply_async(func, kwds={'q': q, 'i': i, 'a': a[i], 'b': b[i], 'c': c[i]})
        result[i] = r
    pool.close()
    pool.join()

    for k, v in result.items():
        print('Index: ' + str(k) + ', result: ' + str(v.get()))

    while not q.empty():
        print(q.get())

    print('Process pool execution')
    m = Manager()
    q = m.Queue()
    pool = Pool(processes=3)
    result = {}
    for i in range(0, len(a)):
        r = pool.apply_async(func, kwds={'q': q, 'i': i, 'a': a[i], 'b': b[i], 'c': c[i]})
        result[i] = r
    pool.close()
    pool.join()

    for k, v in result.items():
        print('Index: ' + str(k) + ', result: ' + str(v.get()))

    while not q.empty():
        print(q.get())
