dictnum ={'零':0,'一':1,'二':2,'三':3,'四':4,'五':5,'六':6,'七':7,'八':8,'九':9,'十':10,'百':12,'千':13,'万':14,'亿':18,'两':2
          }
def getResultForDigit(a):
    count = len(a)-1
    result = 0
    tmp = 0

    while count >= 0:
        tmpChr = a[count:count+1]
        tmpNum = 0
        if tmpChr.isdigit():#防止大写数字中夹杂阿拉伯字母
            tmpNum=int(tmpChr)
        else:
            tmpNum = dictnum[tmpChr]
        if tmpNum >10:#获取0的个数
            tmp=tmpNum-10
        #如果是个位数
        else:
            if tmp == 0:
                result+=tmpNum
            else:
                result+=pow(10,tmp)*tmpNum
            tmp = tmp+1
        count = count - 1
    return result
aa = getResultForDigit("四百二十二")
print(aa)