"""Rebuild BrandFusion blog figures from arXiv:2603.02816v2 and local demo videos.
Requires matplotlib, Pillow and ffmpeg. No network or model calls.
Tables 1 (PDF p6), 3 (p7), 5 (p22); methodology pp3–5.
Images are full decoded video frames, resized uniformly with no content edits.
"""
from pathlib import Path
from html import escape
import csv
import subprocess
import tempfile
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from PIL import Image, ImageDraw, ImageFont

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / 'assets/img/blog/brandfusion'
OUT.mkdir(parents=True, exist_ok=True)
BG, INK, TEAL, MUTED = '#fdfcfa', '#19383c', '#166a6f', '#53686c'
COLORS = ['#64748b', '#b46e24', '#6266aa', TEAL]
plt.rcParams.update({'font.family': 'DejaVu Sans', 'font.size': 12, 'text.color': INK, 'axes.labelcolor': INK, 'xtick.color': INK, 'ytick.color': INK, 'axes.edgecolor': '#becac8', 'svg.fonttype': 'none'})
METHODS = ['Direct append', 'Template rewriting', 'Single rewriting', 'BrandFusion']
# model, method, VBench, CLIPScore, VQAScore, LLMScore, BPR, NS
rows = [
['Veo3',0,.8112,.2671,.8342,.7821,.7221,2.83],['Veo3',1,.8267,.2842,.8756,.9234,.8845,3.12],['Veo3',2,.8289,.2956,.8891,.9412,.8968,3.90],['Veo3',3,.8283,.3274,.9098,.9556,.9474,4.70],
['Sora2',0,.7945,.2645,.8298,.8756,.6434,2.71],['Sora2',1,.8033,.2868,.8712,.9187,.7845,3.84],['Sora2',2,.8029,.2968,.8867,.9368,.8278,3.98],['Sora2',3,.8031,.3177,.9231,.9875,.9066,4.60],
['Kling2.1',0,.7754,.2634,.8276,.8742,.6989,2.65],['Kling2.1',1,.7803,.2855,.8689,.9165,.7812,3.73],['Kling2.1',2,.7883,.2951,.8823,.9351,.8145,3.84],['Kling2.1',3,.7818,.3165,.9208,.9853,.8834,4.48]]
with (OUT/'table-1.csv').open('w') as f:
 w=csv.writer(f); w.writerow(['model','method','VBench_Quality','CLIPScore','VQAScore','LLMScore','BPR','NS'])
 for row in rows: w.writerow([row[0],METHODS[row[1]],*row[2:]])
fig, axes = plt.subplots(1,2,figsize=(12,6.6),facecolor=BG)
for ax, idx, title, lim in [(axes[0],6,'Brand presence rate',1),(axes[1],7,'Integration naturalness',5)]:
 ax.set_facecolor(BG)
 for m in range(4):
  vals=[r[idx] for r in rows if r[1]==m]
  pos=[i+(m-1.5)*.19 for i in range(3)]
  bars=ax.bar(pos,vals,.17,color=COLORS[m],label=METHODS[m],hatch=['//','..','xx',''][m],edgecolor=BG,linewidth=.6,zorder=3)
  for b,v in zip(bars,vals): ax.text(b.get_x()+b.get_width()/2,v+.025*lim,f'{v:.4f}' if idx==6 else f'{v:.2f}',ha='center',va='bottom',fontsize=9,rotation=90)
 ax.set_xticks(range(3),['Veo3','Sora2','Kling2.1']); ax.set_ylim(0,lim*1.2)
 ax.set_yticks([0,.2,.4,.6,.8,1] if idx==6 else range(6)); ax.set_title(title,loc='left',fontweight='bold',pad=18)
 ax.grid(axis='y',color='#dae2df',zorder=0); ax.spines[['top','right']].set_visible(False)
 ax.set_ylabel('Fraction of generated videos' if idx==6 else 'LLM-rated score (1–5)')
fig.suptitle('Recognizability and naturalness improve together',x=.07,y=.97,ha='left',fontsize=19,fontweight='bold')
fig.legend(*axes[0].get_legend_handles_labels(),loc='lower center',bbox_to_anchor=(.5,.06),ncol=4,frameon=False,fontsize=11)
fig.text(.07,.025,'Table 1 · arXiv:2603.02816v2, p. 6 · Aggregate values; uncertainty intervals not reported.',fontsize=10,color=MUTED)
fig.subplots_adjust(left=.07,right=.98,top=.84,bottom=.22,wspace=.27)
fig.savefig(OUT/'main-results.svg',facecolor=BG); fig.savefig('/tmp/brandfusion-main-results.png',dpi=110,facecolor=BG); plt.close(fig)

match = [[3.95,3.21,1.33],[4.01,3.97,1.38],[4.68,4.05,2.97],[4.90,4.78,4.42]]
semantic=[[.8234,.7876,.7353],[.9456,.9178,.9068],[.9512,.9489,.9235],[.9734,.9601,.9333]]
with (OUT/'table-3.csv').open('w') as f:
 w=csv.writer(f);w.writerow(['method','match_level','LLMScore','NS'])
 for j,m in enumerate(METHODS):
  for k,level in enumerate(['High','Medium','Low']): w.writerow([m,level,semantic[j][k],match[j][k]])
fig,ax=plt.subplots(figsize=(10,6.2),facecolor=BG);ax.set_facecolor(BG)
for i,m in enumerate(METHODS):
 ax.plot(range(3),match[i],color=COLORS[i],marker=['s','^','D','o'][i],lw=2.5,label=m)
 for j,v in enumerate(match[i]):
  offset = (-.24 if i==0 else .12) if j<2 else (-.21 if i==0 else .10)
  if i==1 and j==1: offset=-.25
  if i==2 and j==0: offset=-.24
  ax.text(j,v+offset,f'{v:.2f}',ha='center',color=COLORS[i],fontsize=11)
ax.set_xticks(range(3),['High match','Medium match','Low match']);ax.set_xlim(-.18,2.18);ax.set_ylim(1,5.25);ax.set_yticks([1,2,3,4,5]);ax.set_ylabel('Naturalness score (1–5)');ax.grid(axis='y',color='#dae2df');ax.spines[['top','right']].set_visible(False)
ax.set_title('When the brand is harder to place',loc='left',fontsize=20,fontweight='bold',pad=25)
fig.legend(*ax.get_legend_handles_labels(),loc='lower center',bbox_to_anchor=(.5,.07),ncol=4,frameon=False,fontsize=10)
fig.text(.09,.03,'Table 3 · arXiv:2603.02816v2, p. 7 · Lines connect discrete match categories, not a time series.',fontsize=10,color=MUTED)
fig.subplots_adjust(left=.09,right=.96,top=.83,bottom=.23);fig.savefig(OUT/'match-levels.svg',facecolor=BG);fig.savefig('/tmp/brandfusion-match-levels.png',dpi=110,facecolor=BG);plt.close(fig)

variants=['Full BrandFusion','Without strategy agent','Without critic agent','Without strategy + critic']
abl=[[.8283,.3274,.9098,.9556,.9474,4.70],[.8281,.3168,.8945,.9478,.9289,4.42],[.8279,.3021,.8834,.9401,.9045,4.15],[.8275,.2912,.8756,.9278,.8812,3.82]]
with (OUT/'table-5.csv').open('w') as f:
 w=csv.writer(f);w.writerow(['variant','VBench_Quality','CLIPScore','VQAScore','LLMScore','BPR','NS']);w.writerows([[v,*r] for v,r in zip(variants,abl)])
fig,ax=plt.subplots(figsize=(10,5.8),facecolor=BG);ax.set_facecolor(BG)
ax.barh(range(4),[r[-1] for r in abl],color=[TEAL,'#6266aa','#b46e24','#64748b'],height=.55,zorder=3)
for i,r in enumerate(abl):ax.text(r[-1]+.06,i,f'{r[-1]:.2f}',va='center',fontsize=13,fontweight='bold')
ax.set_yticks(range(4),variants);ax.invert_yaxis();ax.set_xlim(0,5.25);ax.set_xticks(range(6));ax.set_xlabel('Naturalness score (1–5; zero baseline shown)');ax.grid(axis='x',color='#dae2df',zorder=0);ax.spines[['top','right','left']].set_visible(False)
fig.suptitle('What do planning and critique contribute?',x=.06,y=.96,ha='left',fontsize=19,fontweight='bold')
fig.text(.06,.07,'Veo3 ablation · Table 5, arXiv:2603.02816v2, p. 22',fontsize=11,color=MUTED)
fig.text(.06,.03,'Published aggregate scores; no error bars or significance claims added.',fontsize=10,color=MUTED)
fig.subplots_adjust(left=.32,right=.95,top=.83,bottom=.21);fig.savefig(OUT/'agent-ablation.svg',facecolor=BG);fig.savefig('/tmp/brandfusion-agent-ablation.png',dpi=110,facecolor=BG);plt.close(fig)

def text(x,y,s,size=24,color=INK,weight='400'):
 return f'<text x="{x}" y="{y}" fill="{color}" font-size="{size}" font-weight="{weight}">{escape(s)}</text>'
def box(x,y,w,h,fill='#eff5f3'):
 return f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="14" fill="{fill}" stroke="#c9dad6"/>'
def arrow(x,y1,y2):
 return f'<path d="M{x},{y1} V{y2}" fill="none" stroke="{TEAL}" stroke-width="2.5" marker-end="url(#arrow)"/>'
s=[f'<svg xmlns="http://www.w3.org/2000/svg" width="900" height="1250" viewBox="0 0 900 1250" role="img" aria-labelledby="title desc"><title id="title">BrandFusion: prepare brand knowledge, then refine the prompt</title><desc id="desc">Offline probing and optional LoRA adaptation populate a knowledge base. Online brand selection, strategy, rewriting, critique and experience learning use that knowledge. The critic evaluates the prompt before video generation.</desc><rect width="900" height="1250" fill="{BG}"/><defs><marker id="arrow" markerWidth="10" markerHeight="10" refX="8" refY="5" orient="auto"><path d="M0,1 L8,5 L0,9" fill="none" stroke="{TEAL}" stroke-width="1.5"/></marker></defs><g font-family="Arial, Helvetica, sans-serif">',text(40,57,'Prepare knowledge. Then refine the prompt.',34,weight='700'),text(40,99,'A shared knowledge base connects two phases.',24,MUTED),box(40,135,820,200,'#f8f1df'),text(65,172,'OFFLINE · advertiser-facing',23,TEAL,'700'),text(65,216,'Probe the video model’s knowledge of the brand.',26),text(65,257,'Sufficient prior → register profile and visual patterns.',24),text(65,297,'Insufficient prior → synthetic videos + LoRA adapter.',24),arrow(450,343,377),box(40,390,820,98),text(65,428,'BRAND KNOWLEDGE BASE · long-term memory',23,TEAL,'700'),text(65,465,'Profiles · optional adapters · successful and failed experiences',22),text(40,535,'ONLINE · user prompt + shared session context',24,TEAL,'700')]
for y,title,desc in [(560,'1  Select a compatible brand','Retrieve the profile and any required adapter.'),(690,'2  Plan an integration strategy','Choose the object, placement and contextual role.'),(820,'3  Rewrite the prompt','Preserve subjects, actions, logic and visual style.'),(950,'4  Critique the rewritten prompt','Accept it, revise its wording, or replan the strategy.')]:
 s += [box(40,y,760,103),text(65,y+38,title,27,weight='700'),text(65,y+77,desc,23)]
 if y<950:s.append(arrow(420,y+108,y+124))
s += ['<path d="M800,1003 H842 V742 H807" fill="none" stroke="#166a6f" stroke-width="2" stroke-dasharray="6 5" marker-end="url(#arrow)"/>',arrow(420,1062,1090),box(40,1100,820,105,'#f8f1df'),text(65,1138,'Generate video → 5  Learn from feedback',27,weight='700'),text(65,1177,'Store experiences for future requests in the knowledge base.',23),text(40,1232,'Method redraw · §4, pp. 3–5 · Critic reviews prompts, not rendered video.',20,MUTED),'</g></svg>']
(OUT/'workflow.svg').write_text('\n'.join(s))

# Real demo examples: use the complete frame and preserve the generation watermark.
examples=[('nike/Serene_Beach_Yoga_Sunrise_Video.mp4',2,'Nike · yoga mat · 00:02'),('nike/Basketball_Dunk_Video_Generated.mp4',4,'Nike · arena banner · 00:04'),('bmw/Businesswoman_s_City_Call.mp4',6,'BMW · key fob · 00:06'),('nike/Fashion_Designer_Creates_Nike_Sportswear.mp4',5,'Nike · studio garment · 00:05')]
font_path='/System/Library/Fonts/Supplemental/Arial.ttf'
font=ImageFont.truetype(font_path,27);small=ImageFont.truetype(font_path,22);titlefont=ImageFont.truetype(font_path,36)
canvas=Image.new('RGB',(1440,1020),BG);draw=ImageDraw.Draw(canvas)
draw.text((30,25),'Four placements from the project’s generated videos',fill=INK,font=titlefont)
manifest=[]
with tempfile.TemporaryDirectory() as tmp:
 for i,(path,sec,label) in enumerate(examples):
  src=ROOT/'brandfusion/examples'/path;dest=Path(tmp)/f'{i}.png'
  subprocess.run(['ffmpeg','-loglevel','error','-y','-ss',str(sec),'-i',str(src),'-frames:v','1',str(dest)],check=True)
  im=Image.open(dest).convert('RGB');im=im.resize((680,383),Image.Resampling.LANCZOS)
  x=30+(i%2)*700;y=105+(i//2)*440
  draw.text((x,y-34),label,fill=INK,font=font);canvas.paste(im,(x,y))
  manifest.append([str(src.relative_to(ROOT)),sec,'full frame; uniformly resized; no content editing'])
draw.text((30,986),'Curated qualitative examples · source video watermarks retained · not a random sample',fill=MUTED,font=small)
canvas.save(OUT/'video-examples.jpg',quality=94)
with (OUT/'video-frames.csv').open('w') as f:
 w=csv.writer(f);w.writerow(['source_video','timestamp_seconds','transformation']);w.writerows(manifest)
print('Wrote five figures and four source CSVs to',OUT)

# Normalize generated text files for clean Git diffs.
for _slug in ['brandfusion']:
    for _path in (Path(__file__).resolve().parents[1] / "assets/img/blog" / _slug).iterdir():
        if _path.suffix in {".svg", ".csv"}:
            _path.write_text("\n".join(line.rstrip() for line in _path.read_text().splitlines()) + "\n")
