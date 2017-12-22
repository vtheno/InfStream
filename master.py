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
            #if not self.computed:
            # not false is True then calc
            #    self.rest = self.compute_func()#next(self.compute_func)
            #    self.computed = 1
            self = self.compute()#self.rest
            n    -= 1
        else:
            return self.first

    def getG(self,n):
        self.get(n)
        while n:
            yield self.first
            self = self.rest
            #self = self.compute()
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
    def compute_Inf():
        #yield Inf(fn,fn(start))
        return Inf(fn,fn(start))
    #return Stream(start,lambda:Inf(fn,fn(start)))
    return Stream(start,compute_Inf)



def add1(x):
    return x+1

a = Inf(add1,0)
print('a:', a.get(2) )
#print('g:', get(a,4) )
#print('old', a )
#a = get(a,4)
#print('new', a )
class WeGet(object):
    def __init__(self,obj):
        self.obj = obj
        self.count_n = 0
        self.history = { }
        self.take_history = { }
    def _get(self,stream,n):
        #print('get:',stream,'n:',n)
        while n:
            self.history[self.count_n] = stream.first
            self.count_n += 1
            # 这个过程 不会重复 
            stream = stream.compute()
            n-=1
            
        else:
            return stream
    def get(self,n):

        if self.count_n == 0:
            self.obj = self._get(self.obj,n)
            return self.obj
        while (n - self.count_n) > 0:
            self.obj = self._get(self.obj, (n - self.count_n) + 1)
            #print( self.count_n ,self.history)
        else:
            return self.history[n]

    def take(self,n):
        #print( self.count_n,self.obj,self.history,self.take_history )
        if n > self.count_n:
            self.get(n)
        if n not in self.take_history.keys() :
            temp = [ ]
            count = 0
            while count < n:
                temp += [ self.history[count] ]
                count += 1
            self.take_history[n] = temp
        return self.take_history[n]
c = WeGet(a)
#print('before:', a, '|',c.obj)
#print( c.history,c.count_n )
#print( c.get(5) )
#print('after:', a, '|',c.obj)
#print( c.history,c.count_n )
#print( c.take(20) )
import timeit
t1 = timeit.Timer('range(100000)')
t2 = timeit.Timer('c.take(100000)','from __main__ import c')
t  = 1000000
print( t1.timeit(t) )
print( t2.timeit(t) )
#print( list(a.getG(20)) is list(a.getG(20)))
#c = a.take(20)#a.getG(20) 
#print( list(c) )
# not define a then ,不包括定义 a 
# Stream __init__ call count 20
# Inf call count 20 
# Inf.compute_Inf count 20
# Add1 count 20
# getG count 20
# compute count 20
#print( [i for i in a.getG(20) ] ) eq up line
#print( a.take(20) )
#import timeit
#def testG(n):
#    now = 0
#    while n:
#        yield now
#        now +=1
#        n-=1

# 1 s = 1k ms
# 1 ms = 1k us
# 1 us = 1k ns

#c  = 100000#00
#t1 = timeit.Timer('list( range(c) )','from __main__ import c')
#t2 = timeit.Timer('list( testG(c) )','from __main__ import testG,c')
#t3 = timeit.Timer('list( a.getG(c) )','from __main__ import a,c')
#t1 = timeit.Timer('[i for i in range(c) ]','from __main__ import c')
#t2 = timeit.Timer('[i for i in testG(c) ]','from __main__ import testG,c')
#t3 = timeit.Timer('[i for i in a.getG(c) ]','from __main__ import a,c')
#t3  = timeit.Timer('[i for i in a.take(c) ]','from __main__ import a,c')
#t  = 10#0#0#00
#print( t1.timeit(t) )
#print( t2.timeit(t) )
#print( t3.timeit(t) )

