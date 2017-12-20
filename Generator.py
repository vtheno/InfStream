#coding=utf-8
class Generator(object):
    #__slots__ = ['init_func','init_val']
    def __init__(self, init_func, init_val):
        self.init_func = init_func
        self.old_init_val = init_val
        self.init_val = init_val
        self.store    = [  ]
        self.firstForce = 1#True
    def iter(self):
        now = self.init_val if self.firstForce else self.init_func(self.init_val)
        while 1:
            yield now
            self.store.append(now)
            now = self.init_func(now)
            
    def __iter__(self):
        return self.iter()
        
def myrange(size):
    return [0]*size

def head(n,stream):
    assert n >= 0 
    if stream.firstForce:
        tmp = [i for i,_ in zip(stream, [0]*n ) ]
        stream.firstForce = 0
        stream.init_val = stream.store[-1]
        return tmp
    else:
        if n > len(stream.store):
            tmp = [i for i,_ in zip(stream, [0] * (n - len(stream.store) ) )]
            stream.init_val = stream.store[-1]
            return [i for i in stream.store[0:n]]
        elif n == len(stream.store):
            return [i for i in stream.store]
        else:
            return [i for i in stream.store[0:n]]
        
def get(n,stream):
    t = head(n,stream)
    #print 'get:',t
    while t: return t[-1]

def copyInfo(stream):
    temp = Generator(stream.init_func,stream.old_init_val)
    temp.firstForce = stream.firstForce
    return temp
def Map(f,stream):
    item = stream.iter()
    temp = copyInfo(stream)
    if not temp.firstForce:
        temp.store = map(f,stream.store)
        temp.init_val = temp.store[-1]
    def mapc():
        for i in stream:
            r = f(next(item))
            temp.store.append(r)
            yield r
    temp.iter = mapc
    return temp

def Filter(f,stream):
    item=stream.iter()
    temp=copyInfo(stream)
    if not temp.firstForce:
        temp.store = filter(f,stream.store)
        temp.init_val = temp.store[-1]
    def filc():
        while 1:
            tmp  =  next(item)
            flag =  f(tmp)
            if flag: 
                temp.store.append(tmp)
                yield tmp
    temp.iter = filc
    return temp
g = Generator(lambda x:x+1,0)
def show(stream):
    print( "func:",stream.init_func )
    print( "old:",stream.old_init_val)
    print( "val:",stream.init_val  )
    print( "store:",stream.store     )
    print( "store:",len(stream.store) )
    return 'done'
print( '5,g', head(5,g)  )
print( '1000,g',head(1000,g)[-1] )
z = Map(lambda x:x*2,g)
print( '6,z',head(6,z) )
c = Filter(lambda x:x%2==0,z)
print( '7,c',head(7,c) )
print( '5,c',get(5,c) )
print( '100,c',len(head(100,c)) )

import timeit
t1 = timeit.Timer("range(100)")
t2 = timeit.Timer("head(100,g)",'from __main__ import head,g')
print( t1.timeit() ,t2.timeit() )
