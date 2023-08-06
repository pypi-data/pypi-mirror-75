# coding=utf-8
import json
import random
import time
import unittest
import string
from Driver.base_request import request
from Driver.GenPass import GenPass
from Driver.handle_excle import handle
from Driver.handle_init import handle_ini
from Driver.hashlib_md5 import md5_hb
class UpDownStuff():
    base_url = handle_ini.get_value('updownstuff_host')
    List_url = base_url + '/list'
    selectCamera_url = base_url + '/selectCamera'
    closeStream_url = base_url +'/closeStream'
    setIpConfig_url = base_url + '/setIpConfig'
    startToGrab_url = base_url + '/startToGrab'
    detail_url = base_url + '/detail'
    def getCameraList(self):
        res = request.run_main('get',self.List_url)
        res  = res['data'][0]['uuid']
        print('uuid:'+res)
        return res
    def closeStream(self,uuid):
        json = { "uuid": uuid }
        res = request.run_main('post',self.closeStream_url,json=json)
        print(res)
    def SelectCamera(self,uuid):
        json = {
            "uuid":uuid,
            "control-mode":"exclusive"
        }
        res =request.run_main('post',self.selectCamera_url,json=json)
        print(res)
        status = res['status']
        if status == False:
            time.sleep(2)
            self.closeStream(uuid)
            res1 = request.run_main('post',self.selectCamera_url,json=json)
            if res1['status'] == True:
                print('selectCamera操作成功1')
            else:
                    print(res1)
        else:
            print('selectCamera操作成功2')
    # def setIpConfig(self,uuid):
    #     json = {
    #         "uuid": uuid,
    #         "config": "static"
    #     }
    #     res = request.run_main('post', self.setIpConfig_url, json=json)
    #     print('setIpConfig: ',str(res))
    def startToGrab(self,uuid):
        json = {
            "uuid":uuid,
	        "rgb":False
        }
        res = request.run_main('post', self.startToGrab_url, json=json)
        if res['status'] == True:
            print('startToGrab操作成功')
        else:
            print(res)
    def detail(self,uuid):
        json1 = { "uuid": uuid}
        res = request.run_main('post', self.detail_url, json=json1)
        if res['status'] == True:
            print('detail操作成功')
        else:
            print(res)
        print(json.dumps(res, indent=2, ensure_ascii=False))

    def Go(self):
       uuid =  self.getCameraList()
       self.SelectCamera(uuid)
       # self.setIpConfig(uuid)
       self.startToGrab(uuid)
       self.detail(uuid)
if __name__ == '__main__':
    updown = UpDownStuff()
    updown.Go()

