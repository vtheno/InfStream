#coding=utf-8
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
from clazy import *
nature = iterates(lambda x:x+1,0)
#smap = sMap(lambda x:x+1,nature)
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
