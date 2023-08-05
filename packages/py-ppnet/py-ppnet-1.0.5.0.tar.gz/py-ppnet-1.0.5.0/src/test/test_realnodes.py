import time
import unittest
import logging
from ppnet.common import set_debug, Log
from ppnet.config import NAT_TYPE, PP_APPID
from ppnet.ppbeater import Beater
from ppnet.ppl2node import PPMessage
from ppnet.ppl3node import PPL3Node
from ppnet.ppl4node import PPNet, PPNetNode
from test.mocknet import MockNet

set_debug(logging.DEBUG)
nodeA = PPNetNode()
nodeB = PPNetNode(node_port=54321)
nodeA.start()
nodeB.start()

class Test(unittest.TestCase):

    def start(self):
        pass

    def setUp(self):
        self.start()
        pass

    def tearDown(self):

        pass


    def test_id(self,i=0):
        nodeA.set_peer(("127.0.0.1",54321))
        time.sleep(1)
        self.assertTrue(nodeA.underlayer.has_id, "test id.")
        self.assertTrue(nodeB.underlayer.has_id, "test id.")



if __name__ == '__main__':
    unittest.main()
