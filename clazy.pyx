#coding=utf-8
cdef class Ref:
    cdef object Value
    def __init__(self,object v):
        self.Value = v
    def __repr__(self):
        return "(Ref {})".format(repr(self.Value))
cpdef list S(object a,object b):
    return [a,b]
cpdef list List(object s):
    return list(s)#[i for i in s]
cpdef list force(Ref s):
    x = s.Value
    if callable (x):
        s.Value = s.Value()
    return s.Value
cpdef list cons(object a,object b):
    return S(a,delay (b))
cpdef Ref delay(object x):
    return Ref (x)
cdef Mcycle(object seqfn): # 有 lambda 的无法做 cpdef 
    tmp = Ref ( seqfn (lambda : tmp.Value) )
    return tmp.Value
def cycle(object seqfn):
    return cycle(seqfn)
cdef list Map (object f,list s):
    if s == [None,None]:#s[0] == None and s[1] == None:
        return s
    return cons ( f(s[0]), lambda :Map(f,force (s[1])) )
def sMap(object f,list s):
    return Map(f,s)
cdef list Filter (object f,list s):
    if s == [None,None]:
        return s
    if f(s[0]) :
        return cons ( s[0] , lambda : Filter(f,force(s[1])))
    return Filter(f,force(s[1]))
def sFilter(object f,list s):
    return Filter(f,s)
cdef list Foldl(object f,object acc,list s):
    if s == [None,None]:
        return s
    return cons ( acc ,lambda : Foldl(f,f(s[0],acc),force(s[1]) ) )
def sFoldl(object f,object acc,list s):
    return Foldl(f,acc,s)
cdef list Mpairs(list xq,list yq):
    return cons ( (xq[0],yq[0]),lambda :Mpairs(force(xq[1]),force(yq[1])))
def pairs(list xq,list yq):
    return Mpairs(xq,yq)
cdef list Madd (list xq,list yq):
    plus = lambda a : a[0] + a[1]
    return sMap (plus,Mpairs(xq,yq))
def add(list xq,list yq):
    return Madd(xq,yq)
cdef list Miterates(object f,object x):
    return Mcycle (lambda g : cons( x ,  lambda : Map (f,g() ) ) )
def iterates(object f,object init):
    return Miterates(f,init)
cdef list Append (list xq,list yq):
    if xq == [None,None]:
        return yq
    return S ( xq[0],delay (lambda : Append ( force(xq[1]) , yq )))
def sAppend (list xq,list yq):
    return Append(xq,yq)

nature = iterates(lambda x:x+1,0)
def take(list s,int n):
    #print type(s),s
    while n > 1 and (s != [None,None]): #(s[0] != None and s[1] != None ):
        yield s[0]
        n-=1
        s = force(s[1])
    else:
        yield s[0]

