#coding=utf-8
#cimport cython
#from cython cimport array
#from cpython cimport list
#from cython.view cimport array as carray
cdef class Ref:
    cdef object Value
    def __init__(self,object v):
        self.Value = v
    def __repr__(self):
        return "(Ref {})".format(repr(self.Value))
cpdef list S(object a,object b):
    return [a,b]
cpdef list List(object s):
    return [i for i in s]#list(s)
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
def cycle(seqfn):
    return cycle(seqfn)
cdef list Map (object f,list s):
    if s == [None,None]:#s[0] == None and s[1] == None:
        return s
    return cons ( f(s[0]), lambda :Map(f,force (s[1])) )
def sMap(f,s):
    return Map(f,s)
cdef list Mpairs(list xq,list yq):
    return cons ( (xq[0],yq[0]),lambda :Mpairs(force(xq[1]),force(yq[1])))
def pairs(xq,yq):
    return Mpairs(xq,yq)
cdef list Madd (list xq,list yq):
    plus = lambda a : a[0] + a[1]
    return sMap (plus,Mpairs(xq,yq))
def add(xq,yq):
    return Madd(xq,yq)
cdef list Miterates(object f,object x):
    return Mcycle (lambda g : cons( x ,  lambda : Map (f,g() ) ) )
def iterates(f,init):
    return Miterates(f,init)
nature = iterates(lambda x:x+1,0)
def take(list s,int n):
    #print type(s),s
    while n > 1 and (s[0] != None and s[1] != None ):
        yield s[0]
        n-=1
        s = force(s[1])
    else:
        yield s[0]

