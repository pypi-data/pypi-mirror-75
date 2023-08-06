# coding=utf-8
import json
import random
import unittest
import string
from Driver.base_request import request
from Driver.GenPass import GenPass
from Driver.handle_excle import handle
from Driver.handle_init import handle_ini
from Driver.hashlib_md5 import md5_hb


class Znjj(unittest.TestCase):
    def setUp(self):
        print('测试开始')
        rootpath = handle_ini.get_value('rootpath')
        self.url = rootpath + "Data\case_01.xlsx"
        self.register_url =  "/user/register"
        self.login =  "/user/login"
        self.addFamily = "/family/addFamily"
    @classmethod
    def setUpClass(cls):
        globals()["token"]=None

    def tearDown(self):
        print('测试结束')

    def test_1_test_login(self):
        rows = handle.get_rows()
        for i in range(rows):
            data = handle.get_rows_value(i + 2)
            is_run = data[2]
            if is_run == 'yes':
                method = data[6]
                log_url = data[5]
                json1 = eval(data[7])
                headers = eval(data[9])  # 字符串转化字典类型
                res = request.run_main(method, url=log_url, headers=headers, json=json1)
                json_res = res
                print(json.dumps(json_res, indent=2, ensure_ascii=False))
                message=json_res["description"]
                try:
                    self.assertEqual(message, " 登陆成功")
                    handle.excel_write_data(i+2, 15, "测试通过")
                except Exception as e:
                    handle.excel_write_data(i+2, 15, "测试失败")
                    raise e

    def test_2_register(self):
        global user
        user = random.randint(6, 999999)
        play = GenPass()
        pwd = md5_hb(play).Hashlib_md5()
        json1 = {
            "userAccount": user,
            "userPassword": pwd
        }
        headers = {
            "Content-Type": "application/json"
        }
        res = request.run_main('post', url=self.register_url, headers=headers, json=json1)
        json_res = res
        register = json_res["description"]
        if register == " 注册成功":
            register = json_res["description"]
        else:
            register = "注册失败,请重新注册"
        print(json.dumps(json_res, indent=2, ensure_ascii=False))
        array = [user, pwd, register]
        handle.write_cell_content(array)
        print("账号: "+ str(user))
        print("密码：" + str(pwd))
    def test_3_login(self):
        headers = {
            "Content-Type": "application/json"
        }
        index = 1
        rows = handle.get_rows(index)
        for i in range(rows):
            data = handle.get_rows_value( i + 2, index)
            userAccount = data[0]
            if userAccount == user:
                userPassword = data[1]
                json1 = {
                    "userAccount": userAccount,
                    "userPassword": userPassword
                }
                res = request.run_main('post', url=self.login, headers=headers, json=json1)
                json_res = res
                globals()["token"]=json_res["data"]["token"]
                print(json.dumps(json_res, indent=2, ensure_ascii=False))
                self.assertEqual(json_res["description"], " 登陆成功", msg="登陆失败")

    def test_4_addFamily(self):
        val = ''.join(random.sample(string.ascii_letters + string.digits, 60))
        headers = {
            "token":globals()["token"]
        }
        data = {
            'familyName':'{}号家庭'.format(random.randint(6, 999999)),
            'familyDescribe':val,
            'file':'//img.mukewang.com/5de711c50951202612000676.jpg'
        }
        print("备注："+val)
        res = request.run_main('post', url=self.addFamily, data=data, headers=headers)
        json_res = res
        print(json.dumps(json_res, indent=2, ensure_ascii=False))
        self.assertEqual(json_res["description"], " 操作成功", msg="操作失败")

if __name__ == "__main__":
    unittest.main()

