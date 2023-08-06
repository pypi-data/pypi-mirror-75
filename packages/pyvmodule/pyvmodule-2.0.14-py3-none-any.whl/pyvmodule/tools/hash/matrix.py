from pyvmodule.tools.utility import clog2
from functools import reduce
class BinaryMatrix(list):
    '''Binary Matrix
    e.g. a matrix that N=4,M=5 [
     4'b0001,
     4'b0010,
     4'b0100,
     4'b1000,
     4'b1111]
    '''
    N = property(lambda self:clog2(max(self)+1) if self._N is None else self._N)
    M = property(lambda self:len(self))
    def __init__(self,*args,N=None,**kwargs):
        list.__init__(self,*args,**kwargs)
        self._N = N
    def bit(self,i,j):return (self[i]>>j)&1
    def __xor__(self,other):return BinaryMatrix([self[i]^other[i] for i in range(M)],N=self._N)
    def __or__ (self,other):return BinaryMatrix([self[i]|other[i] for i in range(M)],N=self._N)
    def __and__(self,other):return BinaryMatrix([self[i]&other[i] for i in range(M)],N=self._N)
    def __hash__(self):return hash(tuple(self))
    def __eq__(self,other):return tuple(self) == tuple(other)
    def __call__(self,other):return self*other
    def __mul__(self,other):
        mat = [reduce((lambda a,b:a^b),(other[j] for j in range(len(other)) if (1<<j)&self[i])) for i in range(len(self))]
        return BinaryMatrix(mat)
    def __mod__(self,other):
        if other._N is None:raise ValueError('Unknown Boundary')
        mat = [self[i]<<other._N | other[i] for i in range(len(self))]
        return BinaryMatrix(mat,N=None if self._N is None else self._N + other._N)
    @property
    def T(self):
        mat = [reduce((lambda a,b:a^b),(self.bit(j,i)<<j for j in range(len(self)))) for i in range(self.N)]
        return BinaryMatrix(mat,N=len(self))
    def split(self,start=0,stop=None):
        width = (None if self._N is None else self._N - start) if stop is None else stop - start
        mask  = -1 if width is None else (1<<width)-1 
        return BinaryMatrix([(item>>start)&mask for item in self],N=width)
    def __str__(self):
        fmtstr = '{:0%db}'%self.N
        return '\n'.join(fmtstr.format(self[i]) for i in range(self.M))
    def __repr__(self):
        return '<BinaryMatrix n=%d m=%d rank=%d>\n%s\n</BinaryMatrix>'%(self.N,self.M,self.rank,str(self))
    @property
    def rank(self):
        mat = self.copy()
        r = 0
        while len(mat)>0:
            m = max(mat)
            if m==0:break
            sel = 1<<(clog2(m+1)-1)
            for i in range(len(mat)-1,-1,-1):
                if sel&mat[i]:mat[i]^=m
                if mat[i]==0:del mat[i]
            r+= 1
        return r
    
