import time
import random
def get_birthday():
    start_birthday = (1970,10,10,1,10,10,10,10,10)    #设置开始时间元组
    end_birthday = (2020,5,5,10,10,10,10,10,10)      #设置结束时间元组
    start = time.mktime(start_birthday)        #生成开始时间戳
    end = time.mktime(end_birthday)            #生成结束时间戳
    for i in range(1):
        s = random.randint(start,end)          #选择一个开始时间和结束时间
        date_touole = time.localtime(s)        #将时间生成元组
        date = time.strftime("%Y%m%d",date_touole)  #时间元组转换成格式化字符串
    return date
