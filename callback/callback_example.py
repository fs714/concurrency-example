datas = range(0, 100)


def func(callback, args=[], kwargs={}):
    for data in datas:
        callback(data, args, kwargs)


def cb(data, args=[], kwargs={}):
    print('Current Data: {}'.format(data))
    args.append(data)
    print('Arguments args: {}'.format(args))
    for k, v in kwargs.items():
        print('Arguments kwargs: {}: {}'.format(k, v))


if __name__ == '__main__':
    for i in range(0, 100):
        func(cb, [], {'key1': 'value1', 'key2': 'value2'})
