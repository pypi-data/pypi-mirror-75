# coding=utf-8

import os
import subprocess
import time
import logging
import struct
import socket

from .config import PP_APPID, version

import argparse


class Log(object):
    """
    @Log(level='WARNING')
    def say(something):
        print("say {}!".format(something))
    """

    def __init__(self, level='INFO'):
        self.level = level

    def __call__(self, func):
        # 接受函数
        def wrapper(*args, **kwargs):
            if self.level == "DEBUG":
                logging.debug("{} \nargs: {} \n".format(func.__name__, ''.join('\n{}'.format(x) for x in args)))
            elif self.level == "INFO":
                logging.info("{} \nargs: {} \n".format(func.__name__, ''.join('\n{}'.format(x) for x in args)))
            elif self.level == "WARNING":
                logging.warning("{} \nargs: {} \n".format(func.__name__, ''.join('\n{}'.format(x) for x in args)))
            else:
                logging.info("{} \nargs: {} \n".format(func.__name__, ''.join('\n{}'.format(x) for x in args)))
            func(*args, **kwargs)

        return wrapper  # 返回函数


def ota():
    if os.path.exists("start.bat"):
        subprocess.check_output("start.bat")
    if os.path.exists("reload.bat"):
        subprocess.check_output("reload.bat")


def ota2():
    if os.path.exists("reload.bat"):
        subprocess.check_output("reload.bat", cwd=".", shell=False)


def get_app_name(app_id):
    for app_name in PP_APPID:
        if PP_APPID[app_name] == app_id:
            return app_name
    return "Unknown"


def _is_private_ip(ip):
    if ip.startswith("172.") or ip.startswith("192.") or ip.startswith("10."):
        return True
    else:
        return False


def restart_nic(nic):
    subprocess.getstatusoutput('netsh interface set interface "' + nic + '" disabled')
    time.sleep(10)
    subprocess.getstatusoutput('netsh interface set interface "' + nic + '" enabled')


def set_debug(debug_level=logging.INFO, filename="", debug_filter=lambda record: True):
    console = logging.StreamHandler()
    console_filter = logging.Filter()
    console_filter.filter = debug_filter
    console.addFilter(console_filter)
    if filename:
        logging.basicConfig(level=debug_level,
                            format='%(asctime)s %(filename)s[line:%(lineno)d] %(levelname)s %(message)s',
                            datefmt='%Y/%m/%d %H:%M:%S',
                            filename=filename,
                            filemode='w',
                            )
    else:
        logging.basicConfig(level=debug_level,
                            format='%(asctime)s %(filename)s[%(lineno)d] %(levelname)s %(message)s',
                            datefmt='%Y/%m/%d %H:%M:%S',
                            # handlers=[console, ]
                            )


def wait(trytimes):
    def wrapper(func):
        def deco(*args, **kwargs):
            count = 0
            while count < trytimes:
                if func(*args, **kwargs):
                    return True
                count += 1

        return deco

    return wrapper


# 这是装饰函数
# def Log1(level):
#     def wrapper(func):
#         def logger(*args, **kw):
#             if level=="debug":
#                 logging.debug("{} \nargs: {} \n".format(func.__name__,''.join('\n{}'.format(x) for x in args)))
#             elif level=="info":
#                 logging.info("{} \nargs: {} \n".format(func.__name__,''.join('\n{}'.format(x) for x in args)))
#             func(*args, **kw)
#         return logger
#     return wrapper


def do_wait(func, test_func, times, interval=1):
    count = 0
    while count < times:
        func()
        time.sleep(interval)
        if test_func():
            return True
        count += 1
    return False


def wait_available(datadict, item, times):
    if do_wait(lambda: True, lambda: item in datadict, times):
        return datadict[item]
    else:
        return None


def wait_result(item, result, times):
    if do_wait(lambda: True, lambda: item == result, times):
        return item


def ip_stoi(ip):
    return socket.ntohl(struct.unpack("I", socket.inet_aton(ip))[0])


def ip_itos(ip):
    return socket.inet_ntoa(struct.pack("I", socket.htonl(ip)))


def is_turnable(nat_type):
    return nat_type < 3


def of_bytes(node):
    return node if isinstance(node, bytes) else node.encode()


def unpackip(bin_ip):
    return socket.inet_ntoa(struct.pack('I', socket.htonl(struct.unpack("I", bin_ip)[0])))


def packip(ip):
    return struct.pack("I", socket.ntohl(struct.unpack("I", socket.inet_aton(ip))[0]))


def packaddr(addr):
    return packip(addr[0]) + struct.pack("H", addr[1])


def unpackaddr(bindata):
    return unpackip(bindata[:4]), struct.unpack("H", bindata[4:6])[0]


def parser_argument():
    parser = argparse.ArgumentParser(
        formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument('-d', '--debug', action='store_true',
                        default=False,
                        help='Enable debug logging')
    parser.add_argument('--daemon', action='store_true',
                        default=False,
                        help='daemon mode')
    parser.add_argument('-o', '--org_id',
                        default="misas",
                        help='org id')
    parser.add_argument('-n', '--node_id',
                        default="",
                        help='node id')
    parser.add_argument('-p', '--password',
                        default="",
                        help='password for node')
    parser.add_argument('--vpn_user',
                        default="",
                        help='vpn user id')
    parser.add_argument('--vpn_password',
                        default="",
                        help='password for vpn')
    parser.add_argument('--tcp', action='store_true',
                        default=False,
                        help='tcp mode')
    parser.add_argument('-f', '--config',
                        default="",
                        help='config file')
    parser.add_argument('--server_port',
                        default=9000,
                        help='remote port')
    parser.add_argument('--server_ip',
                        default="127.0.0.1",
                        help='remote ip')
    parser.add_argument('--brain_ip',
                        default="14.29.201.19",
                        help='brain ip')
    parser.add_argument('--brain_port',
                        default="54320",
                        help='brain port')

    parser.add_argument('--version', action='version', version=version)
    return parser
