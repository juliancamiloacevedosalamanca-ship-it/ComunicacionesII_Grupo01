import numpy as np, csv
from scipy.special import erfc
from link import *
Q=lambda x:0.5*erfc(x/np.sqrt(2))
EB=np.arange(0,15)
def curva(A,noise_amp=0.0,seed=3):
    rng=np.random.default_rng(seed); out=[]
    for eb in EB:
        nb=400000 if eb<7 else (2000000 if eb<10 else 4000000)
        errs=0;tot=0;chunk=500000
        for k in range(0,nb,chunk):
            b=rng.integers(0,2,chunk); x=tx(b,diff=True)
            y,_=canal(x,noise_amp,A,rng)
            Ps=np.mean(np.abs(y)**2)          # e_EbN0_Sweep: potencia medida antes del ruido artificial
            Pn=Ps*fs/(Rs*10**(eb/10))
            y=y+np.sqrt(Pn/2)*(rng.standard_normal(len(y))+1j*rng.standard_normal(len(y)))
            z,s,bh=rx(y,0,diff=True)
            g=1000; e=bh[11+g:]!=b[g:len(bh)-11]
            errs+=e.sum(); tot+=len(e)
        out.append((eb,errs/tot,tot,errs)); print(A,eb,errs/tot,tot,errs,flush=True)
    return out
res={}
for tag,A in [('AWGN',0.0),('Impulsos_A1',1.0),('Impulsos_A5',5.0)]:
    res[tag]=curva(A)
    with open(f'curva_BER_sim_{tag}.csv','w',newline='') as f:
        w=csv.writer(f); w.writerow(['EbN0_dB','BER','bits','errores'])
        for r in res[tag]: w.writerow([r[0],f'{r[1]:.6e}',r[2],r[3]])
