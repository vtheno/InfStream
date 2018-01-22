#coding=utf-8
"""
this is nothing 
class MyRange(object):
    def __init__(self,start,end=None,step=1):
        self.start = start
        self.step  = step
        self.end   = end
    def __iter__(self):
        now = self.start
        while 1:
            yield now
            now += self.step
            if now == self.end:
                break

def unlist(lst):
    if lst == [ ]:
        return ()
    else:
        return (lst[0],lst[1:])
def Zip(inp1,inp2):
    if inp1 == [] or inp2 == []:
        return [ ]
    else:
        # x,*xs = inp1 # py3
        # c,*cs = inp2
        x,xs = unlist(inp1)
        c,cs = unlist(inp2)
        return [(x,c)] + Zip(xs,cs)
def unZip(zips):
    if zips == []:
        return [] , [] 
    else:
        x,xs = unlist(zips)
        return [x[0]] + unZip(xs)[0], [x[1]]+unZip(xs)[1] 

def Box(*args):
    return args
temp = list(zip(MyRange(0),MyRange(0,4)))
print( temp )
print( unZip(temp) )
#print Zip(MyRange(0),MyRange(0,4))
# x for x in (1,) <=> x where x = 1
def x():
    for i in MyRange(0):
        if i%2 == 0:
            yield i
# zip([ x for x in MyRange(0) if x%2==0 ],range(4))
print( [i for k,i in zip(MyRange(0,4) , x()) ] )
#func c | c > 0 = "c>0"
#       | otherwise = "other"
func = lambda c: (lambda flag : "c>0" if flag else flag)(c > 0) or (lambda otherwise: "other")(c) 
print( func(0) )
def warp(func):
    # this func is tuple lambda (a,b)
    a,b = func
    def compute(inp):
        r1 = a(inp)
        if r1 !=None:
            return r1
        else:
            return b(inp)
    return compute

# length [] = 0
# length (x:xs) = 1 + length xs
length1 = (
    (lambda _   : 0 if _==[] else None ) ,
    (lambda lst : 1 + length1(lst[1:]) ) )
length1 = warp(length1)
#print( length1( range(941) ) ) # pypy
#print( length1( list(range(498) ) ) ) # py3
#print( length1( range(498) ) ) # py2
def makefunc(*funcs):
    def delay(*args,**kw):
        for fn in funcs:
            r = fn(*args,**kw)
            if r != None :
                return r
        return None
    return delay
def l1(_):
    if _ == [ ] : return 0
def l2(xxs):
    return 1 + length(xxs[1:])
length = makefunc(l1,l2)
#print( length (range(1004)) )
"""
#def iterate(func,init):
#    now = init
#    while 1:
#        yield now
#        now = func(now)
        
class Inf(object):
    # abstract class 
    def __repr__(self):
        return "< {} {} >".format(self.__class__.__name__,self.__name__)
    def generator(self): 
        raise NotImplementedError
    def __iter__(self):
        return self.generator()

class iterate(Inf):
    def __init__(self,func,init):
        self.func = func
        self.init = init
        self.stop = None
        self.__name__ = self.func.__name__ + repr(self.init)
    def generator(self):
        now = self.init
        count = 0
        while 1:
            yield now
            now = self.func(now)
            count += 1
            if count == self.stop:
                break

class map1(Inf):
    def __init__(self,func,stream):
        self.func = func
        self.s    = stream
        self.stop = None
        self.__name__ = self.func.__name__ + ':' +self.s.__name__

    def generator(self):
        g = self.s.generator()
        now = self.func( next(g) )
        count = 0
        while 1:
            yield now
            now = self.func( next(g) )
            count += 1
            if count == self.stop:
                break

class filter1(Inf):
    def __init__(self,func,stream):
        self.func = func # pred 
        self.s    = stream
        self.stop = None
        self.__name__ = self.func.__name__ + ':' +self.s.__name__
    def generator(self):
        g = self.s.generator()
        now = next(g)
        count = 0
        while 1:
            if self.func(now):
                yield now
                count += 1
            now = next(g)
            if count == self.stop:
                break

def copy(s):
    info_func = s.func
    info_stop = s.stop
    info_name = s.__name__
    if isinstance(s,iterate):
        info_init = s.init
        i = iterate(info_func,info_init)
        i.stop = info_stop
        i.__name__ = info_name
        return i
    elif isinstance(s,map1):
        info_s = s.s
        i = map1(info_func,info_s)
        i.stop = info_stop
        i.__name__ = info_name
        return i
    elif isinstance(s,filter1):
        info_s = s.s
        i = map1(info_func,info_s)
        i.stop = info_stop
        i.__name__ = info_name
        return i

inf = iterate(lambda x:x+1,0)
#def take(n,s):
#    return [i for v,i in zip(range(n),s)]
# head <=> take 1 inf 
# take 
#print( take(4,inf) )
#print( take(4,inf) )
mapv = map1(lambda x:x,inf)
filtv = filter1(lambda x:x%2==0,mapv)

class abc(object):
    def __repr__(self):
        return repr(self.s)+repr(self.env)
    def __init__(self,s):
        self.s   = s
        self.env = {}#[] #{}
    def __call__(self,n):
        if n not in self.env.keys():
            self.s.stop = n
            self.env[n] = copy(self.s)
            #[i for i in self.s]
            #list(self.s.generator())
            self.s.stop = None
            return self.env[n]
        else:
            return self.env[n]
class makeTake:
    def __init__(self,env):
        self.env = env
    def __call__(self,n,s):
        if s.__name__ not in self.env.keys():
            self.env[s.__name__] = abc(s)
            return self.env[s.__name__](n)
        else:
            return self.env[s.__name__](n)
env = {}
take = makeTake(env)
print( env )
print( list( take(4,inf) ) )
print( take(4,inf) == take(4,inf) )
print( list( take(5,inf) ) )
print( env )
print( list( take(4,mapv) ) )
print( take(4,mapv) == take(4,mapv) )
print( list( take(5,mapv) ) )
print( env )
print( list( take(4,filtv)  ) )
print( take(4,filtv) == take(4,filtv) ) 
print( list( take(5,filtv) ) )
print( env )

ta4 = take(4 ,inf)
ta2 = take(2 ,inf)
ta2s = take(2,ta4)
print( list(ta2s ) )
print( list(ta2) )
print( list(ta4) )
print( ta2s == ta2 )
import timeit 
#t1 = timeit.Timer("take(100000,inf)","from __main__ import take,inf")
#t2 = timeit.Timer("list(range(100000))")
t1 = timeit.Timer("list(take(10000000,inf))","from __main__ import take,inf")
t2 = timeit.Timer("list(range(10000000))")
#t1 = timeit.Timer("list(take( 1000000,inf))","from __main__ import take,inf")
#t2 = timeit.Timer("list(range(1000000))")
t  = 1
print( t1.timeit(t) )
print( t2.timeit(t) )
