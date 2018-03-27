#coding=utf-8
class Ref(object):
    def __init__(self,v):
        self.Value = v
    def __repr__(self):
        return "(Ref {})".format(repr(self.Value))
    def __invert__(self):
        return self.Value
    def __le__(self,v):
        self.Value = v
        return self

class S(object):
    def __init__(self,a,b):
        self.hd = a # if a == None then get self.hd raise Empty error
        self.tl = b #
    def __repr__(self):
        #print "repr:",type(self.tl)
        return "s<{},delay>".format(repr(self.hd))
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
    tmp = Ref( S(None,None) )
    #tmp <= seqfn (lambda : ~tmp)
    #return ~tmp
    # tmp.Value = seqfn (lambda : tmp.Value)
    tmp.Value = seqfn (lambda : tmp.Value)
    return tmp.Value
class Cycle(object):
    def __init__(self):
        self.tmp = Ref(S(None,None))
    def __call__(self,seqfn):
        self.tmp.Value = seqfn(lambda : self.tmp.Value)
        return self.tmp.Value
cycle = Cycle()
def take (s,n): # take : 'a t * int -> 'a list
    #print "take:",type(s),s
    if n == 0 or (s[0] == None and s[1] == None) :#( s.hd == None and s.tl == None):
        return [ ]
    #return [ s.hd ] + take ( force(s.tl)  ,n - 1)
    return [s[0]] + take ( force (s[1]),n-1)
def take1 (s,n):
    while not (n ==0 or (s[0] == None and s[1] == None)):
        #while not (n == 0 or ( s.hd == None and s.tl == None)) :
        yield s[0]#s.hd
        n -= 1
        #s = force(s.tl)
        s = force(s[1])
def sMap (f,s):
    #if (s.hd == None and s.tl == None):
    #    return [ ]
    #return S ( f (s.hd) , delay (lambda : sMap (f,force (s.tl))) )
    if s[0] == None and s[1] == None:
        return [ ]
    return S ( f(s[0]),delay (lambda :sMap(f,force (s[1]))))
def pairs(xq,yq):
    #return cons( (xq.hd,yq.hd) ,lambda : pairs( force (xq.tl) , force(yq.tl)))
    return cons ( (xq[0],yq[0]),lambda :pairs(force(xq[1]),force(yq[1])))
def add (xq,yq):
    plus = lambda a : a[0] + a[1]
    return sMap (plus,pairs(xq,yq))
def iterates(f,x):
    return cycle (lambda g :
                  cons( x ,  lambda : sMap (f,g()) ) )
def append (xq,yq) :
    if xq[0] == None and xq[1] == None:
        return yq
    return S ( xq[0],delay (lambda : append ( force(xq[1]) , yq )))
def fromList (lst):
    if lst == []:
        return S (None,None)
    return cons (lst[0],lambda : fromList(lst[1:]) )
t1 = fromList( list(range(100)) ) 
print( t1 )
f = lambda g : cons("Never!",g)
never = cycle (f)
print( never )
print( force(never[1]) )
print( never )
test = append (t1,never)
print( list( take1(test ,100)) )
zero = cycle (lambda g : cons (0,g) )
print( id (zero[1]) )
force(zero[1])
print( id (zero[1]) )
print( id (((zero[1]).Value)[1]))
one  = cycle (lambda g : cons (1,g) )
fib = cycle ( lambda fibf :
              cons (1,lambda :
                    cons (1,lambda :
                          add(fibf(),force((fibf())[1])))))
nature = cycle (lambda g :
                cons( 0 ,  lambda : sMap ( lambda x : x+1,g())) )
nature = iterates(lambda x:x-1,0)
#print( list(take1(nature,1000000)) )
if __name__ == "__main__":
    import cProfile
    import timeit
    t1 = timeit.Timer("map(lambda x:x+1, range(1000000))")
    t2 = timeit.Timer("take1(tmp,              1000000)",
                      "from __main__ import take1,nature,sMap;tmp = sMap(lambda x:x+1,nature)")
    t = 10000000
    print( t1.timeit(t) )
    print( t2.timeit(t) )
    # print( cProfile.run(
