# coding=utf-8
import requests
from .handle_init import handle_ini


class BaseRequest:
    def send_post(self, url,**kwargs):
        params = kwargs.get("params")
        data = kwargs.get("data")
        json = kwargs.get("json")
        headers= kwargs.get("headers")
        try:
            res = requests.post(url,params=params, data=data,json=json, headers=headers).json()
            return res
        except Exception as e:
            print("post请求错误： %s" %e)

    def send_get(self,url, **kwargs):
        params = kwargs.get("params")
        headers = kwargs.get("headers")
        try:
            res = requests.get(url ,params=params,headers=headers).json()
            return res
        except Exception as e:
            print("get请求错误： %s" %e)

    def run_main(self, method,url, **kwargs):
        base_url = handle_ini.get_value('host')
        if 'http' not in url:
            url = base_url+url
            print(url)
        if method == 'get':
            res = self.send_get(url,**kwargs)

        else:
            res = self.send_post(url,**kwargs)
        return res




request = BaseRequest()
if __name__ == '__main__':
    request =BaseRequest()
    url = "/family/addFamily"
    json1 = {
	    "familyName":"东北大家庭",
	    "familyDescribe":"哈哈哈家庭哈哈哈家庭哈哈哈家庭哈哈哈家庭哈哈哈家庭哈哈哈家庭哈哈哈家庭"
    }
    headers = {
        "token": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJhdWQiOlsiMDkwMyIsIjE1ODc2OTExNTM5NjEiXX0.hq9oWYxmBoDZH3dKuWC5ZLNNCpkQuk--ZzpqqEP2XvA"
    }
    res = request.run_main('post',url,data=json1,headers=headers)
    print(res)