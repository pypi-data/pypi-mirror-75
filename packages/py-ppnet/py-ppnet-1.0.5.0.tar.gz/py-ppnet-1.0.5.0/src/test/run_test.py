'''
Created on 2018年5月22日

@author: heguofeng
'''
import unittest

from test.test_ppnetnode import TestL3
from test.test_ppl2node import TestL2
from test.test_ppmessage import TestMessage

def suite():  # 创建测试添加测试套件函数
    suite=unittest.TestSuite()  #  创建测试套件
    suite.addTest(TestL3('testBeat'))  # 添加测试用例
    suite.addTest(TestL3('testBeatnull'))  # 向套件中添加用例
    suite.addTest(TestL3('testPath'))
    suite.addTest(TestL3('testData'))
    suite.addTest(TestL3('testDataNode'))
    suite.addTest(TestL2('testL2Node'))
    suite.addTest(TestL2('testAckor'))
    suite.addTest(TestMessage('test_PPMessage'))
    suite.addTest(TestMessage('test_AppMessage'))
    suite.addTest(TestMessage('test_BeatMessage'))

    return suite



if __name__ == "__main__":
    # suite = unittest.TestLoader().discover("test", "test_*.py" )
    suite = suite()
    unittest.TextTestRunner(verbosity=2).run(suite)