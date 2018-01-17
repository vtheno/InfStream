#coding=utf-8
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

temp = zip(MyRange(0),MyRange(0,4))
print temp 
print unZip(temp)
#print Zip(MyRange(0),MyRange(0,4))
# x for x in (1,) <=> x where x = 1
def x():
    for i in MyRange(0):
        if i%2 == 0:
            yield i
# zip([ x for x in MyRange(0) if x%2==0 ],range(4))
print [i for k,i in zip(MyRange(0,4) , x()) ]
