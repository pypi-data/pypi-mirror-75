from .memorization import memorized
from .utility import clog2
__all__ = ['Polynomial']
def keep(f):
    def g(self,x):
        return type(self)(f(int(self),int(x)))
    return g
def keep_modulus(f):
    def g(self,x):
        return type(self)(f(type(self),int(self),int(x)))
    return g
    
class BinaryPolynomial(int):
    __or__  = keep(lambda self,x:self|x)
    __and__ = keep(lambda self,x:self&x)
    __xor__ = keep(lambda self,x:self^x)
    __lshift__ = keep(lambda self,x:self<<x)
    __rshift__ = keep(lambda self,x:self>>x)
    @keep
    def __pow__(self,n):
        assert n>=0
        y = 1
        while n>0:
            if n&1:y = self*y
            n >>=1
            self = self*self
        return y
    def powers(self,n,phase=0):
        x = self**phase
        for i in range(n):
            yield int(x)
            x = x * self
    def __call__(mod,x):return Polynomial(clog2(mod+1),mod)(x)
    def __mod__ (x,mod):return Polynomial(clog2(mod+1),mod)(x)
    @keep
    def __mul__(x,y):
        z = 0
        while x>0:
            if x&1:z^=y
            x>>=1
            y<<=1
        return z
class ModulusPolynomial(BinaryPolynomial):
    @keep_modulus
    def __lshift__(cls,x,n):
        if n < cls._deg:
            top,msk = 1<<cls._deg,(1<<cls._deg)-1
            for i in range(n):
                x <<= 1
                if x&top:x^=cls._mod
            return x
        else:return (cls(2)**n)*x
    @keep_modulus
    def __rshift__(cls,x,n):
        if cls._mod&1:
            for i in range(n):
                if x&1:x^=cls._mod
                x>>=1
            return x
        else:return x>>n
    def __new__(cls,val):
        assert val >= 0
        t = 1<<cls._deg
        if val >= t:
            sft = clog2(val+1)-1
            top = 1<<sft
            msk = cls._mod<<(sft-cls._deg)
        while val >= t:
            if val&top:val^= msk
            top >>= 1
            msk >>= 1
        return super(ModulusPolynomial,cls).__new__(cls,val)
@memorized
def Modulus(deg,mod):
    assert mod < (1<<(deg + 1))
    mod |= 1<<deg
    class Poly(ModulusPolynomial):
        _deg = deg
        _mod = mod
    return Poly
def Polynomial(deg=-1,mod=0):
    if deg < 0:return BinaryPolynomial
    else:return Modulus(deg,mod)
