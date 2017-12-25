#coding=utf-8
class Generator(object):
    def __init__(self, init_func, init_val):
        self.init_func = init_func
        self.init_val = init_val
    def iter(self):
        now = self.init_val
        while 1:
            yield now
            now = self.init_func(now)
    def __iter__(self):
        return self.iter()
def myrange(size):
    return [0]*size

def head(n,stream):
    #print stream.init_func,stream.init_val
    #temp = Generator(stream.init_func,stream.init_val)
    #temp.iter = stream.iter
    # def compose(f,g):
    #def comp(x):
    #    return g(f(x))
    #return comp
    #[i for i,_ in zip(stream,[0]*n)]
    return [i for i,_ in  zip(stream,[0]*n) ]

def takes(n,t,stream):
    tmp = head(t,stream)
    [tmp.remove(i) for i in head(n,stream)]
    return tmp

def get(n,stream):
    t = head(n,stream)
    while t:
        return t[-1]
    return t

def Map(f,stream):
    temp = Generator(stream.init_func,stream.init_val)
    temp.iter = stream.iter
    def mapc():
        #for i in stream:
        #print( 'mapc:',i )
        [(yield f(i)) for i in stream]
    temp.iter = mapc
    return temp

def Filter(f,stream):
    temp = Generator(stream.init_func,stream.init_val)
    temp.iter = stream.iter
    def filc():
        #[f(i) and (yield i)  for i in stream]
        [(yield i) for i in stream if f(i)]
    temp.iter = filc
    return temp

def Reduce(f,stream,init):
    temp = Generator(stream.init_func,stream.init_val)
    temp.iter = stream.iter
    tmp_init = [init]
    def redu():
        init = tmp_init[0]
        for i in stream:
            r = f(init,i)
            init = r
            yield r
    temp.iter = redu
    return temp

g = Generator(lambda a:a + 1,0)
print( g.init_func,g.init_val)
print( dir(g) )
f = Map(lambda x:x * 2,g)
h = Map(lambda x:x*x,f)
#print ( vars(f) ,f.init_func ,f.init_val)
print ( [i for i,_ in zip(g,[0]*4)] )
print ( [i for i,_ in zip(f,[0]*4)] )
print ( [i for i,_ in zip(h,[0]*4)] )
print ( [i for i,_ in zip(g,[0]*4)] )
print ('h:',head(4,h))
print ("takes:",takes(2,4,f))
print ("takes:",takes(2,4,h))
print ("head: ",head(12,h) )
print ("takes:",takes(0,12,h))
print ("get:  ",get(10,h) )
c = Reduce(lambda a,b:(a,b),g,-1)
print( 'c:',head(5,c))
print( 'c:',get( 100 ,c) )

#t1 = timeit.Timer('[i for i,_ in zip(c,myrange(100))]','from __main__ import h as c,myrange')
#print(t1.timeit())
#t2 = timeit.Timer('[i for i,_ in zip(c,range(100))]','from __main__ import h as c')
#print(t2.timeit())
#print( head(100,h) )
negInt = Generator(lambda x:x-1,0)
print( head(100,negInt) )

import timeit
t1 = timeit.Timer("range(100)")
t2 = timeit.Timer("head(100,g)",'from __main__ import head,g')
print( t1.timeit() ,t2.timeit() )
