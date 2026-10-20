"""Rebuild original blog diagrams and paper-derived plots (requires matplotlib).
Sources: EARBench arXiv:2408.04449v5; VDC arXiv:2309.16211v2.
No empirical values are inferred from generated cover images.
"""
from pathlib import Path
from html import escape
import csv
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np
ROOT = Path(__file__).resolve().parents[1] / 'assets/img/blog'
BG, INK, TEAL, RED, MUTED = '#fdfcfa', '#19383c', '#166a6f', '#ad4a32', '#53686c'
plt.rcParams.update({'font.family':'DejaVu Sans','font.size':13,'text.color':INK,'axes.labelcolor':INK,'xtick.color':MUTED,'ytick.color':INK,'axes.spines.top':False,'axes.spines.right':False,'axes.spines.left':False,'axes.edgecolor':'#c9dad6','svg.fonttype':'none','figure.facecolor':BG,'axes.facecolor':BG,'savefig.facecolor':BG})

def save_csv(slug,name,header,rows):
    with (ROOT/slug/(name+'.csv')).open('w') as f:
        w=csv.writer(f);w.writerow(header);w.writerows(rows)

def txt(x,y,s,size=25,color=INK,bold=False):
    return f'<text x="{x}" y="{y}" font-size="{size}" fill="{color}" font-weight="{700 if bold else 400}">{escape(s)}</text>'

def diagram(slug,name,title,subtitle,steps,footer):
    height=180+len(steps)*170+50
    svg=[f'<svg xmlns="http://www.w3.org/2000/svg" width="800" height="{height}" viewBox="0 0 800 {height}" role="img" aria-labelledby="title desc"><title id="title">{escape(title)}</title><desc id="desc">{escape(subtitle)}</desc><rect width="800" height="{height}" fill="{BG}"/><g font-family="Arial, Helvetica, sans-serif">',txt(40,60,title,33,bold=True),txt(40,103,subtitle,23,MUTED)]
    for i,(heading,one,two) in enumerate(steps):
        y=140+i*170
        svg.extend([f'<rect x="40" y="{y}" width="720" height="135" rx="15" fill="{["#eff5f3","#f8f1df","#edf1f7"][i%3]}" stroke="#c9dad6"/>',txt(62,y+40,heading,27,bold=True),txt(62,y+79,one,25),txt(62,y+113,two,25)])
        if i<len(steps)-1:svg.append(f'<path d="M400,{y+142} v19 m-7,-7 l7,7 l7,-7" stroke="{TEAL}" fill="none" stroke-width="3"/>')
    svg.extend([txt(40,height-25,footer,19,MUTED),'</g></svg>'])
    (ROOT/slug/(name+'.svg')).write_text('\n'.join(svg))

def bars(slug,name,title,subtitle,labels,series,limits,foot):
    n=len(labels);fig,axes=plt.subplots(1,len(series),figsize=(12,max(4.8,n*.45+2.5)),sharey=True,squeeze=False)
    axes=axes[0];y=np.arange(n)
    for ax,(metric,values,color),limit in zip(axes,series,limits):
        colors=[TEAL if label=='VDC' else color for label in labels]
        ax.barh(y,values,height=.58,color=colors)
        ax.set_xlim(0,limit);ax.set_title(metric,loc='left',fontsize=14,pad=13,fontweight='bold');ax.set_yticks(y,labels);ax.tick_params(axis='y',length=0,pad=9);ax.grid(axis='x',alpha=.17);ax.set_axisbelow(True)
        for yi,v in zip(y,values):
            inside=v>limit*.86
            ax.text(v-limit*.015 if inside else v+limit*.015,yi,f'{v:.2f}',va='center',ha='right' if inside else 'left',fontsize=11,color='white' if inside else INK)
    axes[0].invert_yaxis()
    fig.suptitle(title,x=.02,y=.985,ha='left',fontsize=19,fontweight='bold')
    fig.text(.02,.87,subtitle,fontsize=12,color=MUTED)
    fig.text(.02,.025,foot,fontsize=10,color=MUTED)
    fig.subplots_adjust(left=.23,right=.97,top=.73,bottom=.14,wspace=.17)
    fig.savefig(ROOT/slug/(name+'.svg'));plt.close(fig)

for slug in ['earbench','vdc']:(ROOT/slug).mkdir(parents=True,exist_ok=True)
diagram('earbench','planning-gap','Two questions for the same plan','A kitchen example, simplified from the paper’s case study.',[
('The instruction','Heat a pie. The observation says that it is','wrapped in aluminum foil.'),
('Executability: can the robot do this?','A robot may have all the actions needed','to carry out the proposed plan.'),
('Safety: should this plan be executed?','The plan must account for material properties','and the safety constraints of the appliance.'),
('The missing bridge','Task completion requires checking consequences,','not merely listing available actions.')], 'Conceptual explanation · not a robot rollout or incident record')
diagram('earbench','framework','How EARBench evaluates plans','Four modules connect a safety rule to a testable scenario.',[
('01  Generate safety guidelines','Create domain-specific safety tips; filter them','for applicability to embodied tasks.'),
('02  Construct risky scenarios','Combine task, objects and environment context','with a textual or synthetic visual observation.'),
('03  Ask the target model for a plan','Provide robot capabilities and scenario context;','collect a sequence of high-level actions.'),
('04  Evaluate risk and executability','Judge potential risk using the reference tip;','assess whether the plan fits the robot’s skills.')], 'Source: EARBench v5, framework and methods · simplified diagram')
rows=[['GPT-4o',94.03,96.53],['Llama 3.1-70B',95.51,94.24]]
save_csv('earbench','risk-and-effectiveness',['model','TRR_percent','TER_percent'],rows)
bars('earbench','risk-and-effectiveness','An executable plan can still carry risk','Two independent evaluator-derived rates; neither is real-world success.',[r[0] for r in rows],[('Task Risk Rate (%) ↓',[r[1] for r in rows],RED),('Task Effectiveness Rate (%) ↑',[r[2] for r in rows],TEAL)],[100,100],'Source: EARBench v5 §2.3.1 · selected models, reported point estimates')
rows=[['GPT-4o',94.53,45.64],['Llama 3.1-70B',95.51,67.85]]
save_csv('earbench','prompt-mitigation',['model','baseline_TRR_percent','explicit_tips_TRR_percent_approx'],rows)
bars('earbench','prompt-mitigation','Specific safety context helps, but leaves residual risk','Textual scenarios · Task Risk Rate (%) ↓ · relevant safety tips supplied.',[r[0] for r in rows],[('Baseline',[r[1] for r in rows],RED),('With explicit safety tips ≈',[r[2] for r in rows],TEAL)],[100,100],'Source: EARBench v5 §2.3.3 + §2.4 / Fig. 5 · reported approximate values')
rows=[['Without safety tips',.48],['With safety tips',.85]]
save_csv('earbench','evaluation-agreement',['evaluator_condition','cohen_kappa_approx'],rows)
bars('earbench','evaluation-agreement','Giving the evaluator a concrete safety criterion','200 sampled instances · five human annotators · majority human judgment.',[r[0] for r in rows],[('Cohen’s κ (reported approximately)',[r[1] for r in rows],TEAL)],[1],'Source: EARBench v5 §2.3.5 / Fig. 4d · agreement is not proof of physical safety')

diagram('vdc','label-gap','Different causes, one semantic mismatch','An illustrative image depicts a dog; the stored label says “cat”.',[
('Accidental label noise','The label was corrupted during annotation','or dataset processing.'),
('A dirty-label backdoor sample','An attacker changes the label and adds a trigger.','The image’s main semantic content still disagrees.'),
('A shared detection opportunity','Ask whether the visible evidence supports','the supplied class label.'),
('A boundary: clean-label poisoning','If the image and label still agree, this signal','does not establish whether the sample is poisoned.')], 'Conceptual examples · not samples from the experimental datasets')
diagram('vdc','pipeline','Ask the label. Check the image.','VDC uses existing language and vision-language models.',[
('01  VQG: prepare questions and expected answers','General questions ask about the whole image.','Label-specific questions probe class attributes.'),
('02  VQA: answer from the visual evidence','The multimodal model responds to each question','using the actual image.'),
('03  VAE: evaluate answer agreement','A language model judges open-ended descriptions;','yes/no matching handles label-specific answers.'),
('04  Vote across the questions','Score = fraction of answers judged consistent.','The paper removes samples with score < 0.5.')], 'Source: VDC v2 §4–5 · “consistent” means consistent with the supplied label')
rows=[['CIFAR-10 / symmetric',98.81,2.61],['CIFAR-10 / asymmetric',99.60,2.62],['ImageNet-100 / symmetric',94.79,1.55],['ImageNet-100 / asymmetric',92.34,1.55],['ImageNet-Dog / symmetric',97.30,7.90],['ImageNet-Dog / asymmetric',91.97,7.90]]
save_csv('vdc','noise-detection',['dataset_and_noise','TPR_percent','FPR_percent'],rows)
bars('vdc','noise-detection','Finding mislabeled images across datasets','VDC · 40% synthetic label noise · each metric has its own denominator.',[r[0] for r in rows],[('Dirty samples detected: TPR (%) ↑',[r[1] for r in rows],TEAL),('Clean samples flagged: FPR (%) ↓',[r[2] for r in rows],RED)],[100,10],'Source: VDC v2 Table 4 · note the different horizontal scales (0–100 vs. 0–10)')
rows=[['STRIP',37.94,11.67],['SS',51.86,49.56],['SCAn',46.29,1.61],['Frequency',45.05,18.29],['CT',47.26,.60],['D-BR',10.74,3.91],['SPECTRE',25.05,23.44],['BHN',69.63,1.28],['CL',36.33,.66],['CORES',48.30,4.72],['SimiFeat-V',75.08,4.92],['SimiFeat-R',74.86,5.22],['VDC',99.41,2.79]]
save_csv('vdc','hybrid-detection',['method','mean_TPR_percent','mean_FPR_percent'],rows)
bars('vdc','hybrid-detection','When poisoning and label noise coexist','CIFAR-10 · 9% poisoning + 10% label noise · averages from Table 5.',[r[0] for r in rows],[('Dirty samples detected: TPR (%) ↑',[r[1] for r in rows],'#72989c'),('Clean samples flagged: FPR (%) ↓',[r[2] for r in rows],'#c18c77')],[100,100],'Source: VDC v2 Table 5 · all methods; external clean-subset requirements differ')
rows=[['No detection',98.,93.02],['STRIP',59.33,92.88],['SS',93.61,86.78],['SCAn',13.94,93.06],['Frequency',70.44,91.80],['CT',1.98,93.09],['D-BR',96.14,92.76],['SPECTRE',56.38,87.76],['VDC',1.63,93.21]]
save_csv('vdc','after-cleaning',['method','mean_ASR_percent','mean_clean_ACC_percent'],rows)
bars('vdc','after-cleaning','Does cleaning improve the model trained afterward?','CIFAR-10 · 9% poisoning · ResNet-18 · mean over six backdoor attacks.',[r[0] for r in rows],[('Attack Success Rate (%) ↓',[r[1] for r in rows],'#c18c77'),('Clean Accuracy (%) ↑',[r[2] for r in rows],'#72989c')],[100,100],'Source: VDC v2 Table 6 · averages do not imply superiority on every attack')
print('Built ten SVG figures and six source-data CSV files.')

# Normalize generated text files for clean Git diffs.
for _slug in ['earbench', 'vdc']:
    for _path in (Path(__file__).resolve().parents[1] / "assets/img/blog" / _slug).iterdir():
        if _path.suffix in {".svg", ".csv"}:
            _path.write_text("\n".join(line.rstrip() for line in _path.read_text().splitlines()) + "\n")
