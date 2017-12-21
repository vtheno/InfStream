#coding=utf-8
class Generator(object):
    def __init__(self,init_func,init_val):
        self.init_func = init_func
        self.init_val  = init_val
        self.old_init_val = init_val
        self.history      = [ ]
        self.take_history = {}
        self.length       = 0
    def get(self,n):
        while n >= self.length:
            print self.history,self.length
            self.calc()
        else:
            return self.history[n]
    def take(self,n):
        while n>= self.length:
            print self.history,self.take_history
            self.calc()
        else:
            if not self.take_history.has_key(n):
                self.take_history[n] = self.history[0:n]
            return self.take_history[n]
    def calc(self):
        self.history  += [ self.init_val ]
        self.length   += 1
        self.init_val = self.init_func(self.init_val)



g = Generator(lambda x:x+1,0)
print g.take(2) , g.take(2)
print g.take(2) == g.take(2)
print g.take(2) is g.take(2)
