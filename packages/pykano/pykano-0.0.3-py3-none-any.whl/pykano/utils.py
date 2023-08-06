import datetime
import os


def kprint(log):
    print(datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S') + '\n' + log)


def ktolist(path):
    ls = []
    with open(path, mode='r', encoding='UTF-8') as f:
        for i in f.readlines():
            if i.strip() != "":
                ls.append(i.strip())
    return ls


def ktotext(ls, path):
    if os.path.exists(path):
        os.remove(path)
    for i in list(ls):
        if i.strip() != '':
            with open(path, mode='a+', encoding='UTF-8') as w:
                w.write(i.strip() + '\n')
