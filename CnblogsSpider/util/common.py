# _*_ coding :utf-8 _*_
__author__ = 'du'
__bolg__ = 'www.github.com/anmutu;'
__date__ = '2020/2/21 16:28'

import hashlib
import time


def get_md5(url):
    if isinstance(url, str):
        url = url.encode("utf-8")
    md5 = hashlib.md5()
    md5.update(url)
    return md5.hexdigest()


if __name__ == "__main__":
    print(get_md5("www.cnblogs.com"))

    print(time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())))
    print(time.strftime('%Y%m%d%H%M%S', time.localtime(time.time())))




