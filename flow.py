#coding=utf-8
class Stream(object):
    __slots__ = ['empty','first','length',
                 '_compute_rest','_rest','_computed','take_history','history']
    def __repr__(self):
        if self.empty:
            return "<Empty Stream>"
        return 'Stream({0},<compute_rest>)'.format(repr(self.first))
    def __init__(self,first,compute_rest,empty=False):
        self.first = first
        self._compute_rest = compute_rest
        self.empty = empty
        self._rest = None
        self._computed = False
        self.history   = [ ]
        self.length    = 0
        self.take_history = {}
    @property
    def rest(self):
        #assert not self.empty,'Empty Streams have no rest.'
        if not self._computed:
            self._rest = self._compute_rest()
            self._computed = True
        return self._rest

    def get(self,n):
        temp = self #Stream(self.first,self._compute_rest) 
        # 这里是 引用 赋值 相当于 是由于命名的关系
        while n >= temp.length:
            temp.history += [self.first]
            temp.length  += 1
            self = self.rest
        else:
            return temp.history[n]

    def take(self,n):
        while n>= self.length:
            self.get(n)
        else:
            if n not in self.take_history.keys():#self.take_history.has_key(n):
                self.take_history[n] = self.history[0:n]
            return self.take_history.get(n)

def make_inf(fn,start):
    def compute_rest():
        return make_inf(fn,fn(start))
    return Stream(start,compute_rest)

def map_stream(fn,s):
    if s.empty:
        return s
    def compute_rest():
        return map_stream(fn,s.rest)
    return Stream(fn(s.first),compute_rest)

def filter_stream(fn,s):
    if s.empty:
        return s
    def compute_rest():
        return filter_stream(fn,s.rest)
    if fn(s.first):
        return Stream(s.first,compute_rest)
    return compute_rest()

def foldr(fn,end,s):
    if s.empty:
        return end
    def compute_rest():
        return foldr(fn,fn(s.first,end),s.rest)
    return Stream(fn(s.first,end),compute_rest)

def foldl(fn,accum,s):
    if s.empty:
        return accum
    def compute_rest():
        return foldl(fn,fn(accum,s.first),s.rest)
    return Stream(fn(accum,s.first),compute_rest)

reduce_stream = foldr

test = Stream(1,lambda :2)
print( test.rest )
print( test._computed )
def add(x):
    return x+1
s = make_inf(add,0)
#print( s.take(200) is s.take(200) )
#print( 'computed:',s.rest._computed )
#f = map_stream(lambda x:x*2,s)
#g = s.take(200)
#print( g is s.take(200) )
import timeit
t1 = timeit.Timer('sum(range(100))')#'range(100)')
t2 = timeit.Timer('sum(s.take(100))','from __main__ import s')
print( t1.timeit(),t2.timeit() )
print( s.get(3) )
