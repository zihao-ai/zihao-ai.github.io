"""Rebuild AdvChain's five blog figures and published-data CSVs.

Source: arXiv:2509.24269v1 (29 September 2025), sections 3–4 and Tables 1–4.
Diagrams are explanatory. Numerical values are transcribed, not estimated.
Run with Python 3 + matplotlib. The website has no Python dependency.
"""
from pathlib import Path
from html import escape
import csv
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.colors import LinearSegmentedColormap, Normalize

OUT = Path(__file__).resolve().parents[1] / 'assets/img/blog/advchain'
OUT.mkdir(parents=True, exist_ok=True)
BG, INK, TEAL, MUTED, RUST = '#fdfcfa', '#19383c', '#166a6f', '#53686c', '#ad4a32'

def text(x, y, s, size=24, fill=INK, weight='400', anchor='start'):
    return f'<text x="{x}" y="{y}" fill="{fill}" font-size="{size}" font-weight="{weight}" text-anchor="{anchor}">{escape(s)}</text>'

def rect(x, y, w, h, fill='#edf5f2'):
    return f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="16" fill="{fill}" stroke="#cfddd8"/>'

def start(h, title, desc):
    return [f'<svg xmlns="http://www.w3.org/2000/svg" width="800" height="{h}" viewBox="0 0 800 {h}" role="img" aria-labelledby="title desc">',
            f'<title id="title">{escape(title)}</title><desc id="desc">{escape(desc)}</desc>',
            f'<rect width="800" height="{h}" fill="{BG}"/>',
            f'<defs><marker id="arrow" markerWidth="10" markerHeight="10" refX="8" refY="5" orient="auto"><path d="M0 1 L8 5 L0 9" fill="none" stroke="{TEAL}" stroke-width="1.5"/></marker></defs><g font-family="Arial, Helvetica, sans-serif">']

def arrow(x, y, to_y):
    return f'<path d="M{x} {y} V{to_y}" fill="none" stroke="{TEAL}" stroke-width="2.5" marker-end="url(#arrow)"/>'

def save_svg(name, svg):
    (OUT/name).write_text('\n'.join(svg+['</g></svg>']))

s = start(810, 'Two ways a reasoning chain can drift', 'Conceptual diagram of harmfulness escalation and over-refusal, not a plot of measured scores.')
s += [text(42, 62, 'One recovery problem, two directions', 32, weight='700'),
      text(42, 104, 'A small mistake can shape every step that follows.', 23, MUTED)]
for x, title, steps, fill in [
    (42, 'HARMFUL REQUEST', [('Safe assessment', 'Recognize the risk'), ('Misleading justification', 'Begin rationalizing harm'), ('Harmful compliance', 'The final answer is unsafe')], '#fae9e3'),
    (420, 'BENIGN REQUEST', [('Helpful assessment', 'Engage with the task'), ('Unnecessary hesitation', 'Misread a safe request'), ('Unnecessary refusal', 'The final answer withholds help')], '#f8f1df')]:
    s.append(text(x, 165, title, 21, TEAL, '700'))
    for i, (head, detail) in enumerate(steps):
        y = 195+i*155
        s += [rect(x, y, 338, 112, '#edf5f2' if i==0 else fill),
              text(x+20, y+42, head, 23, weight='700'), text(x+20, y+80, detail, 19)]
        if i<2: s.append(arrow(x+169, y+119, y+145))
s += [rect(42, 680, 716, 86), text(400, 715, 'The target skill: detect a wrong turn and recover.', 25, TEAL, '700', 'middle'),
      text(400, 748, 'A conceptual explanation of §3; no empirical scale.', 20, MUTED, anchor='middle')]
save_svg('two-directions.svg', s)

s = start(930, 'Training recovery instead of only ideal paths', 'AdvChain rewrites existing safe reasoning into 800 temptation-correction and 200 hesitation-correction examples, then uses supervised fine-tuning.')
s += [text(42, 60, 'Put recovery into the training example', 32, weight='700'), text(42, 100, 'The final response remains appropriate to the request.', 23, MUTED)]
for x, title, origin, mid, correction, final, count in [
    (42,'Temptation–Correction','Harmful prompt + safe reasoning','Flawed justification','Recognize and reject the drift','Safe final response','800 examples'),
    (420,'Hesitation–Correction','Benign prompt + helpful reasoning','Unnecessary caution','Recognize the false alarm','Helpful final response','200 examples')]:
    s += [text(x, 156, title, 23, TEAL, '700'), text(x, 187, count, 21, MUTED)]
    for i,(head,fill) in enumerate([(origin,'#edf5f2'),(mid,'#fae9e3'),(correction,'#edf5f2'),(final,'#edf5f2')]):
        y=216+i*118
        s += [rect(x,y,338,78,fill), text(x+169,y+46,head,18,anchor='middle')]
        if i<3:s.append(arrow(x+169,y+84,y+109))
s += [f'<path d="M211 656 V694 H589 V656 M400 694 V730" fill="none" stroke="{TEAL}" stroke-width="2.5" marker-end="url(#arrow)"/>',
      rect(42,745,716,114),text(400,786,'Supervised fine-tuning on 1,000 examples',26,TEAL,'700','middle'),
      text(400,826,'Learn the whole corrected trajectory and final response.',22,anchor='middle'),
      text(42,902,'Source: arXiv:2509.24269v1, §4 and §5.1. Explanatory diagram.',19,MUTED)]
save_svg('recovery-training.svg',s)

# Exact table transcriptions, retaining two decimal places in the downloadable CSVs.
benchmarks=['HarmBench','StrongReject','WJ-VaniHarm','SafeUnlearning','WJ-AdvHarm']
general={
'DeepSeek-R1-7B':[
('Base', [51.00,45.05,28.46,45.35,26.00]),
('STAR-1 (1k)',[8.00,6.00,11.67,28.05,17.33]),
('SafeChain (1k)',[38.00,38.00,24.67,39.65,24.00]),
('UnsafeChain (1k)',[26.00,27.00,12.67,34.86,19.33]),
('RealSafe-R1 (15k)',[2.00,2.50,.20,8.14,4.80]),
('AdvChain (1k)',[4.50,2.00,2.00,9.30,9.00])],
'Qwen3-4B':[
('Base',[24.00,9.50,6.60,79.07,24.80]),
('STAR-1 (1k)',[2.50,.50,.67,37.21,13.33]),
('SafeChain (1k)',[33.00,21.00,12.00,36.05,19.33]),
('UnsafeChain (1k)',[17.00,7.50,11.33,52.33,20.66]),
('AdvChain (1k)',[4.00,1.00,.67,17.44,10.68])]
}
with (OUT/'general-safety-table1.csv').open('w',newline='') as f:
    w=csv.writer(f); w.writerow(['family','method', *[b+'_ASR_percent' for b in benchmarks]])
    for fam,rows in general.items():
        for method, vals in rows:w.writerow([fam,method,*[f'{v:.2f}' for v in vals]])

plt.rcParams.update({'font.family':'DejaVu Sans','font.size':13,'text.color':INK,'axes.labelcolor':INK,'xtick.color':MUTED,'ytick.color':INK,'svg.fonttype':'none'})
cmap=LinearSegmentedColormap.from_list('safety',['#eef5f2','#85b7b0','#125c63'])
fig,axs=plt.subplots(2,1,figsize=(10,10),facecolor=BG,gridspec_kw={'height_ratios':[6,5]})
fig.subplots_adjust(left=.27,right=.97,top=.80,bottom=.12,hspace=.50)
for ax,(fam,rows) in zip(axs,general.items()):
    vals=[row[1] for row in rows]
    im=ax.imshow(vals,cmap=cmap,norm=Normalize(0,100),aspect='auto')
    ax.set_xticks(range(5),['HarmBench','StrongReject','WJ vanilla\nharmful','Safe-\nUnlearning','WJ adversarial\nharmful'],fontsize=11)
    ax.xaxis.tick_top();ax.tick_params(axis='both',length=0,pad=8)
    ax.set_yticks(range(len(rows)),[row[0] for row in rows],fontsize=12)
    for i,row in enumerate(vals):
        for j,val in enumerate(row): ax.text(j,i,f'{val:.2f}',ha='center',va='center',fontsize=14,weight='bold',color='white' if val>=65 else INK)
    ax.set_title(fam,loc='left',pad=51,fontsize=18,weight='bold')
    for spine in ax.spines.values():spine.set_visible(False)
    ax.set_xticks([i-.5 for i in range(6)],minor=True);ax.set_yticks([i-.5 for i in range(len(rows)+1)],minor=True)
    ax.grid(which='minor',color=BG,lw=3);ax.tick_params(which='minor',length=0)
fig.text(.04,.955,'Safety improves, but no method wins every test',size=21,weight='bold')
fig.text(.04,.916,'Final-answer attack success rate (%) · lower is better',size=15,color=MUTED)
cax=fig.add_axes([.27,.065,.7,.015]);cb=fig.colorbar(im,cax=cax,orientation='horizontal',ticks=[0,25,50,75,100]);cb.outline.set_visible(False);cb.ax.tick_params(labelsize=10,length=0)
fig.text(.04,.018,'Source: Table 1, p. 7. Two model families shown; exact reported point estimates.',size=11,color=MUTED)
fig.savefig(OUT/'general-safety.svg',facecolor=BG);plt.close(fig)

# Table 2 ASR/RR and Table 3 over-refusal. The chart uses XSTest ORR; CSV includes WJ.
balance={
'DeepSeek-R1-7B':[
('Base',74.67,35.33,16.80,10.40),('STAR-1',54.67,43.33,42.00,33.33),
('SafeChain',44.00,58.00,28.80,14.67),('UnsafeChain',60.67,45.33,24.80,21.33),
('RealSafe-R1 (15k)',14.67,84.67,66.40,60.60),('AdvChain',9.33,74.00,18.00,12.67)],
'Qwen3-4B':[
('Base',30.00,72.67,10.80,16.00),('STAR-1',12.67,82.67,26.80,22.00),
('SafeChain',14.00,68.00,15.40,20.67),('UnsafeChain',39.33,62.00,16.00,22.33),
('AdvChain',8.67,84.00,12.50,18.00)]}
with (OUT/'safety-utility-tables2-3.csv').open('w',newline='') as f:
    w=csv.writer(f);w.writerow(['family','method','CoT_Hijack_ASR_percent','CoT_Hijack_RR_percent','XSTest_ORR_percent','WJ_Benign_ORR_percent'])
    for fam,rows in balance.items():
        for row in rows:w.writerow([fam,row[0],*[f'{v:.2f}' for v in row[1:]]])
fig,axs=plt.subplots(2,1,figsize=(10,10.5),facecolor=BG)
fig.subplots_adjust(left=.13,right=.96,top=.85,bottom=.105,hspace=.50)
positions={
'DeepSeek-R1-7B':{'Base':(-8,-22),'STAR-1':(10,8),'SafeChain':(-8,12),'UnsafeChain':(10,-20),'RealSafe-R1 (15k)':(12,-4),'AdvChain':(12,-4)},
'Qwen3-4B':{'Base':(12,-5),'STAR-1':(12,6),'SafeChain':(20,-5),'UnsafeChain':(12,4),'AdvChain':(-6,-26)}}
for ax,(fam,rows) in zip(axs,balance.items()):
    ax.set_facecolor(BG)
    for method,asr,rr,orr,wj in rows:
        adv=method=='AdvChain';base=method=='Base'
        ax.scatter(asr,orr,s=120 if adv else 75,color=TEAL if adv else MUTED,marker='*' if adv else ('s' if base else 'o'),zorder=3)
        dx,dy=positions[fam][method]
        ax.annotate(method,(asr,orr),xytext=(dx,dy),textcoords='offset points',ha='right' if dx<0 else 'left',fontsize=12,weight='bold' if adv else 'normal',color=TEAL if adv else INK)
    ax.set(xlim=(0,100),ylim=(0,80),xlabel='CoT-Hijack attack success (%) ↓',ylabel='XSTest over-refusal (%) ↓')
    ax.set_title(fam,loc='left',fontweight='bold',fontsize=18,pad=12)
    ax.grid(alpha=.18);ax.set_axisbelow(True)
    for spine in ['top','right']:ax.spines[spine].set_visible(False)
    ax.text(.98,.94,'Lower left is better',transform=ax.transAxes,ha='right',va='top',fontsize=12,color=MUTED)
fig.text(.04,.955,'Resisting hijacking without refusing everything',size=21,weight='bold')
fig.text(.04,.918,'Different test sets, separate denominators · no combined score',size=15,color=MUTED)
fig.text(.04,.035,'Source: Tables 2–3, p. 8. CoT-Hijack: 150 samples. Reported point estimates.',size=11,color=MUTED)
fig.savefig(OUT/'safety-utility.svg',facecolor=BG);plt.close(fig)

reasoning={'DeepSeek-R1-7B':([92.80,51.30,37.60],[93.40,49.33,36.50]),'Qwen3-4B':([97.00,71.35,53.03],[96.20,69.50,52.40])}
with (OUT/'reasoning-table4.csv').open('w',newline='') as f:
    w=csv.writer(f);w.writerow(['family','benchmark','base_Pass1_percent','AdvChain_Pass1_percent'])
    for fam,(base,adv) in reasoning.items():
        for b,a,c in zip(['Math-500','AIME 2024','LiveCodeBench'],base,adv):w.writerow([fam,b,f'{a:.2f}',f'{c:.2f}'])
fig,axs=plt.subplots(2,1,figsize=(10,8),facecolor=BG)
fig.subplots_adjust(left=.23,right=.91,top=.79,bottom=.12,hspace=.60)
for ax,(fam,(base,adv)) in zip(axs,reasoning.items()):
    ax.set_facecolor(BG)
    for i,(a,b) in enumerate(zip(base,adv)):
        ax.barh(i+.16,a,height=.28,color='#809499',label='Base' if i==0 else None)
        ax.barh(i-.16,b,height=.28,color=TEAL,label='AdvChain' if i==0 else None)
        ax.text(a+1.3,i+.16,f'{a:.2f}',va='center',fontsize=12)
        ax.text(b+1.3,i-.16,f'{b:.2f}',va='center',fontsize=12,weight='bold',color=TEAL)
    ax.set_yticks([0,1,2],['Math-500','AIME 2024','LiveCodeBench']);ax.invert_yaxis()
    ax.set_xlim(0,105);ax.set_xticks([0,25,50,75,100]);ax.set_xlabel('Pass@1 (%) ↑');ax.set_title(fam,loc='left',pad=14,fontsize=18,weight='bold')
    ax.grid(axis='x',alpha=.18);ax.set_axisbelow(True);ax.tick_params(axis='y',length=0)
    for spine in ax.spines.values():spine.set_visible(False)
handles,labels=axs[0].get_legend_handles_labels();fig.legend(handles,labels,loc='upper right',bbox_to_anchor=(.94,.90),ncol=2,frameon=False)
fig.text(.04,.95,'Reasoning scores stay close, with small declines',size=21,weight='bold')
fig.text(.04,.90,'Single-attempt accuracy · higher is better',size=15,color=MUTED)
fig.text(.04,.035,'Source: Table 4, p. 8. No uncertainty intervals reported; differences are descriptive.',size=11,color=MUTED)
fig.savefig(OUT/'reasoning-capability.svg',facecolor=BG);plt.close(fig)
print(f'Wrote five SVGs and three CSVs to {OUT}')

# Normalize generated text files for clean Git diffs.
for _slug in ['advchain']:
    for _path in (Path(__file__).resolve().parents[1] / "assets/img/blog" / _slug).iterdir():
        if _path.suffix in {".svg", ".csv"}:
            _path.write_text("\n".join(line.rstrip() for line in _path.read_text().splitlines()) + "\n")
