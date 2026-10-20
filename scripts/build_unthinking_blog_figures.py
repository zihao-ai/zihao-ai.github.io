"""Regenerate five Unthinking blog figures and exact-value CSVs.
Source: arXiv:2502.12202v2 (16 May 2025), §§3–5, Tables 1, 2, 5, 6.
Run: python scripts/build_unthinking_blog_figures.py (requires matplotlib).
"""
from pathlib import Path
from html import escape
import csv
import argparse
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np

parser = argparse.ArgumentParser()
parser.add_argument('--figure', choices=['all', 'bot-success'], default='all')
SELECTED = parser.parse_args().figure

OUT = Path(__file__).resolve().parents[1] / 'assets/img/blog/unthinking'
OUT.mkdir(parents=True, exist_ok=True)
PREVIEW = Path('/tmp/unthinking-blog')
PREVIEW.mkdir(parents=True, exist_ok=True)
BG, INK, MUTED, TEAL, RED, GOLD = '#fdfcfa', '#19383c', '#53686c', '#166a6f', '#b34d37', '#b68a35'
plt.rcParams.update({'font.family': 'DejaVu Sans', 'font.size': 13, 'svg.fonttype': 'none', 'axes.labelcolor': INK, 'xtick.color': MUTED, 'ytick.color': INK, 'text.color': INK})

def start(h, title, desc):
    return [f'<svg xmlns="http://www.w3.org/2000/svg" width="1000" height="{h}" viewBox="0 0 1000 {h}" role="img" aria-labelledby="title desc"><title id="title">{escape(title)}</title><desc id="desc">{escape(desc)}</desc><rect width="1000" height="{h}" fill="{BG}"/><defs><marker id="arrow" markerWidth="9" markerHeight="9" refX="7" refY="4" orient="auto"><path d="M0 0 L8 4 L0 8" fill="none" stroke="{MUTED}" stroke-width="1.5"/></marker></defs><g font-family="Arial, Helvetica, sans-serif">']
def text(x,y,s,size=24,color=INK,weight='400',anchor='start'):
    return f'<text x="{x}" y="{y}" font-size="{size}" fill="{color}" font-weight="{weight}" text-anchor="{anchor}">{escape(s)}</text>'
def rect(x,y,w,h,color):
    return f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="12" fill="{color}"/>'
def line(x1,y1,x2,y2,color=MUTED,dash=False):
    return f'<path d="M{x1} {y1} L{x2} {y2}" stroke="{color}" stroke-width="3" fill="none"'+(' stroke-dasharray="7 6"' if dash else '')+' marker-end="url(#arrow)"/>'
def save_svg(name,s):
    if SELECTED == 'bot-success' and name != 'bot-success-table.svg': return
    (OUT/name).write_text('\n'.join(s+['</g></svg>']))
def csvsave(name,headers,rows):
    if SELECTED == 'bot-success' and name != 'bot-success.csv': return
    with (OUT/name).open('w',newline='') as f:
        w=csv.writer(f); w.writerow(headers); w.writerows(rows)
def clean(ax):
    ax.set_facecolor(BG)
    for sp in ax.spines.values(): sp.set_visible(False)
    ax.tick_params(length=0,pad=9)
    ax.set_axisbelow(True)
def save(fig,name,title,desc):
    if SELECTED == 'bot-success':
        plt.close(fig)
        return
    fig.savefig(OUT/name,facecolor=BG,metadata={'Title':title,'Description':desc})
    fig.savefig(PREVIEW/name.replace('.svg','.png'),dpi=130,facecolor=BG)
    plt.close(fig)

s=start(650,'A boundary that changes model behavior','Conceptual comparison of normal reasoning, unauthorized suppression, and owner-authorized monitoring. Widths do not encode measured token counts.')
s += [text(45,65,'Who controls the end of thinking?',38,weight='700'),text(45,108,'The same phase boundary can support an attack or a useful control.',24,MUTED)]
rows=[(160,'Normal generation',620,'#deece8','Reasoning continues','Final answer'),(300,'BoT: unauthorized suppression',120,'#f3d7cf','Skipped','Early answer'),(440,'MoT: owner-authorized stop',365,'#e8e1c8','Reasoning until sufficient','Final answer')]
for y,label,w,color,phase,answer in rows:
    s += [text(45,y,label,25,weight='700'),rect(45,y+20,w,60,color),text(45+w/2,y+59,phase,22,anchor='middle'),line(55+w,y+50,85+w,y+50),rect(95+w,y+20,190,60,'#e9edee'),text(190+w,y+59,answer,22,anchor='middle')]
    if label.startswith('MoT'):
        s += [text(45,y+118,'Monitor judges sufficiency or risk; the owner controls intervention.',21,TEAL)]
s += [text(45,618,'Conceptual timeline · lengths are schematic · source: paper §§3–5',19,MUTED)]
save_svg('thinking-boundary.svg',s)

s=start(870,'Different access, different authority','Training-based BoT changes a learned conditional behavior via poisoned training data. Training-free BoT alters inference inputs without changing weights. Owner-controlled MoT assesses reasoning and can stop it.')
s += [text(45,62,'Three routes to a shorter reasoning trace',35,weight='700'),text(45,105,'Access and authorization determine what the intervention means.',24,MUTED)]
for x,title,sub in [(45,'Training-based BoT','Attacker controls training data'),(520,'Training-free BoT','Attacker controls inference input')]:
    s += [rect(x,145,435,315,'#f8e9e3'),text(x+24,189,title,28,RED,'700'),text(x+24,226,sub,23),text(x+24,281,'Poisoned learning signal' if x==45 else 'Adversarial input influence',24,weight='700'),text(x+24,319,'Conditional behavior is learned' if x==45 else 'Model weights remain unchanged',22),line(x+218,340,x+218,376),text(x+218,414,'Reasoning is suppressed',25,RED,'700','middle')]
s += [rect(45,500,910,265,'#e5efeb'),text(69,547,'Monitoring of Thought',29,TEAL,'700'),text(69,586,'Model owner controls the generation process',24),text(69,637,'Reasoning trace',25,weight='700'),line(270,630,335,630),text(360,637,'External monitor',25,weight='700'),line(562,630,630,630),text(659,637,'Continue or stop',25,weight='700'),text(69,700,'Efficiency: sufficient evidence     Safety: emerging harmful direction',23),text(69,739,'Stopping is a policy decision; correctness and safety still need evaluation.',22,MUTED),text(45,825,'Conceptual summary · source: paper §§4–5 · no attack payloads shown',20,MUTED)]
save_svg('control-paths.svg',s)

names=['DeepSeek-R1-1.5B','DeepSeek-R1-7B','DeepSeek-R1-14B','DeepSeek-R1-32B','Marco-o1-7B','Light-R1-7B-DS','Open-R1-7B','QwQ']
training_math=[97.6,100,100,99.8,99.8,100,100,100]
free_math=[100,97,99,94.2,91.4,100,86.19,100]
training_aime=[100,100,100,100,90,100,100,100]
free_aime=[100,100,93.3,86.6,100,100,73.33,100]
csvsave('bot-success.csv',['model','training_based_math500_asr_percent','training_free_whitebox_math500_asr_percent','training_based_aime2024_asr_percent','training_free_whitebox_aime2024_asr_percent'],zip(names,training_math,free_math,training_aime,free_aime))
# The results are near ceiling: an explicit table is clearer than overlapping dots.
# Preserve all 32 values; no stretched color scale or implied error bars.
s=start(890,'BoT: how often is thinking suppressed?',
        'All 32 ASR values from Tables 1 and 2. Twenty values equal 100 percent. Columns distinguish datasets and attack access conditions.')
s += [text(35,58,'BoT: how often is thinking suppressed?',34,weight='700'),
      text(35,101,'ASR = inputs that skip thinking / evaluated inputs × 100%',24,MUTED),
      text(35,140,'20 of the 32 reported results are 100%. These are not answer accuracies.',22,MUTED)]
centers=[397,565,733,901]
s += [rect(315,178,332,50,'#e5efeb'),rect(651,178,332,50,'#e5efeb'),
      text(481,212,'MATH-500',26,TEAL,'700','middle'),
      text(817,212,'AIME 2024',26,TEAL,'700','middle'),
      text(35,272,'Model',23,weight='700')]
for x,label in zip(centers,['Training-based','Training-free','Training-based','Training-free']):
    s.append(text(x,268,label,20,weight='700',anchor='middle'))
s.append('<path d="M25 289 H983" stroke="#aebfbd" stroke-width="1.5"/>')
for i,name in enumerate(names):
    y=292+i*53
    if i%2==0:s.append(rect(25,y,958,53,'#f0f4f3'))
    s.append(text(35,y+35,name,22))
    for x,v in zip(centers,[training_math[i],free_math[i],training_aime[i],free_aime[i]]):
        s.append(text(x,y+35,f'{v:.2f}%',23,INK,'500','middle'))
s += ['<path d="M649 178 V716" stroke="#c5d4d1" stroke-width="2"/>',
      text(35,756,'Training-based: SFT with a semantic trigger (Table 1).',21,MUTED),
      text(35,794,'Training-free: white-box optimization for each input (Table 2).',21,MUTED),
      text(35,839,'Different attack settings; neither column is a clean-model baseline.',21,TEAL),
      text(35,875,'Source: arXiv:2502.12202v2, p. 6. Published values, not a new replication.',18,MUTED)]
save_svg('bot-success-table.svg',s)

sizes=['1.5B','7B','14B','32B']
rtc_math=[-71.78,-68.98,-69.87,-73.50];rpc_math=[7.57,1.51,.42,1.24]
rtc_aime=[-69.14,-60.25,-55.48,-63.02];rpc_aime=[15.31,11.75,5.26,1.01]
csvsave('mot-efficiency.csv',['deepseek_r1_model_size','math500_relative_token_change_percent','math500_relative_pass1_change_percent','aime2024_relative_token_change_percent','aime2024_relative_pass1_change_percent'],zip(sizes,rtc_math,rpc_math,rtc_aime,rpc_aime))
fig,axes=plt.subplots(1,2,figsize=(11,7),facecolor=BG)
fig.subplots_adjust(left=.09,right=.96,top=.72,bottom=.32,wspace=.37)
y=np.arange(4)
for ax,a,b,title,lim in zip(axes,[rtc_math,rpc_math],[rtc_aime,rpc_aime],['Generated tokens','Pass@1 accuracy'],[(-80,0),(0,19)]):
    clean(ax); ax.barh(y-.18,a,height=.30,color=TEAL,label='MATH-500');ax.barh(y+.18,b,height=.30,color=GOLD,label='AIME 2024')
    ax.set_yticks(y,sizes);ax.invert_yaxis();ax.set_xlim(*lim);ax.set_title(title,fontsize=17,weight='bold',pad=17);ax.grid(axis='x',alpha=.17);ax.set_xlabel('Relative change from baseline (%)',fontsize=11,labelpad=14)
    for vals,offset in [(a,-.18),(b,.18)]:
        for i,v in enumerate(vals):
            label=f'{v:+.2f}'
            ax.text(v+(1.4 if v>0 else -1),i+offset,label,va='center',ha='left' if v>0 else 'right',fontsize=10,color=INK)
axes[0].set_ylabel('DeepSeek-R1 model',fontsize=12)
# Keep negative labels readable inside the plotting interval.
axes[0].set_xlim(-91,0)
fig.text(.045,.94,'Shorter reasoning can preserve performance',size=24,weight='bold')
fig.text(.045,.885,'MoT with GPT-4o-mini monitoring once every 200 thinking tokens',size=14,color=MUTED)
handles,labels=axes[0].get_legend_handles_labels();fig.legend(handles,labels,loc='lower center',bbox_to_anchor=(.5,.105),ncol=2,frameon=False)
fig.text(.045,.06,'Relative change = (MoT − baseline) / baseline × 100. Accuracy changes are not percentage points.',size=10,color=MUTED)
fig.text(.045,.025,'Source: Table 5, p. 8. Generated-token savings do not include the monitor’s full deployment cost.',size=10,color=MUTED)
save(fig,'mot-efficiency.svg','MoT relative token and performance changes','Exact Table 5 values for the four DeepSeek-R1 models; two separate axes for relative token and pass@1 changes.')

base=[[81.47,54.63,38.66,34.50],[86,63,46.50,46],[44,52,46,41]]
mot=[[1.92,.96,0,.32],[10,6,2,4],[6,8,5,3]]
datasets=['StrongReject','HarmBench','WildJailbreak']
csvsave('mot-safety.csv',['dataset','deepseek_r1_model_size','baseline_jailbreak_asr_percent','mot_jailbreak_asr_percent'],[(d,n,b,a) for d,bs,ms in zip(datasets,base,mot) for n,b,a in zip(sizes,bs,ms)])
fig,axes=plt.subplots(1,3,figsize=(11,6.8),sharey=True,facecolor=BG)
fig.subplots_adjust(left=.09,right=.97,top=.73,bottom=.34,wspace=.21)
y=np.arange(4)
for ax,d,bs,ms in zip(axes,datasets,base,mot):
    clean(ax); ax.set_title(d,fontsize=16,weight='bold',pad=18);ax.set_xlim(-6,104);ax.set_xticks([0,50,100]);ax.grid(axis='x',alpha=.15)
    for i,(b,m) in enumerate(zip(bs,ms)):
        ax.plot([m,b],[i,i],color='#bccbc7',lw=4,zorder=1)
        ax.text(b,i-.20,f'{b:g}',ha='center',fontsize=10,color=RED)
        ax.text(m,i+.29,f'{m:g}',ha='center',fontsize=10,color=TEAL)
    ax.scatter(bs,y,s=60,color=RED,label='Original model',zorder=3);ax.scatter(ms,y,s=60,color=TEAL,label='With MoT',zorder=3)
    ax.set_xlabel('Jailbreak ASR (%)',labelpad=15,fontsize=12)
axes[0].set_yticks(y,sizes);axes[0].set_ylim(3.55,-.55);axes[0].set_ylabel('DeepSeek-R1 model',fontsize=12)
fig.text(.045,.94,'An owner-controlled monitor improves safety',size=24,weight='bold')
fig.text(.045,.885,'Llama-Guard–judged jailbreak ASR · lower is better',size=14,color=MUTED)
handles,labels=axes[0].get_legend_handles_labels();fig.legend(handles,labels,loc='lower center',bbox_to_anchor=(.5,.11),ncol=2,frameon=False)
fig.text(.045,.06,'Source: Table 6, p. 9. Here ASR measures jailbreak outcomes, not suppression of thinking.',size=11,color=MUTED)
fig.text(.045,.025,'Benchmark and evaluator specific; a low observed ASR is not a guarantee of safe output.',size=11,color=MUTED)
save(fig,'mot-safety.svg','MoT jailbreak attack success rates','Exact Table 6 jailbreak ASR before and after owner-controlled MoT, across three safety benchmarks. All axes use 0–100 percent ticks.')
print('Created BoT ASR table and CSV.' if SELECTED == 'bot-success' else 'Created five SVGs, three CSVs, and two temporary PNG previews.')

# Normalize generated text files for clean Git diffs.
for _slug in ['unthinking']:
    for _path in (Path(__file__).resolve().parents[1] / "assets/img/blog" / _slug).iterdir():
        if _path.suffix in {".svg", ".csv"}:
            _path.write_text("\n".join(line.rstrip() for line in _path.read_text().splitlines()) + "\n")
