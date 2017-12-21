#coding=utf-8
class Generator(object):
    def __init__(self,init_func,init_val):
        self.init_func = init_func
        self.init_val  = init_val
        self.old_init_val = init_val
        self.history      = [ ]
        self.take_history = {}
        self.length       = 0
        self.compose_flag = 0
        self.compose_funcs= [ ]
    def get(self,n):
        while n >= self.length:
            #print self.history,self.length
            self.calc()
        else:
            return self.history[n]
    def take(self,n):
        while n>= self.length:
            #print self.history,self.take_history
            self.calc()
        else:
            if not self.take_history.has_key(n):
                self.take_history[n] = self.history[0:n]
            return self.take_history[n]

    def calc(self):
        self.history  += [ self.init_val ]
        self.length   += 1
        self.init_val = self.init_func(self.init_val)
        # compose flag is 1 then compose_funcs 
        if self.compose_flag:
            # compose init
            self.compose()

    def compose(self):
        for fn in self.compose_funcs:
            self.init_val = fn(self.init_val)

g = Generator(lambda x:x+1,0)
print g.take(2) , g.take(2)
print g.take(2) == g.take(2)
print g.take(2) is g.take(2)
print map(lambda x:x*2,g.take(2) )
def show(stream):
    print '----------start'
    print 'init_val:',stream.init_val
    print 'old_ val:',stream.old_init_val
    print 'history :',stream.history
    print 'take_history :',stream.take_history
    print 'compose:',stream.compose_flag
    print 'compose:',stream.compose_funcs
    print '----------end'
def Map(func,stream):
    # not copy history  
    temp = Generator(stream.init_func,stream.old_init_val)
    temp.compose_flag = stream.compose_flag
    temp.compose_funcs= stream.compose_funcs
    temp.compose_flag = 1
    temp.compose_funcs.append( func )
    return temp
temp =  Map(lambda x:x*2,g)
show( temp )
print temp.take(2)
t2   =  Map(lambda x:x*2,g)
show(t2)
print t2.take(2) is t2.take(2)
show(t2)
#import timeit
#t1 = timeit.Timer('range(100)')
#t2 = timeit.Timer('g.take(100)','from __main__ import g')
#t  = 1000000000
#print t2.timeit(t) , t1.timeit(t) 
