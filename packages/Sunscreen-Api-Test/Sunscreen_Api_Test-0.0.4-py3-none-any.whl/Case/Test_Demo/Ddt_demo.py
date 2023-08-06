# coding=utf-8
import json
import unittest
import ddt
@ddt.ddt
class TestCase(unittest.TestCase):
    def setUp(self):
        print('测试开始')
    def tearDown(self):
        print('测试结束')

    @ddt.file_data('E://AutomationApiTest//Data//test')
    def test_01(self,value):
        print(eval(value))
if __name__ == '__main__':
    unittest.main()
