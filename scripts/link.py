import numpy as np, math, sys, os
sys.path.insert(0,os.path.dirname(os.path.abspath(__file__)))
from grsim import rrc
Rs,Sps,beta,span=32000,8,0.35,11; fs=Rs*Sps; P=256
htx=rrc(Sps,fs,Rs,beta,span*Sps); E=np.sum(htx**2); hrx=htx/E
D=len(htx)-1  # 88 muestras = 11 simbolos
def prbs15(n,seed=1):
    # GLFSR grado 15 (x^15+x^14+1), solo para tener una secuencia determinista
    rng=np.random.default_rng(seed); return rng.integers(0,2,n)
def tx(bits,diff=False):
    d=bits.copy()
    if diff:
        d=np.bitwise_xor.accumulate(bits)
    a=np.where(d==1,1.0,-1.0); up=np.zeros(len(a)*Sps); up[::Sps]=a
    return np.convolve(up,htx)[:len(up)]
def canal(x,noise_amp,A,rng):
    y=x.astype(complex)+noise_amp*(rng.standard_normal(len(x))+1j*rng.standard_normal(len(x)))/np.sqrt(2)
    imp=np.zeros(len(x)); imp[P-1::P]=A
    return y+imp, imp
def rx(y,offset=0,diff=False):
    z=np.convolve(y,hrx)[:len(y)]
    s=z[offset::Sps]; dh=(s.real>0).astype(np.uint8)
    if diff:
        bh=dh^np.concatenate([[0],dh[:-1]])
    else: bh=dh
    return z,s,bh
def ber(b,bh,delay):
    n=len(bh)-delay; return np.mean(bh[delay:delay+n]!=b[:n]), n
