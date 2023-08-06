import random, string  # 调用random、string模块


def GenPass():
    src_digits = string.digits  # string_数字  '0123456789'
    src_uppercase = string.ascii_uppercase  # string_大写字母 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
    src_lowercase = string.ascii_lowercase  # string_小写字母 'abcdefghijklmnopqrstuvwxyz'
    src_special = string.punctuation  # string_特殊字符 '!"#$%&\'()*+,-./:;<=>?@[\\]^_`{|}~'

    # sample从序列中选择n个随机独立的元素，返回列表
    num = random.sample(src_digits, 1)  # 随机取1位数字
    lower = random.sample(src_uppercase, 1)  # 随机取1位小写字母
    upper = random.sample(src_lowercase, 1)  # 随机取1位大写字母
    special = random.sample(src_special, 1)  # 随机取1位大写字母特殊字符
    other = random.sample(string.ascii_letters + string.digits + string.punctuation, 4)  # 随机取4位
    # 生成字符串
    # print(num, lower, upper, special, other)
    pwd_list = num + lower + upper + special + other
    # shuffle将一个序列中的元素随机打乱，打乱字符串
    random.shuffle(pwd_list)
    # 列表转字符串
    password_str = ''.join(pwd_list)
    return password_str


GenPass()

