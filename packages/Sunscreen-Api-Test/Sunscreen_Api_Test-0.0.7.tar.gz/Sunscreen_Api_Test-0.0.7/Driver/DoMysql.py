#引入pymysql模块
import pymysql

class DoMysql:
    #初始化
    def __init__(self,db1):
        self.db=db1
        #创建连接
        self.conn = pymysql.Connect(
          host = 'rm-uf67pz747a40ct135to.mysql.rds.aliyuncs.com',
          port = 3306,
          user = 'yjdf_mall',
          password = 'o1r8sFcfNaQTlBnl',
          db = self.db,
          charset = 'utf8',
          cursorclass = pymysql.cursors.DictCursor  #以字典的形式返回数据
        )
        #获取游标
        self.cursor = self.conn.cursor()

    #返回多条数据
    def fetchAll(self,sql):
        self.cursor.execute(sql)
        return self.cursor.fetchall()

    #插入一条数据
    def insert_one(self,sql):
        result = self.cursor.execute(sql)
        self.conn.commit()
        return result

    #插入多条数据
    def insert_many(self,sql,datas):
        result = self.cursor.executemany(sql,datas)
        self.conn.commit()
        return result

    #更新数据
    def update(self,sql):
        result = self.cursor.execute(sql)
        self.conn.commit()
        return result

    #关闭连接
    def close(self):
        self.cursor.close()
        self.conn.close()


db = DoMysql("yjdf_mall_orders")

if __name__ == '__main__':
    mysql  = DoMysql()
    #插入一条数据
    sql = 'insert into `user`(`mobile`,`passwd`) values("13100010000","123456")'
    result = mysql.insert_one(sql)
    print(result) #返回插入数据的条数(1)

    #插入多条数据
    datas = [
        ("13100010001","111111"),
        ("13100010002","666666")
    ]
    sql = 'insert into `user`(`mobile`,`passwd`) values(%s,%s)'
    result = mysql.insert_many(sql,datas)
    print(result) #返回插入数据的条数(2)

    #查询数据
    sql = 'select * from user'
    result = mysql.fetchAll(sql) #返回列表,如果多条数据，列表中嵌套字典
    for item in result:
        print(item.get('mobile')) #循环列表，输出mobile值

    #关闭连接
    mysql.close()