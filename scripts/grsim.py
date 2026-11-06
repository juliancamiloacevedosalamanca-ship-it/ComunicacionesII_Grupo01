import numpy as np, math
from scipy.special import erfc
def rrc(gain, fs, rs, alpha, ntaps):
    ntaps |= 1; spb=fs/rs; taps=np.zeros(ntaps); scale=0
    for i in range(ntaps):
        x=i-ntaps//2; x1=math.pi*x/spb; x2=4*alpha*x/spb; x3=x2*x2-1
        if abs(x3)>=1e-6:
            num = math.cos((1+alpha)*x1)+math.sin((1-alpha)*x1)/(4*alpha*x/spb) if i!=ntaps//2 else math.cos((1+alpha)*x1)+(1-alpha)*math.pi/(4*alpha)
            den=x3*math.pi
        else:
            x3=(1-alpha)*x1; x2=(1+alpha)*x1
            num=(math.sin(x2)*(1+alpha)*math.pi-math.cos(x3)*((1-alpha)*math.pi*spb)/(4*alpha*x)+math.sin(x3)*spb*spb/(4*alpha*x*x))
            den=-32*math.pi*alpha**3*x/spb
        taps[i]=4*alpha*num/den; scale+=taps[i]
    return taps*gain/scale
Rs,Sps,beta,span=32000,8,0.35,11; fs=Rs*Sps
htx=rrc(Sps,fs,Rs,beta,span*Sps); E=np.sum(htx**2); hrx=htx/E
print('ntaps',len(htx),'sum',htx.sum(),'E',E,'peak',htx.max())
def run(nbits=200000,noise_amp=0.0,A=0.0,P=256,ebn0=None,seed=1,offset=0,delay=None):
    rng=np.random.default_rng(seed); b=rng.integers(0,2,nbits); a=np.where(b==1,1.0,-1.0)
    up=np.zeros(nbits*Sps); up[::Sps]=a; y=np.convolve(up,htx)[:len(up)].astype(complex)
    Ps=np.mean(np.abs(y)**2)
    y=y+noise_amp*(rng.standard_normal(len(y))+1j*rng.standard_normal(len(y)))/np.sqrt(2)
    imp=np.zeros(len(y)); imp[P-1::P]=A; y=y+imp
    if ebn0 is not None:
        Ps2=np.mean(np.abs(y)**2); Pn=Ps2*fs/(Rs*10**(ebn0/10)); y=y+np.sqrt(Pn/2)*(rng.standard_normal(len(y))+1j*rng.standard_normal(len(y)))
    z=np.convolve(y,hrx)[:len(y)]
    s=z[offset::Sps]; bh=(s.real>0).astype(int)
    if delay is None:
        best=min(range(0,30),key=lambda d: np.mean(bh[d:d+5000]!=b[:5000])); delay=best
    err=np.mean(bh[delay:]!=b[:len(bh)-delay])
    return dict(delay=delay,ber=err,Ps=Ps,s=s,z=z)
if __name__=='__main__':
    for off in range(8):
        r=run(20000,offset=off); print('offset',off,'delay',r['delay'],'ber',r['ber'],'|s| min',np.min(np.abs(r['s'][20:].real)).round(3))
