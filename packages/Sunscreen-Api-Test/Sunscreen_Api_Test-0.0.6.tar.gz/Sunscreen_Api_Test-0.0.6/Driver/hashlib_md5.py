import hashlib
class Md5:
    def __init__(self,new_par):
        self.par = new_par

    def Hashlib_md5(self):
        parameter_md5 = self.par
        md5 = hashlib.md5()
        md5.update(parameter_md5.encode("utf-8"))
        parameter = md5.hexdigest()
        return parameter
md5_hb = Md5





