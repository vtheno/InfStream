#coding=utf-8
class Stream(object):
    __slots__ = ['first','compute_func','computed','rest']
    def __repr__(self):
        if not self.computed:
            return "Stream({},<compute_func>)".format(self.first)
        return "Stream({},{})".format(self.first,self.rest)
    def __init__(self,first,compute_func):
        self.first = first
        self.compute_func = compute_func
        self.computed = 0
        self.rest     = None
    def compute(self):
        if not self.computed:
            # not false is True then calc
            self.rest = self.compute_func()#next(self.compute_func)
            self.computed = 1
        return self.rest

    def get(self,n):
        # force <=> self = self.compute()
        while n:
            self = self.compute()
            n    -= 1
        else:
            return self.first

    def getG(self,n):
        self.get(n)
        while n:
            yield self.first
            self = self.rest#self.compute()
            n -=1 

    def take_computed(self):
        temp = [ ]
        while self.computed:
            temp += [self.first]
            self = self.rest
        else:
            return temp

    def take(self,n):
        temp = self.take_computed()
        if n < len(temp):
            return temp[0:n]
        else:
            self.get(n)
            return self.take_computed()

    #def take_computed_g(self):
    #    while self.computed:
    #        yield self.first
    #        self = self.rest

def Inf(fn,start):
    #def compute():
        #yield Inf(fn,fn(start))
    #    return Inf(fn,fn(start))
    #return Stream(start,compute)
    return Stream(start,lambda:Inf(fn,fn(start)))

a = Inf(lambda x:x+1,0)
print( list(a.getG(20)) is list(a.getG(20)))

import timeit
def testG(n):
    now = 0
    while n:
        yield now
        now +=1
        n-=1


# 1 s = 1k ms
# 1 ms = 1k us
# 1 us = 1k ns

c  = 100000#0
#t1 = timeit.Timer('list( range(c) )','from __main__ import c')
#t2 = timeit.Timer('list( testG(c) )','from __main__ import testG,c')
#t3 = timeit.Timer('list( a.getG(c) )','from __main__ import a,c')
t1 = timeit.Timer('[i for i in range(c) ]','from __main__ import c')
t2 = timeit.Timer('[i for i in testG(c) ]','from __main__ import testG,c')
t3 = timeit.Timer('[i for i in a.getG(c) ]','from __main__ import a,c')
t  = 10#000
print( t1.timeit(t) )
print( t3.timeit(t) )
print( t2.timeit(t) )

