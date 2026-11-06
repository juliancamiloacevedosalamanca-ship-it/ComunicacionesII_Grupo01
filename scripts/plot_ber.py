import sys,csv,numpy as np, matplotlib; matplotlib.use('Agg'); import matplotlib.pyplot as plt
from scipy.special import erfc
# usage: plot_ber.py out.png label1=file1.csv label2=file2.csv ...
out=sys.argv[1]; series=[a.rsplit('=',1) for a in sys.argv[2:]]
eb=np.linspace(0,14,141); Q=0.5*erfc(np.sqrt(10**(eb/10)))
fig,ax=plt.subplots(figsize=(6.4,4.4),dpi=200)
ax.semilogy(eb,Q,'k-',lw=1.6,label='Teoría BPSK coherente')
ax.semilogy(eb,2*Q*(1-Q),'k--',lw=1.2,label='Teoría BPSK con cod. diferencial')
mk=['o','s','^','D','v']; cols=['#2563eb','#d97706','#dc2626','#16a34a','#7c3aed']
res={}
for i,(lab,f) in enumerate(series):
    e=[];b=[]
    for r in csv.DictReader(open(f)):
        e.append(float(r['EbN0_dB'])); b.append(float(r['BER']))
    e=np.array(e); b=np.array(b); res[lab]=(e,b)
    m=b>0
    ax.semilogy(e[m],b[m],mk[i%5],color=cols[i%5],ms=5,label=lab,ls='-',lw=1)
ax.set_xlabel('$E_b/N_0$ [dB]'); ax.set_ylabel('BER'); ax.set_ylim(1e-6,0.5); ax.set_xlim(0,14)
ax.grid(True,which='both',alpha=.3); ax.legend(fontsize=7,loc='lower left')
fig.tight_layout(); fig.savefig(out)
# penalty at 1e-3 vs DE-BPSK theory
def at(e,b,t=1e-3):
    for k in range(len(b)-1):
        if b[k]>=t>b[k+1] and b[k+1]>0:
            return e[k]+(np.log10(t)-np.log10(b[k]))/(np.log10(b[k+1])-np.log10(b[k]))*(e[k+1]-e[k])
    return None
ref=at(eb,2*Q*(1-Q)); print('teoria DE-BPSK @1e-3:',round(ref,2),'dB; BPSK:',round(at(eb,Q),2))
for lab,(e,b) in res.items():
    x=at(e,b); print(lab,'@1e-3:',None if x is None else round(x,2),'penalizacion vs DE:',None if x is None else round(x-ref,2))
    print('  ',' '.join(f'{v:.1e}' for v in b))
