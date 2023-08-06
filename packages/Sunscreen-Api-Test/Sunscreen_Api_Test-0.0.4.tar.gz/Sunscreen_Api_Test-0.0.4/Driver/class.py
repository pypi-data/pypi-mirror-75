
class Student:
    name = 1
    age = 0
    def __init__(self,name):
        self.name = name
        self.score = 0

    def marking(self,score):#加入双下划线设置为私有
        if score < 0:
            return "分数不能为负数"
        self.score = score
        print(self.name + '同学本次考试分数为：'+str(self.score)+ '分')

    def print_file(self):
        print('name: ' + self.name)
        print(self.__class__.name)
    @classmethod #类方法
    def plus_sum(cls):
        cls.name +=1
        print(cls.name)

    @staticmethod #静态方法
    def add(x,y):
        print("this is a static method")

Student.plus_sum()