import time
from multiprocessing import Pool
from multiprocessing.pool import ThreadPool


def func(a, b, c):
    time.sleep(2)
    print('a: ' + str(a) + ', b: ' + str(b) + ', c: ' + str(c))
    return a + b + c


if __name__ == "__main__":
    a = list(range(0, 10))
    b = list(range(10, 20))
    c = list(range(20, 30))

    print('Thread pool execution')
    pool = ThreadPool(processes=3)
    result = {}
    for i in range(0, len(a)):
        r = pool.apply_async(func, kwds={'a': a[i], 'b': b[i], 'c': c[i]})
        result[i] = r
    pool.close()
    pool.join()

    for k, v in result.items():
        print('Index: ' + str(k) + ', result: ' + str(v.get()))

    print('Process pool execution')
    pool = Pool(processes=3)
    result = {}
    for i in range(0, len(a)):
        r = pool.apply_async(func, kwds={'a': a[i], 'b': b[i], 'c': c[i]})
        result[i] = r
    pool.close()
    pool.join()

    for k, v in result.items():
        print('Index: ' + str(k) + ', result: ' + str(v.get()))
