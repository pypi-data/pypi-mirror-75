import requests
import platform
import socket


def http_get(url, proxy=None, to=10, callback=None):
    ctx = requests.get(url, proxies =proxy, timeout=to)
    if ctx.status_code==200:
        rtn = ctx.json()
        if callback:
            callback(**rtn)
        else:
            return rtn
    else:
        if callback:
            callback(None)
        else:
            return None


def http_post(url, data, proxy=None, to=10):
    ctx = requests.post(url, data, proxies =proxy, timeout=to)
    if ctx.status_code==200:
        return ctx.json()
    else:
        with open("a.html", "w+", encoding='utf-8') as f:
            f.write(ctx.text)
        return None


def get_device_name():
    try:
        devid = platform.node()
    except:
        devid = socket.gethostname()
    return devid


def get_device_id():
    """
    获得序号最小的2个mac地址，如果不存在那么就随机一个uuid，并持久化起来
    """
    import netifaces
    nic = netifaces.interfaces() # 得到一个数字，代表全部的接口
    nic = sorted(nic)
    for n in nic:
        mac = netifaces.ifaddresses(n)
        mac = mac[netifaces.AF_LINK]
        if mac:
            return mac[0]['addr']# TODO 保证不能异常
    # TODO 保存一个uuid到home下
    return "uuid-device_id"


if __name__=="__main__":
    print(get_device_id())
