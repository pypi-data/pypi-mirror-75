# coding=utf-8 
'''
Created on 2018年2月28日

@author: heguofeng

todo:
用dh 交换，加密

'''
import binascii
import hashlib
import json
import logging
import platform
import threading
import time

from .common import set_debug, packaddr, Log
from .config import PublicNetId, BroadCastId
from .ppl1node import PPLayer
from .ppl2node import PPApp, PP_APPID
from .ppl3node import PPL3Node


class PPNet(PPLayer):
    """
    ppnet =  PPNet(ppl3node)
    ppnet.send(data,node_id)

    callback(node_id,text)
    """

    def __init__(self, underlayer=None):
        super().__init__(underlayer)

    def send(self, data, addr):
        self._underlayer.dataer.send_data(data, addr)

    def receive(self, count=1522):
        return self._underlayer.dataer.receive_data(count)

    def process(self, data, addr):
        logging.debug("receive data from {0} :{1}\n ".format(addr,
                                                             ''.join('{:02x} '.format(x) for x in data[:16])))
        if self.callback:
            self.callback(data, addr)


class PPNetNode(PPNet):
    def __init__(self, **kwargs):
        # config={"node_port": 0, "node_id": b"\0" * 6},node_port=0,node_id=b"\0" * 6):
        self.config={"node_port": 0, "node_id": b"\0" * 6}
        if "config" in kwargs:
            self.config.update(kwargs["config"])
        if "node_port" in kwargs:
            self.config.update({"node_port":kwargs["node_port"]})
        if "node_id" in kwargs:
            self.config.update({"node_id":kwargs["node_id"]})
        l3node = PPL3Node(self.config)
        super().__init__(l3node)
        l3node.dataer.callback = self.process

    def wait_receive(self, callback):
        self.set_callback(callback)

    @property
    def node_id(self):
        return self.underlayer.node_id

    @node_id.setter
    def node_id(self, id=None):
        """
        set node_id
        :param id: bytes or addr tuple(ip,port)
        :return:
        """
        if isinstance(id, bytes):
            self.underlayer.node_id = id
        elif isinstance(id, tuple):  # addr=(ip,port)
            self.underlayer.node_id = packaddr(id)
        self.underlayer.beater.rebeat()

    @property
    def sockname(self):
        return (self._underlayer.ip, self._underlayer.port)

    @property
    def sock(self):
        return self.underlayer.underlayer.sock

    @Log("info")
    def set_peer(self, peer_addr):
        node_id = packaddr(peer_addr)
        if node_id not in self.underlayer.peers:
            self.underlayer.set_peer_addr(node_id, peer_addr,enforce=True)
        return node_id

    @Log("info")
    def del_peer(self,peer_addr):
        node_id = packaddr(peer_addr)
        if node_id in self.underlayer.peers:
            self.underlayer.del_peer(node_id)
        return node_id



def main(config):
    print("PPData Network is lanching...")
    station = PPL3Node(config=config)
    station.start()
    try_count = 0
    while not station.status:
        time.sleep(2)
        station.status = station._check_status()
        try_count += 1
        if try_count > 10 or station.quitting:
            break
    print("node_id=%d online=%s" % (station.node_id, station.status))

    #     if station.status:
    #         station.path_requester.request_path(BroadCastId, 6)
    node_type = config.get("node_type", "server")
    is_client = node_type == "client"
    while not is_client and not station.quitting:
        time.sleep(3)

    s = "help"
    while not station.quitting:
        try:
            station.run_command(s)
            print("\n%d>" % station.node_id, end="")
        except Exception as exp:
            print(exp.__str__())
        if not station.quitting:
            s = input()

    print("PPNetwork Quit!")


if __name__ == '__main__':
    config = {"auth_mode": "secret", "secret": "password",
              "share_folder": ".", "net_id": PublicNetId,
              "pp_net": "home", "node_id": b"100",
              "node_port": 54320, "DebugLevel": logging.DEBUG,
              "nodes": {b"101": {"node_id": b"101", "ip": "127.0.0.1", "port": 54321, "nat_type": 0}}
              # (id,ip,port,type)..]
              }
    # config = yaml.load(open("fmconfig.yaml"))
    set_debug(config.get("DebugLevel", logging.WARNING),
              config.get("DebugFile", ""))

    main(config=config)

    pass
