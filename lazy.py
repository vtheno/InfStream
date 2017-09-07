#coding=utf-8
from copy import deepcopy as dp
# delay
def delay(x):
    yield x
    #tmp = [x]
    #def delay_inline():
    #    return tmp[0]
    #return delay_inline
# force <==> next
def force(x):
    return next(x)
    #return apply(x)
def car(x):
    return x[0]
    
def cdr(x):
    return x[1]

def lazy_cons(a,b):
    return [a,delay(b)]

def lazy_cdr(x):
    return force(cdr(x))

def inf_seq(a0,fn):
    #    return lazy_cons(a0,inf_seq(fn(a0),fn))
    # 直接用return 会直接...
    # 想在这里尝试 eta 变换
    yield lazy_cons(a0,inf_seq(fn(a0),fn))

tmp = inf_seq(0,lambda x:x+1)
print tmp
print tmp,force(dp(tmp))
def ref(lazy_lst,n):
    tmps = None # []
    tmpa = dp(lazy_lst);tmpb = force(tmpa);tmpn = n
    while tmpn!=0:
        #tmps.append(car(tmpb))
        tmps = car(tmpb)
        tmpa = force(cdr(tmpb))
        tmpb = force(tmpa)
        tmpn = tmpn - 1
    #print tmps
    return tmps # tmps[n]
    
print ref(tmp,23333)

def ref2(lst,n):
    tmp = dp(lst);lsta=force(tmp)
    if n==0:
        return car(lsta)
    else:
        return ref2(lazy_cdr(lsta),n-1)

print ref2(tmp,666)

def head(lazy_lst,n):
    tmps = []
    tmpa = dp(lazy_lst);tmpb = force(tmpa);tmpn = n
    while tmpn!=0:
        tmps.append(car(tmpb))
        tmpa = force(cdr(tmpb))
        tmpb = force(tmpa)
        tmpn = tmpn - 1
    #print tmps
    return tmps # tmps[n]

print head(tmp,66)

def head2(lst,n):
    if n==0:
        return []
    else:
        tmp = dp(lst);lsta=force(tmp)
        return [car(lsta),head2(lazy_cdr(lsta),n-1)]

print head2(tmp,66)

def lazy_filter(pred,lst):
    tmpa = dp(lst);tmpb = force(tmpa);
    while True:
        x = car(tmpb)
        if pred(x):
            yield x
        tmpa = lazy_cdr(tmpb)
        tmpb = force(tmpa)

for i in range(100):
    print next(lazy_filter(lambda x:x%2==0,tmp))
        
def lazy_map(fn,lst):
    tmp = dp(lst);lsta=force(tmp);obj=car(lsta)
    yield lazy_cons(fn(obj),lazy_map(fn,lazy_cdr(lsta)))
tmp2 = lazy_map(lambda x:x+233,tmp)
print tmp2
print head2(tmp2,10)
print ref2(tmp2,1)
print head(lazy_map(lambda x:x%2==0,tmp),10)
