def print1(): print('yo fiddle 1 ')

class A():
    def __init__(self, param):
        self.Aval=666
        self.pval = param

    def aFunc(self):
        print("A", self)


class B(A):
    def __init__(self):
        super().__init__(333)
        self.bval = 222
