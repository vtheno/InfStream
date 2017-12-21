#coding=utf-8
class Stream(object):
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
        while n:
            yield self.first
            self = self.compute()
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

    def take_computed_g(self):
        while self.computed:
            yield self.first
            self = self.rest

def Inf(fn,start):
    #def compute():
        #yield Inf(fn,fn(start))
    #    return Inf(fn,fn(start))
    #return Stream(start,compute)
    return Stream(start,lambda:Inf(fn,fn(start)))

a = Inf(lambda x:x+1,0)
print( a.get(4) )
print( a.get(0) )
print( a.take_computed() )
print( [i for i in a.take_computed_g() ] )

#import time
#t1 = time.clock()
#a.take(2000000)
#print( time.clock()-t1 )
#t2 = time.clock()
#list(range(2000000))
#print( time.clock()-t2 )
import timeit
t1 = timeit.Timer('[i for i in range(200)]')
t2 = timeit.Timer('[i for i in a.getG(200)]','from __main__ import a')
print( t1.timeit() )
print( t2.timeit() )
