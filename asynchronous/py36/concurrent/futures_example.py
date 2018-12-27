import time
from concurrent.futures import ThreadPoolExecutor, ProcessPoolExecutor, as_completed


def func1(cnt):
    time.sleep(2)
    print(cnt)
    return cnt * 2


def func2(a, b, c):
    time.sleep(2)
    print('a: ' + str(a) + ', b: ' + str(b) + ', c: ' + str(c))
    return a + b + c


if __name__ == "__main__":
    print('Map with single param')
    executor = ThreadPoolExecutor(max_workers=3)
    res = list(executor.map(func1, range(0, 10)))
    print(res)

    executor = ProcessPoolExecutor(max_workers=3)
    res = list(executor.map(func1, range(0, 10)))
    print(res)

    print('Map with multi param')
    executor = ThreadPoolExecutor(max_workers=3)
    res = list(executor.map(func2, range(0, 10), range(10, 20), range(20, 30)))
    print(res)

    executor = ProcessPoolExecutor(max_workers=3)
    res = list(executor.map(func2, range(0, 10), range(10, 20), range(20, 30)))
    print(res)

    print('Submit with multi param')
    with ThreadPoolExecutor(max_workers=3) as executor:
        a = list(range(0, 10))
        b = list(range(10, 20))
        c = list(range(20, 30))
        future_dict = {}
        for i in range(0, len(a)):
            future = executor.submit(func2, a[i], b[i], c[i])
            future_dict[future] = i

        for f in as_completed(future_dict):
            print("Index: " + str(future_dict[f]) + ", result: " + str(f.result()))

    with ProcessPoolExecutor(max_workers=3) as executor:
        a = list(range(0, 10))
        b = list(range(10, 20))
        c = list(range(20, 30))
        future_dict = {}
        for i in range(0, len(a)):
            future = executor.submit(func2, a[i], b[i], c[i])
            future_dict[future] = i

        for f in as_completed(future_dict):
            print("Index: " + str(future_dict[f]) + ", result: " + str(f.result()))
