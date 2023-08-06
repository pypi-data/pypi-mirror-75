from .matrix import BinaryMatrix
from functools import reduce
from pyvmodule.tools.polynomial import Polynomial
import numpy as np
def Identity(n):return BinaryMatrix((1<<i for i in range(n)),N=n)
def Zero(m,n):return BinaryMatrix((0 for i in range(m)),N=n)
def RowSum(r,c):return BinaryMatrix((((1<<r)-1)<<(i*c) for i in range(r)),N=r*c)
def ColSum(r,c):
    mask = reduce(lambda a,b:a|b,[1<<j for j in range(0,r*c,c)])
    return BinaryMatrix((mask<<i for i in range(c)),N=r*c)
def Square(r,c):return RowSum(r,c) + RowSum(r,c)
def Poly(m,n,seed=1,phase=0):return BinaryMatrix(Polynomial(m,seed)(2).powers(n,phase=phase)).T

@dataclass
class BaseTageHash:
    pc_skip:int
    pc_widths:List[int]
    ghr_widths:List[int]
    idx_widths:List[int]
    tag_widths:List[int]
    @property
    def arguments(self):return (self.pc_widths,self.pc_skip,self.ghr_widths,self.idx_widths,self.tag_widths)
class RandTageHash:
    style = 'random'
    def init(self):self.mat = gen_matrix(*self.arguments)
class PolyTageHash:
    style = 'polynomial'
    def init(self):self.mat = gen_matrix()
class SimpTageHash:
    style = 'simple'
    def init(self):self.mat = gen_matrix()
