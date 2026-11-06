import numpy as np, matplotlib; matplotlib.use('Agg'); import matplotlib.pyplot as plt
from scipy.signal import welch
from link import *
plt.rcParams.update({'font.size':9,'axes.grid':True,'grid.alpha':.3,'savefig.dpi':200,'figure.dpi':100})
C1,C2,C3='#1f5fa8','#c23b22','#2a8a4a'
rng=np.random.default_rng(7)
N=200000; b=prbs15(N); x=tx(b)
cases=[0.0,0.3,0.6,1.0,5.0]
R={}
for A in cases:
    y,imp=canal(x,0.10,A,np.random.default_rng(11))
    z,s,bh=rx(y,0)
    e,n=ber(b,bh,11)
    st=s[20:].real
    # muestras de decision afectadas por impulsos
    R[A]=dict(y=y,z=z,s=s,ber=e,n=n,minI=np.min(np.abs(st)))
    print(f'A={A}: BER={e:.2e} (n={n}) min|I|={R[A]["minI"]:.3f}')
# offset
for off in range(8):
    y,_=canal(x,0.10,0.0,np.random.default_rng(11)); z,s,bh=rx(y,off)
    print('offset',off,'BER',ber(b,bh,11)[0],'min|I|',np.min(np.abs(s[20:].real)).round(3))
# --- PSD
f,Ptx=welch(x,fs=fs,nperseg=1024,return_onesided=False,window='blackmanharris',detrend=False)
f2,Pch=welch(R[1.0]['y'],fs=fs,nperseg=1024,return_onesided=False,window='blackmanharris',detrend=False)
f3,Pch5=welch(R[5.0]['y'],fs=fs,nperseg=1024,return_onesided=False,window='blackmanharris',detrend=False)
o=np.argsort(f)
fig,ax=plt.subplots(figsize=(6.4,3.3))
ax.plot(f[o]/1e3,10*np.log10(Ptx[o]*fs),color=C1,lw=1.2,label='Salida RRC Tx')
ax.plot(f[o]/1e3,10*np.log10(Pch[o]*fs),color=C2,lw=1,label='Canal: AWGN 0.10 + impulsos $A_{imp}$=1.0')
ax.plot(f[o]/1e3,10*np.log10(Pch5[o]*fs),color='#e0912c',lw=1,ls='--',label='Canal con $A_{imp}$=5.0')
for v in (-21.6,21.6): ax.axvline(v,color='k',ls=':',lw=.8)
ax.text(23,3,'$\\pm(1+\\beta)R_s/2$ = $\\pm$21.6 kHz',fontsize=7)
ax.set_xlabel('Frecuencia [kHz]'); ax.set_ylabel('PSD relativa [dB]'); ax.set_xlim(-128,128); ax.set_ylim(-80,15); ax.legend(fontsize=7,loc='upper center',bbox_to_anchor=(0.5,-0.22),ncol=3,frameon=False)
fig.tight_layout(); fig.savefig('f2_psd.png'); plt.close()
# --- tiempo canal
fig,ax=plt.subplots(figsize=(6.4,2.6)); t=np.arange(2048)/fs*1e3; y=R[1.0]['y'][4096:4096+2048]
ax.plot(t,y.real,color=C1,lw=.8,label='I'); ax.plot(t,y.imag,color=C2,lw=.6,label='Q')
ti=np.arange(4096+P-1,4096+2048,P); ax.plot((ti-4096)/fs*1e3,np.full(len(ti),2.25),'v',color='k',ms=4,label='impulso (cada 1 ms)')
ax.set_xlabel('Tiempo [ms]'); ax.set_ylabel('Amplitud'); ax.set_ylim(-2.5,2.5); ax.legend(fontsize=7,ncol=3,loc='lower right')
fig.tight_layout(); fig.savefig('f2_tiempo_canal.png'); plt.close()
# --- ojos
fig,axs=plt.subplots(1,4,figsize=(7.2,2.3),sharey=True)
for ax,A in zip(axs,[0.0,0.6,1.0,5.0]):
    z=R[A]['z'].real[2000:2000+Sps*600]
    seg=z[: (len(z)//(2*Sps))*2*Sps].reshape(-1,2*Sps)
    # alinear: el maximo del ojo esta en multiplos de Sps (retardo 88)
    tt=np.arange(2*Sps)/Sps
    for r in seg: ax.plot(tt,r,color=C1,lw=.35,alpha=.35)
    ax.set_title(f'$A_{{imp}}$ = {A}',fontsize=8); ax.set_xlabel('t / T$_s$'); ax.set_ylim(-1.8,1.8)
axs[0].set_ylabel('Salida filtro acoplado (I)')
fig.tight_layout(); fig.savefig('f2_ojos.png'); plt.close()
# --- constelaciones recuperadas
fig,axs=plt.subplots(1,5,figsize=(7.2,1.9),sharey=True)
for ax,A in zip(axs,cases):
    s=R[A]['s'][20:20000]
    ax.plot(s.real,s.imag,'.',ms=1.5,color=C1,alpha=.5); ax.axvline(0,color='k',lw=.6)
    ax.set_xlim(-1.6,1.6); ax.set_ylim(-1.6,1.6); ax.set_aspect('equal'); ax.set_title(f'$A_{{imp}}$={A}\nBER={R[A]["ber"]:.0e}' if R[A]['ber']>0 else f'$A_{{imp}}$={A}\nBER=0',fontsize=7)
    ax.set_xlabel('I',fontsize=7); ax.tick_params(labelsize=6)
axs[0].set_ylabel('Q',fontsize=7)
fig.tight_layout(); fig.savefig('f2_constelaciones.png'); plt.close()
