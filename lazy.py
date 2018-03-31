#coding=utf-8
"""
class Ref(object):
    __slots__ = ["Value"]
    def __init__(self,v):
        self.Value = v
    def __repr__(self):
        return "(Ref {})".format(repr(self.Value))
        #if callable(self.Value):
        #    return "(Ref {})".format("delay")
        #return "(Ref {})".format(repr(self.Value))
    #def __invert__(self):
    #    return self.Value
    #def __le__(self,v):
    #    self.Value = v
    #    return self
"""
#class S(object):
#    def __init__(self,a,b):
#        self.hd = a # if a == None then get self.hd raise Empty error
#        self.tl = b #
#    def __repr__(self):
#        #print "repr:",type(self.tl)
#        return "s<{},delay>".format(repr(self.hd))
"""
def S(a,b):
    return [a,b]
def delay(x):
    return Ref (x) # ref (Delayed f) (Delayed of unit -> 'a t 
def force(s):
    #print "force:",type(s)
    x = s.Value#(~s) # case !xp of 
    if callable (x): # (Delayed f) => let val s = f() in xp := s ; s end
        #s <= x()
        s.Value = s.Value ()
        return s.Value #(~s)
    return s.Value #(~s) # | s => s
def cons(a,b):
    return S(a,delay (b))
empty = Ref(S(None,None))
def cycle(seqfn):
    #tmp = Ref( S(None,None) )
    #tmp <= seqfn (lambda : ~tmp)
    #return ~tmp
    # tmp.Value = seqfn (lambda : tmp.Value)
    tmp = Ref ( seqfn (lambda : tmp.Value) )
    return tmp.Value
"""
"""
def take (s,n): # take : 'a t * int -> 'a list
    #print "take:",type(s),s
    if n == 0 or (s[0] == None and s[1] == None) :#( s.hd == None and s.tl == None):
        return [ ]
    #return [ s.hd ] + take ( force(s.tl)  ,n - 1)
    return [s[0]] + take ( force (s[1]),n-1)
def take1 (s,n):
    while not (n ==0 or (s[0] == None and s[1] == None)):
        #while not (n == 0 or ( s.hd == None and s.tl == None)) :
        n -= 1
        yield s[0]#s.hd
        #s = force(s.tl)
        s = force(s[1])
"""
"""
def take (s,n):
    while n > 1 and (s[0] != None and s[1] != None ):
        yield s[0]
        n-=1
        s = force(s[1])
    else:
        yield s[0]
"""
"""
def sMap (f,s):
    #if (s.hd == None and s.tl == None):
    #    return [ ]
    #return S ( f (s.hd) , delay (lambda : sMap (f,force (s.tl))) )
    if s[0] == None and s[1] == None:
        return s
    return cons ( f(s[0]), lambda :sMap(f,force (s[1])) )
"""
"""
def sFilter (pred,s):
    if s[0] == None and s[1] == None:
        return s
    if pred(s[0]) :
        return cons ( s[0] , lambda : sFilter(pred,force(s[1])))
    return sFilter(pred,force(s[1]))
def sFoldl (func,acc,s): # it is list
    if (s[0] == None and s[1] == None):
        return s
    return cons ( acc ,lambda :sFoldl(func,func(s[0],acc),force(s[1])) )
"""
"""
def pairs(xq,yq):
    #return cons( (xq.hd,yq.hd) ,lambda : pairs( force (xq.tl) , force(yq.tl)))
    return cons ( (xq[0],yq[0]),lambda :pairs(force(xq[1]),force(yq[1])))
def add (xq,yq):
    plus = lambda a : a[0] + a[1]
    return sMap (plus,pairs(xq,yq))
def iterates(f,x):
    return cycle (lambda g :
                  cons( x ,  lambda : sMap (f,g()) ) )
"""
"""
def append (xq,yq) :
    if xq[0] == None and xq[1] == None:
        return yq
    return S ( xq[0],delay (lambda : append ( force(xq[1]) , yq )))
def fromList (lst):
    if lst == []:
        return S (None,None)
    return cons (lst[0], lambda : fromList(lst[1:]) )
def cList(s):
    return [i for i in s]
"""
"""
t1 = fromList( list(range(100)) ) 
print( "t1:",t1 )
print( [ i for i in take(t1,10) ] )
f = lambda g : cons("Never!",g)
never = cycle (f)
print( never )
print( force(never[1]) ) # [ "Never!",delay ] => ["Never!",["Never!",...]]
print( never )
test = append (t1,never)
print( list( take(test ,100)) )
zero = cycle (lambda g : cons (0,g) )
print( id (zero[1]) )
force(zero[1])
print( id (zero[1]) )
print( id (((zero[1]).Value)[1]))
one  = cycle (lambda g : cons (1,g) )
print ( [i for i in take(one,1)] )
fib = cycle ( lambda fibf :
              cons (1,lambda :
                    cons (1,lambda :
                          add(fibf(),force((fibf())[1])))))
nature = cycle (lambda g :
                cons( 0 ,  lambda : sMap ( lambda x : x+1,g())) )
head2 = List( take(nature,2) )
print ( head2 )
print ( head2[0] is nature[0] )
print ( head2[1] is ((nature[1]).Value)[0])
print ( (nature[1].Value) )
print ( ((nature[1].Value)[1]) )
print ( [i for i in take(nature,20) ] )
even = sFilter(lambda x:x%2==0 ,nature)
print ( [i for i in take(even,20)] )
sumNature = sFoldl(lambda a,b: a+b,nature[0],force(nature[1]))
print( [i for i in take(sumNature,20)] )
"""

from clazy import *
nature = iterates(lambda x:x+1,0)
#print List(take(nature,200))
smap = sMap(lambda x:x+1,nature)
#print List(take(smap,1000000))
#print List(take(nature,200000))
if __name__ == "__main__":
    import timeit
    t01 = timeit.Timer("map(lambda x:x+1,tmp)","tmp = range(1000000)")
    t02 = timeit.Timer("take(tmp,1000000)",
                       "from __main__ import take,nature,sMap;tmp = sMap(lambda x:x+1,nature)")
    t11 = timeit.Timer("list(t2)","tmp = range(1000000);t2=map(lambda x:x+1, tmp)")
    t12 = timeit.Timer("list(t2)",
                       "from __main__ import take,nature,sMap;tmp = sMap(lambda x:x+1,nature);t2=take(tmp,1000000)")
    t21 = timeit.Timer("[i for i in t2]","tmp = range(1000000);t2=map(lambda x:x+1, tmp)")
    t22 = timeit.Timer("[i for i in t2]",
                       "from __main__ import take,nature,sMap;tmp = sMap(lambda x:x+1,nature);t2=take(tmp,1000000)") 
    t31 = timeit.Timer("[i for i in t2]","tmp = range(1000000);t2=map(lambda x:x+1, tmp)")
    t32 = timeit.Timer("List(t2)",
                       "from __main__ import take,nature,sMap,List;tmp = sMap(lambda x:x+1,nature);t2=take(tmp,1000000)") 
    t = 1#00000000
    #print( "t01",t01.timeit(t) )
    #print( "t02",t02.timeit(t) )
    print( "t11",t11.timeit(t) )
    print( "t12",t12.timeit(t) )
    print( "t21",t21.timeit(t) )
    print( "t22",t22.timeit(t) ) # ...
    print( "t31",t31.timeit(t) )
    print( "t32",t32.timeit(t) )
