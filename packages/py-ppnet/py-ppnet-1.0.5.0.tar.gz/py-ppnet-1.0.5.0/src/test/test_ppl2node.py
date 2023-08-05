import unittest

from ppnet.config import NAT_TYPE, PP_APPID
from ppnet.common import set_debug
from ppnet.ppbeater import Beater
from ppnet.ppl2node import PPL2Node, PPMessage
from ppnet.ppl3node import PPL3Node
from ppnet.ppl4node import PPNet, PPNetNode
from test.mocknet import MockNet
import time
import logging


class TestL2(unittest.TestCase):
    inited = 0
    def start(self):
        set_debug(logging.DEBUG)

        self.addrA = ("118.153.152.193", 54330)
        self.addrB = ("118.153.152.193", 54320)
        self.addrC = ("118.153.152.193", 54321)
        self.nodeinfoA = {"node_id": b"PPSTA1", "node_ip": self.addrA[0], "node_port": self.addrA[1],
                          "nat_type": NAT_TYPE["Turnable"], "secret": "password"}
        self.nodeinfoB = {"node_id": b"PPSTA2", "node_ip": self.addrB[0], "node_port": self.addrB[1],
                          "nat_type": NAT_TYPE["Turnable"], "secret": "password"}
        self.nodeinfoC = {"node_id": b"PPSTA3", "node_ip": self.addrC[0], "node_port": self.addrC[1],
                          "nat_type": NAT_TYPE["Turnable"], "secret": "password"}
        self.stationA = PPL3Node(config=self.nodeinfoA)
        self.stationB = PPL3Node(config=self.nodeinfoB)
        self.stationC = PPL3Node(config=self.nodeinfoC)

        self.stationA.set_underlayer(MockNet(self.stationA))
        self.stationB.set_underlayer(MockNet(self.stationB))
        self.stationC.set_underlayer(MockNet(self.stationC))
        # self.mock_net = MockNet()
        # self.mock_net.mock(self.stationA)
        # self.mock_net.mock(self.stationB)
        # self.mock_net.mock(self.stationC)
        self.inited = 1

    def setUp(self):
        if self.inited == 0:
            self.start()
        pass

    def tearDown(self):
        pass

    def testL2Node(self):
        self.assertEqual(self.stationA.node_id, b"PPSTA1")
        self.assertEqual(self.stationB.node_id, b"PPSTA2")
        self.assertEqual(self.stationC.node_id, b"PPSTA3")

    def ack_callback(self,peer_id,sequence,status):
        print(peer_id,sequence,status)
        self.ackResult = status

    # def ttestAckor(self):
    #     # self.stationA = self.mock_net.mock(PPL2Node(config={"node_id":b"100", "node_ip":"118.153.152.193", "node_port":54330, "nat_type":NAT_TYPE["Turnable"]},
    #     #                                             ack_callback=self.ack_callback ))
    #     self.ackResult = False
    #     self.stationA.services[PP_APPID["Ack"]].set_callback(self.ack_callback)
    #     dictdataA={"src_id":b"PPSTA1","dst_id":b"PPSTA2",
    #                "app_data":b"app_data",
    #                "app_id":7}
    #     self.stationA.start()
    #     self.stationB.start()
    #     # to have a hole
    #     dictdataB={"src_id":b"PPSTA2","dst_id":b"PPSTA3",
    #                "app_data":b"app_data",
    #                "app_id":7}
    #     self.stationB.send_ppmsg_peer(PPMessage(dictdata=dictdataB),self.stationC)
    #     self.stationA.send_ppmsg_peer(PPMessage(dictdata=dictdataA),self.stationB,  need_ack=True)
    #
    #     time.sleep(1)
    #     self.assertTrue(self.ackResult, "test Ackor")
    #     self.stationA.quit()
    #     self.stationB.quit()

    def testAckor(self):
        # self.stationA = self.mock_net.mock(PPL2Node(config={"node_id":b"100", "node_ip":"118.153.152.193", "node_port":54330, "nat_type":NAT_TYPE["Turnable"]},
        #                                             ack_callback=self.ack_callback ))
        print("======start ackor========================================")
        self.ackResult = False
        self.stationA.services[PP_APPID["Ack"]].set_callback(self.ack_callback)

        bt_dictdata = {
            "command": "beat_req",
            "parameters": {
                "net_id": 1,
                "node": self.nodeinfoA,
                "peer": self.nodeinfoB,
                "timestamp": int(time.time()),
            }
        }
        bm = Beater.BeatMessage(dictdata=bt_dictdata)
        dictdataA = {"src_id": b"PPSTA1", "dst_id": b"PPSTA2",
                     "app_data": bm.dump(),
                     "app_id": 7}
        self.stationA.start()
        self.stationB.start()

        # to have a hole
        dictdataB = {"src_id": b"PPSTA2", "dst_id": b"PPSTA3",
                     "app_data": b"app_data",
                     "app_id": 7}
        self.stationB.send_ppmsg_peer(PPMessage(dictdata=dictdataB), self.stationC)
        self.stationA.send_ppmsg_peer(PPMessage(dictdata=dictdataA), self.stationB, need_ack=True)

        time.sleep(1)
        self.assertTrue(self.ackResult, "test Ackor")
        self.stationA.quit()
        self.stationB.quit()
        time.sleep(2)
        print("======end ackor========================================")




if __name__ == '__main__':
    unittest.main()
