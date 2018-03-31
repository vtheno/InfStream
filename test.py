from clazy import *

print nature
print list(take(nature,3))
print nature
natPlusOne 
even = sFilter(lambda x:x%2==0,nature)
print even
print list(take(even,20))
print even
msum = sFoldl(lambda a,b:a+b,nature[0],force(nature[1]))
print msum
print list(take(msum,3))
print msum

