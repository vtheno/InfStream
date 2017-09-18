#coding=utf-8
class Stream(object):
    """ A lazily computed recursive list."""
    """ 一个 惰性 计算 的 递归列表 """
    def __init__(self,first,compute_rest,empty=False):
        self.first = first
        self._compute_rest = compute_rest
        self.empty = empty
        self._rest = None
        self._computed = False

    @property
    def rest(self):
        """ Return the rest of the stream computing it necessary."""
        """ CONS [ A . B ] CAR => FIRST CDR => REST """
        """ 属性函数 """
        assert not self.empty,'Empty Streams have no rest.'
        # 空流无息 => 空 Stream 没有 信息 Nothing => nil
        if not self._computed:
            # 惰性求值 不过是 增加了 一层函数抽象 
            self._rest = self._compute_rest()
            # self._rest = apply(self._compute_rest)
            self._computed = True
            # 是否 求值了 
        return self._rest

    def __repr__(self):
        if self.empty:
            return "<Empty Stream>"
        return 'Stream({0},<compute_rest>)'.format(repr(self.first))

    def take(self,n):
        """ 获取第 n 个xxx... """
        if self.empty:
            return self
        while n > 0:
            self = self.rest
            n = n - 1
        return self.first

    def head(self,n):
        """ 获取前 n 个xxx... """
        r = []
        while n > 0:
            r.append(self.first)
            self = self.rest
            n = n - 1
        return r

    def takes(self,from_n,to_n):
        """ 获取 从 fron_n 到 to_n 个xxx..."""     
        r = [];tmpn = to_n - from_n
        while from_n > 0:
            self = self.rest
            from_n = from_n - 1
        while tmpn > 0:
            r.append(self.first)
            self = self.rest
            tmpn = tmpn - 1
        return r


def make_integer_stream(first=1):
    """ 递归定义了 正整数 流(惰性序列) """
    def compute_rest():
        return make_integer_stream(first+1)
    return Stream(first,compute_rest)



def map_stream(fn,s):
    """ 函数组合 """    
    if s.empty:
        return s
    def compute_rest():
        return map_stream(fn,s.rest)
    return Stream(fn(s.first),compute_rest)

def filter_stream(fn,s):
        
    if s.empty:
        return s
    def compute_rest():
        return filter_stream(fn,s.rest)
    if fn(s.first):
        return Stream(s.first,compute_rest)
    return compute_rest()
# reduce is need all values ,so ..we no define

def take(s,n):
    if s.empty:
        return s
    while n!=0:
        s = s.rest
        n = n - 1
    return s.first

def takes(s,f_n,t_n):
    r = [];tmpn = t_n - f_n
    while f_n > 0:
        s = s.rest
        f_n = f_n - 1
    while tmpn > 0:
        r.append(s.first)
        s = s.rest
        tmpn = tmpn - 1
    return r
    
def truncate_stream(s,k):
    if s.empty or k == 0:
        return Stream.empty
    def compute_rest():
        return truncate_stream(s.rest,k-1)
    return Stream(s.first,compute_rest)

def stream2list(s):
    r = []
    while not s.empty:
        r.append(s.first)
        s = s.rest
    return r

def head(s,n):
    if s.empty:
        return s
    r = []
    while n!=0:
        r.append(s.first)
        s = s.rest
        n = n - 1
    return r

def ref(s,n):
    if s.empty:
        return s
    if n==0:
        return s.first
    else:
        return ref(s.rest,n-1)

def isPrime(n):
    if n<=1:
        return False
    i = 2
    while i*i <= n:
        if n%i is 0:
            return False
        i = i + 1
    return True

def test():

    #s = Stream(1,lambda:(Stream(2+3,lambda:Stream.empty)))
    #print s.first
    #print s.rest
    
    ints = make_integer_stream()
    #print ints
    #print ints.first
    #print ints.rest.first
    
    ints_mod2iszero = filter_stream(lambda x:x%2==0,ints)
    ints_mod3iszero = filter_stream(lambda x:x%3==0,ints)
    ints2 = map_stream(lambda x:x*3,ints)
    print head(ints2,20)

    print take(ints_mod2iszero,20)
    print head(ints_mod2iszero,20)
    print ref(ints_mod2iszero,200)

    print head(ints_mod3iszero,20)

    Prime = filter_stream(isPrime,ints)
    print head(Prime,20)
    #print ref(Prime,20000)
    print "20000"
    import time
    ts = time.clock()
    print take(Prime,100000)
    print time.clock()- ts

