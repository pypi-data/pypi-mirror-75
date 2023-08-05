import time
import unittest
import logging
from ppnet.common import set_debug
from ppnet.config import NAT_TYPE
from ppnet.ppl3node import PPL3Node
from ppnet.ppl4node import PPNet, PPNetNode
from test.mocknet import MockNet


class TestL3(unittest.TestCase):
    '''
    todo：多个测试时会出现 duplication message，怀疑和多线程测试有关，
    '''

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
        time_scale = 1
        self.stationA.beater.time_scale = time_scale
        self.stationB.beater.time_scale = time_scale
        self.stationC.beater.time_scale = time_scale

        self.stationA.set_underlayer(MockNet(self.stationA))
        self.stationB.set_underlayer(MockNet(self.stationB))
        self.stationC.set_underlayer(MockNet(self.stationC))
        self.nodes = [(b"PPSTA1", self.addrA[0], self.addrA[1], NAT_TYPE["Turnable"]),
                      (b"PPSTA2", self.addrB[0], self.addrB[1], NAT_TYPE["Turnable"]),
                      (b"PPSTA3", self.addrC[0], self.addrC[1], NAT_TYPE["Turnable"]), ]
        TestL3.inited = 1

    def setUp(self):
        self.start()
        pass

    def tearDown(self):
        # self.stationA.quit()
        # self.stationB.quit()
        # self.stationC.quit()
        pass

    def testBeatnull(self):
        self.stationA.beater.beat_null()
        self.stationB.beater.beat_null()
        self.stationC.beater.beat_null()
        self.assertTrue(self.stationA.underlayer.nat.inaddrs())

    def testBeat(self):
        print("======start beat========================================")
        # self.stationA.underlayer.clear()
        speedup = 0.01
        self.stationA.beater.time_scale = speedup
        self.stationB.beater.time_scale = speedup
        self.stationC.beater.time_scale = speedup
        self.stationA.start()
        self.stationB.start()
        self.stationC.start()

        self.assertTrue(self.stationA.status == False, "StationA offline")
        self.assertTrue(self.stationB.status == False, "StationA offline")
        self.assertTrue(self.stationC.status == False, "StationA offline")
        self.stationB.set_nodes(self.nodes)
        time.sleep(2)
        self.assertTrue(self.stationA.status, "StationA online")
        self.assertTrue(self.stationB.status, "StationB online")
        self.assertTrue(self.stationC.status, "StationC online")
        self.stationA.quit()
        self.stationB.quit()
        self.stationC.quit()
        print("======end beat========================================")

    def testPath(self):
        self.stationA.underlayer.clear()
        self.stationA.set_nodes(self.nodes[:2])
        self.stationA.start()
        self.stationB.set_nodes(self.nodes[1:])
        self.assertTrue(self.stationC.status == False, "StationC offline")
        self.stationB.start()
        self.stationC.start()
        self.stationB.beater.beat()
        time.sleep(10)
        self.assertTrue(self.stationC.status,"StationC online")
        self.stationA.pather.request_path(b"PPSTA3")
        time.sleep(1)
        self.assertEqual(self.stationA.get_node_path(b"PPSTA3"), [b"PPSTA3"], "Find StationC Path")
        # self.assertEqual(self.stationA.get_status(b"PPSTA3"),True,"Find StationC Path 2")
        print(self.stationA.get_node_path(b"PPSTA3"))
        print(self.stationC.get_node_path(b"PPSTA1"))
        time.sleep(5)
        self.stationA.quit()
        self.stationC.quit()
        self.stationB.quit()

    def testData(self):
        self.stationA.underlayer.clear()
        self.stationB.set_nodes(self.nodes)
        self.stationA.set_nodes(self.nodes)
        self.stationC.set_nodes(self.nodes)
        self.stationB.start()
        self.stationA.start()
        self.stationC.start()
        time.sleep(1)
        self.stationA.set_node_path(b"PPSTA3", [b"PPSTA2", b"PPSTA3"])
        self.stationC.set_node_path(b"PPSTA1", [b"PPSTA2", b"PPSTA1"])
        # self.stationA.pather.request_path(b"PPSTA3")
        time.sleep(1)
        dataerC = PPNet()
        dataerC.set_underlayer(self.stationC)
        dataerA = PPNet()
        dataerA.set_underlayer(self.stationA)
        dataerC.send(b"testdata", self.addrA)
        data, addr = dataerA.receive(5)
        time.sleep(2)
        self.assertEqual(data, b"testdata", "Test Dataer")
        self.assertEqual(addr, self.addrC, "Test Dataer")
        dataerA.quit()
        dataerC.quit()
        self.stationB.quit()

    def testDataNode(self):
        datanodeA = PPNetNode(config=self.nodeinfoA)
        datanodeB = PPNetNode(config=self.nodeinfoB)
        self.assertTrue(True, "test datanode. ")




if __name__ == '__main__':
    unittest.main()
