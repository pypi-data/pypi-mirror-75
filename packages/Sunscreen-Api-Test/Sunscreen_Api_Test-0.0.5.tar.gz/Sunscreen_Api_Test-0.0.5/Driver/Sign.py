#python实现sign签名
import hashlib,time
class sign:
    def get_str(self,apikey,body):
        # 列表生成式，生成key=value格式
        a=["".join(i) for i in body.items() if i[1] and i[0] != "sign"]
        # 参数名ASCII码从小到大排序
        b="".join(sorted(a))
        # 在b后面拼接上apikey
        c= b+apikey
        # 将字符串转换为小写字符串
        d=c.lower()
        return d
    def get_md5(self,st):
        md5=hashlib.md5()
        md5.update(st.encode('UTF-8'))
        m=md5.hexdigest()
        return m
    def get_sign(self,apikey,body):
        s=sign()
        st=s.get_str(apikey,body)
        m=s.get_md5(st)
        body['sign']=m
        return body
if __name__ == '__main__':
    # 验证密钥，由开发提供
    apikey="qyoiqyshopuqoij605-Losoh+p0112h2"
    body={
        'pic':'WyJodHRwOi8vcWluaXUtdWF0LnlqZGZtYWxsLmNvbS8lMkZQdWJsaWMlMkZVcGxvYWRzJTJGamN4c2hvcGtleSUyRmltYWdlcyUyRjIwMjAwNzI1JTJGNTUwOTU1NzE1Mi5wbmc/aW1hZ2VWaWV3Mi8wL3cvMzI0L2gvMzI0Il0=',
        'price':'313',
        'type':'1',
        'mId':'45971',
        'method':'qy.Sure.Confirm.Recharge',
        'token':'MTU5NTU3NzMzNjo0NTk3MTo0NTk3MTVmMWE5M2Y4ODE0OGM=',
        'timeZone':'QXNpYS9TaGFuZ2hhaQ==',
        'timestamp':'2020-07-25 13:54:51',
        'v':'wap:0.0.2',
        'source':'wap',
        'format':'json',
        'sign':''
    }
    bb=sign().get_sign(apikey,body)
    print(bb['sign'].upper())