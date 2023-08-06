# coding=utf-8
import json
import random
import unittest
import string

from Driver.DoMysql import DoMysql
from Driver.base_request import request
from Driver.GenPass import GenPass
from Driver.handle_excle import handle
from Driver.handle_init import handle_ini
from Driver.hashlib_md5 import md5_hb
from Data.Headers.headers_data import *
class JcxApi(unittest.TestCase):
    def setUp(self):
        print('测试开始')
        rootpath = handle_ini.get_value('uat')
        self.url = rootpath+"/user/warrant"

    def tearDown(self):
        print('测试结束')

    def test_01_warrant(self):
        res = request.run_main('get',url=self.url,headers=headers_warrant)
        json_res = res
        print(json.dumps(json_res, indent=2, ensure_ascii=False))
        mysql = DoMysql()
        sql = 'SELECT m_id from qy_members_account WHERE ma_mobile = 13577777777'
        result=mysql.fetchAll(sql)
        print(result[0]['m_id'])
if __name__ == '__main__':
    unittest.main()