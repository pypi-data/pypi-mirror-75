# coding=utf-8
import json
import unittest
from Driver.base_request import request
from Driver.handle_excle import handle
from Driver.handle_init import handle_ini
import ddt
data = handle.get_excel_data()
@ddt.ddt
class TestRunMain(unittest.TestCase):
    @ddt.data(*data)
    def testrun_case(self,data):
        #获取mock全部数据

        # rows = handle.get_rows()
        # for i in range(rows):
        #     data = handle.get_rows_value(i + 2)
        cookie = None
        get_cookie = None
        header = None
        is_run = data[2]
        if is_run =='yes':
            method = data[6]
            log_url = data[5]
            json1 =eval(data[7])
            headers = eval(data[9])
            res=request.run_main(method, url=log_url, headers=headers, json=json1)
            json_res = res
            print(json.dumps(json_res, indent=2, ensure_ascii=False))

if __name__=="__main__":
    run = TestRunMain()
    run.testrun_case()
