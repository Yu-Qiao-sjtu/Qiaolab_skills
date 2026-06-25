"""
Analyze filtered term-entropy data:
1. Classify into 基础研究 (Basic Research) vs 临床 (Clinical)
2. Detect burst terms (first appearing in 2025-2026)
"""

import csv
import re
from collections import defaultdict

# ── Read filtered data ──────────────────────────────────────────
with open(r"D:\term\term-entropy-filtered.csv", newline="", encoding="utf-8") as f:
    reader = csv.reader(f)
    raw_header = next(reader)
    header = [h.strip().lstrip('\ufeff') for h in raw_header]
    rows = list(reader)

# Parse columns: TERM, Entropy, 2002..2026, Subtotal
year_cols = [str(y) for y in range(2002, 2027)]
year_idx = {y: header.index(y) for y in year_cols}
subtotal_idx = header.index("Subtotal")
entropy_idx = header.index("Entropy")
term_idx = header.index("TERM")

terms = []
for r in rows:
    t = {
        "term": r[term_idx].strip().lower(),
        "entropy": float(r[entropy_idx]) if r[entropy_idx] else 0.0,
        "years": {},
        "subtotal": float(r[subtotal_idx]) if r[subtotal_idx] else 0.0,
    }
    for y in year_cols:
        t["years"][int(y)] = int(r[year_idx[y]]) if r[year_idx[y]] else 0
    terms.append(t)

print(f"Loaded {len(terms)} terms")

# ── Classification: 基础研究 vs 临床 ─────────────────────────────

# Basic Research keywords (机制/通路/分子/细胞/动物/解剖/生理/影像方法/刺激参数)
BASIC_PATTERNS = [
    # Mechanism & pathway
    r'\b(signaling\s*pathway|signal\s*pathway|signalling)',
    r'\b(receptor|receptors)\b',
    r'\b(neurotransmitter|neurotransmitters)\b',
    r'\b(cytokine|cytokines|inflammatory|inflammation|anti-inflammatory)\b',
    r'\b(oxidative\s*stress|apoptosis|autophagy|necrosis)\b',
    r'\b(gene\s*expression|transcription|epigenetic|methylation)\b',
    r'\b(ion\s*channel|calcium\s*signaling|action\s*potential)\b',
    r'\b(synaptic|synapse|neuroplasticity|long-term\s*potentiation|LTP|ltd)\b',
    r'\b(neurotrophic|bdnf|ngf|growth\s*factor)\b',
    r'\b(pathway|pathways)\b',
    r'\b(mechanism|mechanisms|mechanistic)\b',
    r'\b(modulation|modulatory|modulates)\b',
    r'\b(cholinergic|noradrenergic|adrenergic|gabaergic|glutamatergic|dopaminergic|serotonergic|gaba|glutamate|dopamine|serotonin|norepinephrine|acetylcholine)\b',
    r'\b(neural\s*circuit|neural\s*pathway|neural\s*network|neural\s*mechanism)\b',
    # Brain anatomy
    r'\b(brain\s*region|brain\s*area|brain\s*stem|brainstem|cortex|cortical|subcortical)\b',
    r'\b(locus\s*coeruleus|nucleus\s*tractus\s*solitari|nucleus\s*ambiguus|dorsal\s*motor\s*nucleus)\b',
    r'\b(amygdala|hippocampus|hippocampal|prefrontal\s*cortex|insular\s*cortex|insula|anterior\s*cingulate|posterior\s*cingulate)\b',
    r'\b(thalamus|hypothalamus|striatum|striatal|basal\s*ganglia|cerebellum|cerebellar)\b',
    r'\b(solitary\s*tract|solitary\s*nucleus|parabrachial|raphe|periaqueductal)\b',
    r'\b(neuroanatom|neuroanatomy|auricular\s*branch|cranial\s*nerve|afferent|efferent)\b',
    # Animal models
    r'\b(rat|rats|mouse|mice|rodent|animal\s*model|animal\s*study|canine|feline|primate)\b',
    r'\b(in\s*vivo|in\s*vitro|ex\s*vivo)\b',
    # Neurophysiology
    r'\b(firing\s*rate|neuronal\s*firing|spike|neuronal\s*activity|neuronal\s*excitability)\b',
    r'\b(evoked\s*potential|field\s*potential|local\s*field|oscillation|oscillatory)\b',
    r'\b(electrophysiol|microelectrode|patch\s*clamp|whole-cell)\b',
    # Molecular / cellular
    r'\b(molecular|cellular|intracellular|extracellular|membrane|receptor)\b',
    r'\b(protein|enzyme|kinase|phosphorylation|transduction|cascade)\b',
    r'\b(microglia|astrocyte|glia|neuron|neuronal|interneuron)\b',
    r'\b(blood.brain\s*barrier|bbb|neurovascular)\b',
    # Imaging methods
    r'\b(fmri|functional\s*mri|magnetic\s*resonance|bold\s*signal|resting.state)\b',
    r'\b(dti|diffusion\s*tensor|diffusion\s*weighted|tractography)\b',
    r'\b(eeg|electroencephalog|meg|magnetoencephalog)\b',
    r'\b(pet|positron\s*emission|spect|single\s*photon)\b',
    r'\b(fnirs|near-infrared\s*spectroscopy|optical\s*imaging)\b',
    r'\b(seed.based|independent\s*component|ica|graph\s*theory|small.world|connectivity)\b',
    # Physiological measures
    r'\b(heart\s*rate\s*variability|hrv|rmssd|sdnn|lf/hf|low\s*frequency|high\s*frequency)\b',
    r'\b(blood\s*pressure|systolic|diastolic|baroreflex|baroreceptor)\b',
    r'\b(sympathetic|parasympathetic|sympathovagal|vagal\s*tone|vagal\s*activity|vagal\s*efficiency)\b',
    r'\b(autonomic\s*nervous\s*system|ans|autonomic\s*function|autonomic\s*regulation)\b',
    r'\b(galvanic\s*skin|skin\s*conductance|pupillometry|pupil|cortisol|salivary)\b',
    r'\b(biomarker|biomarkers|biochemical|endocrine|hormone|hormonal)\b',
    # Stimulation parameters / technology
    r'\b(electrode|electrodes|electrode\s*placement|electrode\s*position)\b',
    r'\b(pulse\s*width|pulse\s*duration|frequency|hz|khz|amplitude|intensity|current\s*intensity)\b',
    r'\b(duty\s*cycle|waveform|monophasic|biphasic|rectangular|sinusoidal)\b',
    r'\b(stimulation\s*parameter|stimulation\s*protocol|stimulation\s*site)\b',
    r'\b(impedance|conductivity|current\s*density|current\s*flow|finite\s*element)\b',
    r'\b(concha|cymba|tragus|ear\s*anatomy|auricular|auricle)\b',
    # Computational / bioinformatics
    r'\b(entropy|algorithm|machine\s*learning|deep\s*learning|neural\s*network|classifier)\b',
    r'\b(bioinformatic|computational|modeling|simulation|network\s*analysis)\b',
    r'\b(granger\s*causality|dynamic\s*causal|bayesian|mutual\s*information)\b',
    # Basic science general
    r'\b(physiology|physiological|pathophysiology|pathophysiological)\b',
    r'\b(homeostasis|allostasis|feedback\s*loop|reflex|baroreflex)\b',
]

# Clinical keywords (疾病/患者/试验/结局/治疗/手术/量表)
CLINICAL_PATTERNS = [
    # Diseases / conditions
    r'\b(disease|disorder|syndrome|condition|pathology|morbidity)\b',
    r'\b(depression|depressive|major\s*depressive|mdd|antidepressant)\b',
    r'\b(epilepsy|epileptic|seizure|seizures|anticonvulsant)\b',
    r'\b(pain|analgesia|analgesic|nociceptive|hyperalgesia|allodynia|migraine|headache)\b',
    r'\b(stroke|post.stroke|ischemic|hemorrhagic|cerebral\s*ischemia)\b',
    r'\b(ptsd|post.traumatic\s*stress|trauma|traumatic)\b',
    r'\b(alzheimer|dementia|cognitive\s*decline|cognitive\s*impairment|mci)\b',
    r'\b(parkinson|movement\s*disorder|tremor|dyskinesia)\b',
    r'\b(schizophrenia|psychosis|psychotic|bipolar|mania|manic)\b',
    r'\b(anxiety|anxious|generalized\s*anxiety|social\s*anxiety|panic)\b',
    r'\b(autism|asd|autism\s*spectrum|neurodevelopmental)\b',
    r'\b(insomnia|sleep\s*disorder|sleep\s*quality|sleep\s*disturbance)\b',
    r'\b(obesity|metabolic|diabetes|diabetic|insulin|glucose)\b',
    r'\b(hypertension|hypertensive|cardiovascular\s*disease|cvd|heart\s*failure)\b',
    r'\b(atrial\s*fibrillation|arrhythmia|tachycardia|bradycardia)\b',
    r'\b(tinnitus|hearing\s*loss|vestibular|vertigo|dizziness)\b',
    r'\b(ibs|irritable\s*bowel|inflammatory\s*bowel|crohn|colitis|gastrointestinal)\b',
    r'\b(sepsis|infection|infectious|pneumonia|covid|sars)\b',
    r'\b(cancer|tumor|tumour|neoplasm|malignancy|oncology)\b',
    r'\b(multiple\s*sclerosis|autoimmune|rheumatoid|lupus|immune\s*disorder)\b',
    r'\b(delirium|delirious|confusion|consciousness\s*disorder)\b',
    r'\b(addiction|substance\s*abuse|drug\s*abuse|opioid|alcohol|smoking\s*cessation)\b',
    # Patient populations
    r'\b(patient|patients|participant|participants|subject|subjects)\b',
    r'\b(child|children|pediatric|adolescent|infant|neonatal)\b',
    r'\b(adult|adults|elderly|older\s*adult|geriatric|aged)\b',
    r'\b(healthy\s*volunteer|healthy\s*subject|healthy\s*control|healthy\s*participant)\b',
    r'\b(cohort|population|sample|demographic)\b',
    r'\b(comorbid|comorbidity|comorbidities)\b',
    # Clinical trial / study design
    r'\b(randomized\s*controlled\s*trial|randomised\s*controlled\s*trial|rct|rcts)\b',
    r'\b(clinical\s*trial|clinical\s*study|clinical\s*research|clinical\s*investigation)\b',
    r'\b(sham\s*stimulation|sham\s*group|sham\s*control|placebo)\b',
    r'\b(control\s*group|treatment\s*group|intervention\s*group|active\s*group)\b',
    r'\b(double.blind|single.blind|blinding|blinded|open.label)\b',
    r'\b(controlled\s*trial|control\s*study|comparative\s*study)\b',
    r'\b(meta.analysis|systematic\s*review|network\s*meta.analysis)\b',
    r'\b(pilot\s*study|feasibility|proof.of.concept|exploratory)\b',
    r'\b(multicenter|multi.center|single.center|cross.over|parallel.group)\b',
    r'\b(follow.up|long.term|longitudinal|prospective|retrospective)\b',
    r'\b(registry|real.world|observational|cohort\s*study)\b',
    # Clinical outcomes / endpoints
    r'\b(primary\s*outcome|secondary\s*outcome|endpoint|endpoints|outcome\s*measure)\b',
    r'\b(efficacy|effectiveness|effective|efficacious)\b',
    r'\b(safety|safe|adverse\s*event|adverse\s*effect|side\s*effect|side.effect)\b',
    r'\b(tolerability|tolerable|feasibility|feasible|acceptable)\b',
    r'\b(responder|responders|response\s*rate|remission|remission\s*rate)\b',
    r'\b(quality\s*of\s*life|qol|well.being|daily\s*living|functional\s*outcome)\b',
    r'\b(survival|mortality|death|fatal|prognosis|prognostic)\b',
    r'\b(hospital|hospitalization|length\s*of\s*stay|icu|intensive\s*care)\b',
    r'\b(admission|discharge|readmission|outpatient|inpatient)\b',
    # Clinical scales / assessments
    r'\b(hamd|hamilton|madrs|montgomery|beck|bdi|phq.9|phq9|gad.7|gad7)\b',
    r'\b(scale|score|assessment|evaluation|rating|inventory|questionnaire)\b',
    r'\b(vas|visual\s*analog|numeric\s*rating|nrs|likert)\b',
    r'\b(moca|mmse|mini.mental|cognitive\s*assessment|neuropsychological)\b',
    r'\b(clinical\s*global\s*impression|cgi|cgi.i|cgi.s)\b',
    # Treatment / therapy
    r'\b(treatment|therapy|therapeutic|therapeutics|intervention|interventions)\b',
    r'\b(drug|medication|pharmacological|pharmacotherapy|pharmacologic)\b',
    r'\b(dose|dosage|dosing|titration|regimen|protocol)\b',
    r'\b(adjunctive|add.on|augmentation|combination\s*therapy|monotherapy)\b',
    r'\b(rehabilitation|physical\s*therapy|occupational\s*therapy|physiotherapy)\b',
    r'\b(cognitive\s*behavioral|cbt|psychotherapy|counseling|behavioral\s*therapy)\b',
    # Surgery / perioperative
    r'\b(surgery|surgical|postoperative|perioperative|preoperative|intraoperative)\b',
    r'\b(anesthesia|anaesthesia|anesthetic|anaesthetic|general\s*anesthesia)\b',
    r'\b(incision|laparoscopic|laparotomy|thoracotomy|resection)\b',
    r'\b(postoperative\s*pain|postoperative\s*nausea|postoperative\s*delirium|postoperative\s*cognitive)\b',
    # Clinical application general
    r'\b(neuromodulation|neurostimulation|brain\s*stimulation|electrical\s*stimulation)\b',
    r'\b(non.invasive|noninvasive|minimally\s*invasive|transcutaneous|percutaneous)\b',
    r'\b(clinical\s*application|clinical\s*use|therapeutic\s*application|translational)\b',
    r'\b(diagnosis|diagnostic|screening|detection|prognosis)\b',
    r'\b(guideline|guidelines|recommendation|consensus|standard\s*of\s*care)\b',
]

def classify_term(term_str):
    """Returns 'basic', 'clinical', or 'both'"""
    is_basic = False
    is_clinical = False
    
    term = term_str.lower().strip()
    
    for pat in BASIC_PATTERNS:
        if re.search(pat, term):
            is_basic = True
            break
    
    for pat in CLINICAL_PATTERNS:
        if re.search(pat, term):
            is_clinical = True
            break
    
    if is_basic and is_clinical:
        return "both"
    elif is_basic:
        return "basic"
    elif is_clinical:
        return "clinical"
    else:
        return "unclassified"

# ── Classify all terms ───────────────────────────────────────────
classification = {}
for t in terms:
    classification[t["term"]] = classify_term(t["term"])

# ── Burst detection: 2002-2024 all zero, 2025 or 2026 > 0 ───────
burst_terms = []
for t in terms:
    pre_2025_sum = sum(t["years"].get(y, 0) for y in range(2002, 2025))
    if pre_2025_sum == 0:
        sum_2025_2026 = t["years"].get(2025, 0) + t["years"].get(2026, 0)
        if sum_2025_2026 > 0:
            burst_terms.append(t)

print(f"Burst terms (new in 2025-2026): {len(burst_terms)}")

# ── Aggregate by classification ──────────────────────────────────
categories = {"basic": "基础研究", "clinical": "临床", "both": "基础+临床交叉", "unclassified": "未分类"}

for cat_key in ["basic", "clinical", "both", "unclassified"]:
    cat_terms = [t for t in terms if classification[t["term"]] == cat_key]
    # Filter to those with 2025 or 2026 presence
    active_2025 = [t for t in cat_terms if t["years"].get(2025, 0) > 0]
    active_2026 = [t for t in cat_terms if t["years"].get(2026, 0) > 0]
    active_both = [t for t in cat_terms if t["years"].get(2025, 0) > 0 and t["years"].get(2026, 0) > 0]
    
    # Burst terms in this category
    cat_burst = [t for t in burst_terms if classification[t["term"]] == cat_key]
    
    # Top terms by 2025+2026 total
    cat_sorted = sorted(cat_terms, key=lambda t: t["years"].get(2025, 0) + t["years"].get(2026, 0), reverse=True)
    
    print(f"\n{'='*70}")
    print(f"  {categories[cat_key]} ({cat_key})")
    print(f"  总术语数: {len(cat_terms)}, 2025活跃: {len(active_2025)}, 2026活跃: {len(active_2026)}, 两年都活跃: {len(active_both)}")
    print(f"  突发术语 (2025-2026新出现): {len(cat_burst)}")
    print(f"\n  Top 20 高频术语 (2025+2026):")
    for i, t in enumerate(cat_sorted[:20]):
        s25 = t["years"].get(2025, 0)
        s26 = t["years"].get(2026, 0)
        print(f"    {i+1:2d}. {t['term']:<55s} | 2025:{s25:3d}  2026:{s26:3d}  合计:{s25+s26:4d}")
    
    # Top burst terms
    if cat_burst:
        cat_burst_sorted = sorted(cat_burst, key=lambda t: t["years"].get(2025, 0) + t["years"].get(2026, 0), reverse=True)
        print(f"\n  Top 20 突发术语 (此前从未出现):")
        for i, t in enumerate(cat_burst_sorted[:20]):
            s25 = t["years"].get(2025, 0)
            s26 = t["years"].get(2026, 0)
            print(f"    {i+1:2d}. {t['term']:<55s} | 2025:{s25:3d}  2026:{s26:3d}  合计:{s25+s26:4d}")

# ── Overall burst analysis ───────────────────────────────────────
print(f"\n{'='*70}")
print(f"  总体突发术语分析 (2025-2026 首次出现)")
print(f"  总数: {len(burst_terms)}")
print(f"\n  Top 40 突发术语:")
burst_sorted = sorted(burst_terms, key=lambda t: t["years"].get(2025, 0) + t["years"].get(2026, 0), reverse=True)
for i, t in enumerate(burst_sorted[:40]):
    s25 = t["years"].get(2025, 0)
    s26 = t["years"].get(2026, 0)
    cat = categories[classification[t["term"]]]
    print(f"    {i+1:2d}. [{cat}] {t['term']:<55s} | 2025:{s25:3d}  2026:{s26:3d}  合计:{s25+s26:4d}")

# ── Save burst terms to file ─────────────────────────────────────
with open(r"D:\term\burst-terms-2025-2026.csv", "w", newline="", encoding="utf-8-sig") as f:
    writer = csv.writer(f)
    writer.writerow(["TERM", "Category", "2025", "2026", "Total", "Entropy"])
    for t in burst_sorted:
        cat = categories[classification[t["term"]]]
        writer.writerow([
            t["term"],
            cat,
            t["years"].get(2025, 0),
            t["years"].get(2026, 0),
            t["years"].get(2025, 0) + t["years"].get(2026, 0),
            t["entropy"],
        ])

print(f"\n✅ Burst terms saved to D:\\term\\burst-terms-2025-2026.csv")
print("Done.")
