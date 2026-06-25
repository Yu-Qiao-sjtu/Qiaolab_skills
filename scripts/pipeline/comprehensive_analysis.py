"""
全面分析 2025-2026 taVNS 术语数据：
1. 全部分类为 基础研究 vs 临床（三层分类策略）
2. 2025-2026 热点
3. 2025-2026 突发术语
4. 2022-2026 演化趋势
"""

import csv
import re
from collections import defaultdict

# ═══════════════════════════════════════════════════════════════
# DATA LOADING
# ═══════════════════════════════════════════════════════════════
with open(r"D:\term\term-entropy-filtered.csv", newline="", encoding="utf-8") as f:
    reader = csv.reader(f)
    raw_header = next(reader)
    header = [h.strip().lstrip('\ufeff') for h in raw_header]
    rows = list(reader)

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

# ═══════════════════════════════════════════════════════════════
# THREE-TIER CLASSIFICATION
# ═══════════════════════════════════════════════════════════════

# ── TIER 1: Precise regex patterns (from previous analysis) ──

BASIC_T1 = [
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
    r'\b(cholinergic|noradrenergic|adrenergic|gabaergic|glutamatergic|dopaminergic|serotonergic|gaba\b|glutamate|dopamine|serotonin|norepinephrine|acetylcholine)\b',
    r'\b(neural\s*circuit|neural\s*pathway|neural\s*network|neural\s*mechanism)\b',
    r'\b(brain\s*region|brain\s*area|brain\s*stem|brainstem|cortex|cortical|subcortical)\b',
    r'\b(locus\s*coeruleus|nucleus\s*tractus\s*solitari|nucleus\s*ambiguus|dorsal\s*motor\s*nucleus)\b',
    r'\b(amygdala|hippocampus|hippocampal|prefrontal\s*cortex|insular\s*cortex|insula|anterior\s*cingulate|posterior\s*cingulate)\b',
    r'\b(thalamus|hypothalamus|striatum|striatal|basal\s*ganglia|cerebellum|cerebellar)\b',
    r'\b(solitary\s*tract|solitary\s*nucleus|parabrachial|raphe|periaqueductal)\b',
    r'\b(neuroanatom|neuroanatomy|auricular\s*branch|cranial\s*nerve|afferent|efferent)\b',
    r'\b(rat\b|rats\b|mouse|mice|rodent|animal\s*model|animal\s*study|canine|feline|primate)\b',
    r'\b(in\s*vivo|in\s*vitro|ex\s*vivo)\b',
    r'\b(firing\s*rate|neuronal\s*firing|spike|neuronal\s*activity|neuronal\s*excitability)\b',
    r'\b(evoked\s*potential|field\s*potential|local\s*field|oscillation|oscillatory)\b',
    r'\b(electrophysiol|microelectrode|patch\s*clamp|whole-cell)\b',
    r'\b(molecular|cellular|intracellular|extracellular|membrane)\b',
    r'\b(protein|enzyme|kinase|phosphorylation|transduction|cascade)\b',
    r'\b(microglia|astrocyte|glia|neuron|neuronal|interneuron)\b',
    r'\b(blood.brain\s*barrier|bbb|neurovascular)\b',
    r'\b(fmri|functional\s*mri|magnetic\s*resonance|bold\s*signal|resting.state)\b',
    r'\b(dti|diffusion\s*tensor|diffusion\s*weighted|tractography)\b',
    r'\b(eeg|electroencephalog|meg|magnetoencephalog)\b',
    r'\b(pet\b|positron\s*emission|spect\b|single\s*photon)\b',
    r'\b(fnirs|near-infrared\s*spectroscopy|optical\s*imaging)\b',
    r'\b(seed.based|independent\s*component|ica\b|graph\s*theory|small.world|connectivity)\b',
    r'\b(heart\s*rate\s*variability|hrv|rmssd|sdnn|lf/hf|low\s*frequency|high\s*frequency)\b',
    r'\b(blood\s*pressure|systolic|diastolic|baroreflex|baroreceptor)\b',
    r'\b(sympathetic|parasympathetic|sympathovagal|vagal\s*tone|vagal\s*activity|vagal\s*efficiency)\b',
    r'\b(autonomic\s*nervous\s*system|ans\b|autonomic\s*function|autonomic\s*regulation)\b',
    r'\b(galvanic\s*skin|skin\s*conductance|pupillometry|pupil\b|cortisol|salivary)\b',
    r'\b(biomarker|biomarkers|biochemical|endocrine|hormone|hormonal)\b',
    r'\b(electrode|electrodes|electrode\s*placement|electrode\s*position)\b',
    r'\b(pulse\s*width|pulse\s*duration|hz\b|khz\b|amplitude|intensity|current\s*intensity)\b',
    r'\b(duty\s*cycle|waveform|monophasic|biphasic|rectangular|sinusoidal)\b',
    r'\b(stimulation\s*parameter|stimulation\s*protocol|stimulation\s*site)\b',
    r'\b(impedance|conductivity|current\s*density|current\s*flow|finite\s*element)\b',
    r'\b(concha|cymba|tragus|ear\s*anatomy|auricular|auricle)\b',
    r'\b(entropy|algorithm|machine\s*learning|deep\s*learning|neural\s*network|classifier)\b',
    r'\b(bioinformatic|computational|modeling|simulation|network\s*analysis)\b',
    r'\b(granger\s*causality|dynamic\s*causal|bayesian|mutual\s*information)\b',
    r'\b(physiology|physiological|pathophysiology|pathophysiological)\b',
    r'\b(homeostasis|allostasis|feedback\s*loop|reflex|baroreflex)\b',
]

CLINICAL_T1 = [
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
    r'\b(ibs\b|irritable\s*bowel|inflammatory\s*bowel|crohn|colitis|gastrointestinal)\b',
    r'\b(sepsis|infection|infectious|pneumonia|covid|sars)\b',
    r'\b(cancer|tumor|tumour|neoplasm|malignancy|oncology)\b',
    r'\b(multiple\s*sclerosis|autoimmune|rheumatoid|lupus|immune\s*disorder)\b',
    r'\b(delirium|delirious|confusion|consciousness\s*disorder)\b',
    r'\b(addiction|substance\s*abuse|drug\s*abuse|opioid|alcohol|smoking\s*cessation)\b',
    r'\b(patient|patients|participant|participants|subject|subjects)\b',
    r'\b(child|children|pediatric|adolescent|infant|neonatal)\b',
    r'\b(adult|adults|elderly|older\s*adult|geriatric|aged)\b',
    r'\b(healthy\s*volunteer|healthy\s*subject|healthy\s*control|healthy\s*participant)\b',
    r'\b(cohort|population|sample|demographic)\b',
    r'\b(comorbid|comorbidity|comorbidities)\b',
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
    r'\b(primary\s*outcome|secondary\s*outcome|endpoint|endpoints|outcome\s*measure)\b',
    r'\b(efficacy|effectiveness|effective|efficacious)\b',
    r'\b(safety|safe|adverse\s*event|adverse\s*effect|side\s*effect|side.effect)\b',
    r'\b(tolerability|tolerable|feasibility|feasible|acceptable)\b',
    r'\b(responder|responders|response\s*rate|remission|remission\s*rate)\b',
    r'\b(quality\s*of\s*life|qol|well.being|daily\s*living|functional\s*outcome)\b',
    r'\b(survival|mortality|death|fatal|prognosis|prognostic)\b',
    r'\b(hospital|hospitalization|length\s*of\s*stay|icu|intensive\s*care)\b',
    r'\b(admission|discharge|readmission|outpatient|inpatient)\b',
    r'\b(hamd|hamilton|madrs|montgomery|beck\b|bdi|phq.9|phq9|gad.7|gad7)\b',
    r'\b(scale|score|assessment|evaluation|rating|inventory|questionnaire)\b',
    r'\b(vas\b|visual\s*analog|numeric\s*rating|nrs\b|likert)\b',
    r'\b(moca|mmse|mini.mental|cognitive\s*assessment|neuropsychological)\b',
    r'\b(clinical\s*global\s*impression|cgi|cgi.i|cgi.s)\b',
    r'\b(treatment|therapy|therapeutic|therapeutics|intervention|interventions)\b',
    r'\b(drug|medication|pharmacological|pharmacotherapy|pharmacologic)\b',
    r'\b(dose|dosage|dosing|titration|regimen|protocol)\b',
    r'\b(adjunctive|add.on|augmentation|combination\s*therapy|monotherapy)\b',
    r'\b(rehabilitation|physical\s*therapy|occupational\s*therapy|physiotherapy)\b',
    r'\b(cognitive\s*behavioral|cbt|psychotherapy|counseling|behavioral\s*therapy)\b',
    r'\b(surgery|surgical|postoperative|perioperative|preoperative|intraoperative)\b',
    r'\b(anesthesia|anaesthesia|anesthetic|anaesthetic|general\s*anesthesia)\b',
    r'\b(incision|laparoscopic|laparotomy|thoracotomy|resection)\b',
    r'\b(postoperative\s*pain|postoperative\s*nausea|postoperative\s*delirium|postoperative\s*cognitive)\b',
    r'\b(neuromodulation|neurostimulation|brain\s*stimulation|electrical\s*stimulation)\b',
    r'\b(non.invasive|noninvasive|minimally\s*invasive|transcutaneous|percutaneous)\b',
    r'\b(clinical\s*application|clinical\s*use|therapeutic\s*application|translational)\b',
    r'\b(diagnosis|diagnostic|screening|detection|prognosis)\b',
    r'\b(guideline|guidelines|recommendation|consensus|standard\s*of\s*care)\b',
]

# ── TIER 2: Broader catch-all keywords ──

BASIC_T2_WORDS = [
    # Anatomy / neuroanatomy
    "nerve", "nerv", "brain", "cerebral", "cerebell", "cortex", "cortical",
    "subcortical", "hippocamp", "amygdal", "thalam", "striatum", "striatal",
    "brainstem", "medulla", "pons", "midbrain", "diencephalon",
    "nucleus", "nuclei", "ganglion", "ganglia", "tract", "fiber", "fibre",
    "axon", "dendrit", "synap", "terminal", "bouton", "varicosit",
    "afferent", "efferent", "vagal", "auricular", "concha", "cymba", "tragus",
    "ear canal", "external ear", "inner ear", "tympanic",
    "spinal cord", "dorsal horn", "dorsal root", "trigeminal",
    "autonomic", "sympathetic", "parasympathetic", "enteric",
    "baroreflex", "baroreceptor", "chemoreflex", "chemoreceptor",
    "peripheral nervous", "central nervous", "cns",
    # Cellular / molecular
    "neuron", "neuronal", "neural", "neuro", "glia", "glial",
    "microglia", "astrocyte", "oligodendrocyt",
    "cell", "cellular", "intracellular", "extracellular", "membrane",
    "receptor", "channel", "ion", "transporter", "pump",
    "protein", "gene", "rna", "dna", "transcript", "translat",
    "kinase", "phosphatase", "phosphorylat", "enzyme", "enzymatic",
    "cytokine", "chemokine", "interleukin", "tnf", "nf-kb", "nlrp3",
    "inflammatory", "inflammation", "anti-inflammatory", "pro-inflammatory",
    "oxidative", "antioxidant", "ros", "reactive oxygen",
    "apoptosis", "apoptotic", "autophagy", "necroptosis", "necrosis",
    "bdnf", "ngf", "neurotrophin", "growth factor", "trophic",
    "plasticity", "neuroplastic", "ltp", "ltd", "long-term potentiation",
    "synaptic", "synaptogenesis", "neurogenesis",
    "epigenetic", "methylation", "acetylation", "histone",
    "microbiome", "microbiota", "gut-brain",
    # Neurotransmitter systems
    "cholinergic", "adrenergic", "noradrenergic", "dopaminergic",
    "serotonergic", "gabaergic", "glutamatergic", "opioidergic",
    "acetylcholine", "norepinephrine", "noradrenaline", "dopamine",
    "serotonin", "5-ht", "gaba", "glutamate", "endorphin",
    "cannabinoid", "endocannabinoid",
    # Neurophysiology
    "action potential", "membrane potential", "resting potential",
    "depolariz", "hyperpolariz", "repolariz",
    "firing rate", "spike", "burst", "oscillat", "rhythm",
    "eeg", "electroencephalog", "erp", "event-related",
    "meg", "magnetoencephalog", "local field potential",
    "patch clamp", "electrophysiol", "electrode",
    "impedance", "conductance", "resistance", "capacitance",
    # Neuroimaging
    "fmri", "mri", "magnetic resonance", "bold", "resting-state",
    "functional connectivity", "effective connectivity",
    "dti", "diffusion tensor", "diffusion weighted", "tractography",
    "pet", "positron emission", "spect", "single photon",
    "fnirs", "near-infrared", "optical imaging",
    "seed-based", "independent component", "ica", "graph theory",
    "small-world", "default mode", "salience network",
    "central executive", "frontoparietal",
    # Physiological measures
    "heart rate variability", "hrv", "rmssd", "sdnn", "lf/hf",
    "blood pressure", "systolic", "diastolic", "baroreflex",
    "heart rate", "pulse", "electrocardiogram", "ecg", "ekg",
    "skin conductance", "galvanic skin", "pupillometry",
    "pupil", "cortisol", "salivary", "alpha-amylase",
    "respiration", "respiratory", "breathing rate",
    "temperature", "thermoregulat",
    # Stimulation parameters / methods
    "stimulation parameter", "stimulation protocol", "stimulation site",
    "pulse width", "pulse duration", "frequency", "hz", "khz",
    "amplitude", "intensity", "current", "voltage",
    "duty cycle", "waveform", "monophasic", "biphasic",
    "rectangular", "sinusoidal", "burst mode",
    "electrode placement", "electrode position", "electrode size",
    "current density", "current flow", "finite element",
    # Computational / methods
    "entropy", "algorithm", "machine learning", "deep learning",
    "classifier", "bioinformatic", "computational",
    "modeling", "simulation", "network analysis",
    "granger causality", "dynamic causal",
    "bayesian", "mutual information",
    # Physiology / mechanism
    "physiology", "physiological", "pathophysiology", "pathophysiological",
    "homeostasis", "allostasis", "feedback loop", "reflex",
    "mechanism", "mechanistic", "pathway", "signaling",
    "modulation", "modulatory", "regulat",
    "circadian", "diurnal", "chronobiology",
    # Animal models
    "rat", "rats", "mouse", "mice", "rodent", "animal",
    "in vivo", "in vitro", "ex vivo", "canine", "feline", "primate",
    "zebrafish", "drosophila", "c elegans",
    "knockout", "transgenic", "wild-type", "mutant",
]

CLINICAL_T2_WORDS = [
    # Diseases / conditions
    "disease", "disorder", "syndrome", "condition", "pathology", "morbidity",
    "depression", "depressive", "mdd", "antidepressant",
    "epilepsy", "epileptic", "seizure", "anticonvulsant",
    "pain", "analgesia", "analgesic", "nociceptive", "hyperalgesia",
    "allodynia", "migraine", "headache", "fibromyalgia",
    "stroke", "ischemic", "hemorrhagic", "cerebral ischemia",
    "ptsd", "post-traumatic", "trauma", "traumatic",
    "alzheimer", "dementia", "cognitive decline", "cognitive impairment", "mci",
    "parkinson", "movement disorder", "tremor", "dyskinesia",
    "schizophrenia", "psychosis", "psychotic", "bipolar", "mania",
    "anxiety", "anxious", "panic",
    "autism", "asd", "neurodevelopmental",
    "insomnia", "sleep disorder", "sleep quality", "sleep disturbance",
    "obesity", "metabolic", "diabetes", "diabetic", "insulin", "glucose",
    "hypertension", "hypertensive", "cardiovascular disease", "cvd",
    "heart failure", "myocardial infarction", "coronary",
    "atrial fibrillation", "arrhythmia", "tachycardia", "bradycardia",
    "tinnitus", "hearing loss", "vestibular", "vertigo", "dizziness",
    "ibs", "irritable bowel", "inflammatory bowel", "crohn", "colitis",
    "gastrointestinal", "gastric", "gastroparesis",
    "sepsis", "infection", "infectious", "pneumonia", "covid", "sars",
    "cancer", "tumor", "tumour", "neoplasm", "malignancy", "oncology",
    "multiple sclerosis", "autoimmune", "rheumatoid", "lupus",
    "delirium", "confusion", "consciousness",
    "addiction", "substance abuse", "drug abuse", "opioid",
    "alcohol", "smoking cessation", "nicotine",
    "obesity", "overweight", "bmi", "body mass",
    "fatigue", "chronic fatigue",
    # Patient / population
    "patient", "patients", "participant", "participants",
    "subject", "subjects", "volunteer", "volunteers",
    "child", "children", "pediatric", "adolescent", "infant", "neonatal",
    "adult", "adults", "elderly", "older", "geriatric", "aged",
    "healthy", "control", "cohort", "population",
    "demographic", "comorbid", "comorbidity",
    "inclusion", "exclusion", "recruitment", "enrollment",
    "dropout", "attrition", "retention",
    # Clinical trials / study design
    "randomized", "randomised", "rct", "trial", "trials",
    "clinical study", "clinical research", "clinical investigation",
    "sham", "placebo", "control group", "treatment group",
    "intervention group", "active group",
    "double-blind", "single-blind", "blinding", "blinded", "open-label",
    "controlled trial", "comparative study",
    "meta-analysis", "systematic review", "network meta-analysis",
    "pilot study", "feasibility", "proof-of-concept", "exploratory",
    "multicenter", "multi-center", "single-center",
    "cross-over", "parallel-group", "factorial",
    "follow-up", "long-term", "longitudinal",
    "prospective", "retrospective", "registry", "real-world",
    "observational", "cohort study", "case-control",
    # Outcomes / endpoints
    "primary outcome", "secondary outcome", "endpoint",
    "outcome measure", "efficacy", "effectiveness", "effective",
    "safety", "adverse event", "adverse effect", "side effect",
    "tolerability", "tolerable", "feasibility",
    "responder", "responders", "response rate",
    "remission", "remission rate", "recovery",
    "quality of life", "qol", "well-being",
    "daily living", "functional outcome",
    "survival", "mortality", "death", "fatal", "prognosis", "prognostic",
    "hospital", "hospitalization", "length of stay",
    "icu", "intensive care", "admission", "discharge", "readmission",
    "outpatient", "inpatient", "emergency",
    # Clinical scales / assessments
    "hamd", "hamilton", "madrs", "montgomery", "beck", "bdi",
    "phq-9", "phq9", "gad-7", "gad7",
    "scale", "score", "assessment", "evaluation", "rating",
    "inventory", "questionnaire", "survey",
    "vas", "visual analog", "numeric rating", "nrs", "likert",
    "moca", "mmse", "mini-mental", "neuropsychological",
    "cgi", "clinical global impression",
    "clinical assessment", "clinical evaluation",
    # Treatment / therapy
    "treatment", "therapy", "therapeutic", "therapeutics",
    "intervention", "interventions",
    "drug", "medication", "pharmacological", "pharmacotherapy",
    "dose", "dosage", "dosing", "titration", "regimen",
    "adjunctive", "add-on", "augmentation",
    "combination therapy", "monotherapy",
    "rehabilitation", "physical therapy", "physiotherapy",
    "occupational therapy", "speech therapy",
    "cognitive behavioral", "cbt", "psychotherapy", "counseling",
    "behavioral therapy", "cognitive training",
    # Surgery / perioperative
    "surgery", "surgical", "postoperative", "perioperative",
    "preoperative", "intraoperative",
    "anesthesia", "anaesthesia", "anesthetic", "anaesthetic",
    "incision", "laparoscopic", "laparotomy", "thoracotomy", "resection",
    "postoperative pain", "postoperative nausea",
    "postoperative delirium", "postoperative cognitive",
    "surgical site", "wound", "healing",
    # Clinical application
    "neuromodulation", "neurostimulation", "brain stimulation",
    "electrical stimulation", "non-invasive", "noninvasive",
    "minimally invasive", "transcutaneous", "percutaneous",
    "clinical application", "clinical use", "therapeutic application",
    "translational", "diagnosis", "diagnostic",
    "screening", "detection", "guideline", "guidelines",
    "recommendation", "consensus", "standard of care",
    "medical device", "fda", "approval", "regulatory",
    "cost-effectiveness", "cost", "economic", "reimbursement",
    # Other clinical
    "symptom", "symptoms", "sign", "signs",
    "flare", "relapse", "recurrence", "exacerbation",
    "acute", "chronic", "subacute", "subchronic",
    "phase", "stage", "grade", "severity", "mild", "moderate", "severe",
    "onset", "duration", "course", "episode",
    "baseline", "week", "month", "year", "follow-up period",
    "improvement", "worsening", "deterioration", "change",
    "clinically", "statistically significant",
    "p value", "confidence interval", "effect size",
    "number needed", "absolute risk", "relative risk",
    "odds ratio", "hazard ratio",
]

def classify_term(term_str):
    """Three-tier classification: basic, clinical, or both"""
    term = term_str.lower().strip()
    
    # Tier 1: precise patterns
    is_basic = any(re.search(pat, term) for pat in BASIC_T1)
    is_clinical = any(re.search(pat, term) for pat in CLINICAL_T1)
    
    if is_basic and is_clinical:
        return "both"
    if is_basic:
        return "basic"  # tentative
    if is_clinical:
        return "clinical"  # tentative
    
    # If Tier 1 gave basic or clinical, still check Tier 2 to see if it's "both"
    if is_basic or is_clinical:
        # Tier 1 already decided; skip Tier 2 for "both" detection
        if is_basic:
            # Check if also has strong clinical words
            for w in CLINICAL_T2_WORDS:
                if w in term:
                    return "both"
            return "basic"
        else:
            for w in BASIC_T2_WORDS:
                if w in term:
                    return "both"
            return "clinical"
    
    # Tier 2: broad catch-all
    is_basic2 = any(w in term for w in BASIC_T2_WORDS)
    is_clinical2 = any(w in term for w in CLINICAL_T2_WORDS)
    
    if is_basic2 and is_clinical2:
        return "both"
    if is_basic2:
        return "basic"
    if is_clinical2:
        return "clinical"
    
    # Tier 3: still unclassified → contextual heuristic
    # General academic/statistical terms → clinical (as taVNS is mostly clinical)
    # Geographic/author names → clinical
    # Measurement/time descriptions → clinical if about sessions/trials, basic if about physiology
    
    # Check for words that suggest measurement/session descriptions
    if any(w in term for w in ["session", "week", "month", "trial", "group",
                                 "min", "hour", "day", "period", "baseline",
                                 "visit", "follow", "recruitment", "enroll",
                                 "administer", "dos", "prescri", "medic",
                                 "surger", "operat", "clinic", "hospit",
                                 "rehab", "therap", "consult"]):
        return "clinical"
    
    # Check for words that suggest basic/mechanistic work
    if any(w in term for w in ["activation", "inhibition", "response",
                                 "latency", "amplitude", "peak", "trough",
                                 "slope", "threshold", "sensitivity",
                                 "specificity", "accuracy", "signal",
                                 "noise", "ratio", "index", "coefficient",
                                 "correlation", "regression", "variance",
                                 "frequency band", "alpha", "beta", "gamma",
                                 "delta", "theta", "oscillat", "wave",
                                 "evok", "induc", "elicit", "trigger"]):
        return "basic"
    
    # Default for remaining: clinical (majority of taVNS research)
    return "clinical"

# ── Classify all terms ────────────────────────────────────────────
classification = {}
for t in terms:
    classification[t["term"]] = classify_term(t["term"])

# ═══════════════════════════════════════════════════════════════
# STATISTICS
# ═══════════════════════════════════════════════════════════════
cat_counts = {"basic": 0, "clinical": 0, "both": 0}
for t in terms:
    c = classification[t["term"]]
    cat_counts[c] = cat_counts.get(c, 0) + 1

print(f"\nFinal classification:")
print(f"  基础研究 (basic): {cat_counts['basic']}")
print(f"  临床 (clinical): {cat_counts['clinical']}")
print(f"  交叉 (both): {cat_counts['both']}")
print(f"  Total: {sum(cat_counts.values())}")

# ▸▸▸▸▸▸▸▸▸▸▸▸▸▸▸▸▸▸▸▸▸▸▸▸▸▸▸▸▸▸▸▸▸▸▸▸▸▸▸▸▸▸▸▸▸▸▸▸▸▸▸▸▸▸▸▸▸▸▸▸▸▸▸▸▸▸▸▸▸▸▸▸▸▸▸▸▸▸▸▸
# ANALYSIS 1: 2025-2026 HOTSPOTS
# ▸▸▸▸▸▸▸▸▸▸▸▸▸▸▸▸▸▸▸▸▸▸▸▸▸▸▸▸▸▸▸▸▸▸▸▸▸▸▸▸▸▸▸▸▸▸▸▸▸▸▸▸▸▸▸▸▸▸▸▸▸▸▸▸▸▸▸▸▸▸▸▸▸▸▸▸▸▸▸▸
def sum_2025_2026(t):
    return t["years"].get(2025, 0) + t["years"].get(2026, 0)

def sum_2022_2026(t):
    return sum(t["years"].get(y, 0) for y in range(2022, 2027))

# Overall hotspots (2025-2026, all categories)
all_sorted = sorted(terms, key=sum_2025_2026, reverse=True)
basic_terms = [t for t in terms if classification[t["term"]] in ("basic", "both")]
clinical_terms = [t for t in terms if classification[t["term"]] in ("clinical", "both")]
basic_sorted = sorted(basic_terms, key=sum_2025_2026, reverse=True)
clinical_sorted = sorted(clinical_terms, key=sum_2025_2026, reverse=True)

# ▸▸▸▸▸▸▸▸▸▸▸▸▸▸▸▸▸▸▸▸▸▸▸▸▸▸▸▸▸▸▸▸▸▸▸▸▸▸▸▸▸▸▸▸▸▸▸▸▸▸▸▸▸▸▸▸▸▸▸▸▸▸▸▸▸▸▸▸▸▸▸▸▸▸▸▸▸▸▸▸
# ANALYSIS 2: 2025-2026 BURST TERMS
# ▸▸▸▸▸▸▸▸▸▸▸▸▸▸▸▸▸▸▸▸▸▸▸▸▸▸▸▸▸▸▸▸▸▸▸▸▸▸▸▸▸▸▸▸▸▸▸▸▸▸▸▸▸▸▸▸▸▸▸▸▸▸▸▸▸▸▸▸▸▸▸▸▸▸▸▸▸▸▸▸
burst_terms = []
for t in terms:
    pre_2025_sum = sum(t["years"].get(y, 0) for y in range(2002, 2025))
    if pre_2025_sum == 0:
        s25 = t["years"].get(2025, 0)
        s26 = t["years"].get(2026, 0)
        if s25 + s26 > 0:
            burst_terms.append(t)

burst_basic = [t for t in burst_terms if classification[t["term"]] in ("basic", "both")]
burst_clinical = [t for t in burst_terms if classification[t["term"]] in ("clinical", "both")]
burst_basic_sorted = sorted(burst_basic, key=sum_2025_2026, reverse=True)
burst_clinical_sorted = sorted(burst_clinical, key=sum_2025_2026, reverse=True)

# ▸▸▸▸▸▸▸▸▸▸▸▸▸▸▸▸▸▸▸▸▸▸▸▸▸▸▸▸▸▸▸▸▸▸▸▸▸▸▸▸▸▸▸▸▸▸▸▸▸▸▸▸▸▸▸▸▸▸▸▸▸▸▸▸▸▸▸▸▸▸▸▸▸▸▸▸▸▸▸▸
# ANALYSIS 3: 2022-2026 EVOLUTION
# ▸▸▸▸▸▸▸▸▸▸▸▸▸▸▸▸▸▸▸▸▸▸▸▸▸▸▸▸▸▸▸▸▸▸▸▸▸▸▸▸▸▸▸▸▸▸▸▸▸▸▸▸▸▸▸▸▸▸▸▸▸▸▸▸▸▸▸▸▸▸▸▸▸▸▸▸▸▸▸▸

# Aggregate by year for basic vs clinical
yearly_basic = {y: 0 for y in range(2022, 2027)}
yearly_clinical = {y: 0 for y in range(2022, 2027)}
for t in terms:
    cat = classification[t["term"]]
    for y in range(2022, 2027):
        val = t["years"].get(y, 0)
        if cat in ("basic", "both"):
            yearly_basic[y] += val
        if cat in ("clinical", "both"):
            yearly_clinical[y] += val

# Top 30 terms by growth 2022→2026
growth_terms = []
for t in terms:
    s22_24 = sum(t["years"].get(y, 0) for y in range(2022, 2025))
    s25_26 = sum(t["years"].get(y, 0) for y in (2025, 2026))
    growth = s25_26 - s22_24
    growth_terms.append((t, growth))

growth_sorted = sorted(growth_terms, key=lambda x: x[1], reverse=True)

# Top terms each year (for evolution tracking)
top_terms_evolution = {}
for y in range(2022, 2027):
    year_terms = [(t, t["years"].get(y, 0)) for t in terms if t["years"].get(y, 0) > 0]
    year_terms.sort(key=lambda x: x[1], reverse=True)
    top_terms_evolution[y] = year_terms[:30]

# ═══════════════════════════════════════════════════════════════
# GENERATE REPORT
# ═══════════════════════════════════════════════════════════════

report = []
def p(line=""):
    report.append(line)
    print(line)

p("=" * 80)
p("  taVNS 术语分析综合报告")
p("  Comprehensive Term Analysis Report")
p("=" * 80)
p()

p("─" * 80)
p("  一、分类结果总览")
p("─" * 80)
p()
p(f"  术语总数: {len(terms)}")
p(f"  基础研究: {cat_counts['basic']} ({cat_counts['basic']/len(terms)*100:.1f}%)")
p(f"  临床:      {cat_counts['clinical']} ({cat_counts['clinical']/len(terms)*100:.1f}%)")
p(f"  交叉:      {cat_counts['both']} ({cat_counts['both']/len(terms)*100:.1f}%)")
p()
p(f"  基础研究（含交叉）: {cat_counts['basic'] + cat_counts['both']}")
p(f"  临床（含交叉）:     {cat_counts['clinical'] + cat_counts['both']}")
p()

# ═══════════════════════════════════════════════════════════════
p("─" * 80)
p("  二、2025-2026 研究热点 (Hotspots)")
p("─" * 80)
p()

# Basic research hotspots
p("  【基础研究】2025-2026 高频术语 Top 30")
p(f"  {'Rank':<6}{'Term':<50}{'2025':>6}{'2026':>6}{'合计':>6}{'类别':>8}")
p(f"  {'-'*4:<6}{'-'*50:<50}{'-'*6:>6}{'-'*6:>6}{'-'*6:>6}{'-'*8:>8}")
for i, t in enumerate(basic_sorted[:30]):
    s25 = t["years"].get(2025, 0)
    s26 = t["years"].get(2026, 0)
    cat = classification[t["term"]]
    cat_cn = "基础" if cat == "basic" else "交叉"
    p(f"  {i+1:<6}{t['term'][:50]:<50}{s25:>6}{s26:>6}{s25+s26:>6}{cat_cn:>8}")
p()

# Clinical hotspots
p("  【临床】2025-2026 高频术语 Top 30")
p(f"  {'Rank':<6}{'Term':<50}{'2025':>6}{'2026':>6}{'合计':>6}{'类别':>8}")
p(f"  {'-'*4:<6}{'-'*50:<50}{'-'*6:>6}{'-'*6:>6}{'-'*6:>6}{'-'*8:>8}")
for i, t in enumerate(clinical_sorted[:30]):
    s25 = t["years"].get(2025, 0)
    s26 = t["years"].get(2026, 0)
    cat = classification[t["term"]]
    cat_cn = "临床" if cat == "clinical" else "交叉"
    p(f"  {i+1:<6}{t['term'][:50]:<50}{s25:>6}{s26:>6}{s25+s26:>6}{cat_cn:>8}")
p()

# ═══════════════════════════════════════════════════════════════
p("─" * 80)
p("  三、2025-2026 突发术语 (Burst Terms — 此前从未出现)")
p("─" * 80)
p(f"  突发术语总数: {len(burst_terms)}")
p(f"  基础研究突发: {len(burst_basic)}")
p(f"  临床突发:     {len(burst_clinical)}")
p()

# Burst basic
p("  【基础研究】突发术语 Top 40")
p(f"  {'Rank':<6}{'Term':<50}{'2025':>6}{'2026':>6}{'合计':>6}")
p(f"  {'-'*4:<6}{'-'*50:<50}{'-'*6:>6}{'-'*6:>6}{'-'*6:>6}")
for i, t in enumerate(burst_basic_sorted[:40]):
    s25 = t["years"].get(2025, 0)
    s26 = t["years"].get(2026, 0)
    p(f"  {i+1:<6}{t['term'][:50]:<50}{s25:>6}{s26:>6}{s25+s26:>6}")
p()

# Burst clinical
p("  【临床】突发术语 Top 40")
p(f"  {'Rank':<6}{'Term':<50}{'2025':>6}{'2026':>6}{'合计':>6}")
p(f"  {'-'*4:<6}{'-'*50:<50}{'-'*6:>6}{'-'*6:>6}{'-'*6:>6}")
for i, t in enumerate(burst_clinical_sorted[:40]):
    s25 = t["years"].get(2025, 0)
    s26 = t["years"].get(2026, 0)
    p(f"  {i+1:<6}{t['term'][:50]:<50}{s25:>6}{s26:>6}{s25+s26:>6}")
p()

# ═══════════════════════════════════════════════════════════════
p("─" * 80)
p("  四、2022-2026 演化趋势 (Evolution)")
p("─" * 80)
p()

p("  4.1 年度术语活跃度（基础 vs 临床）")
p(f"  {'Year':<8}{'基础研究':>10}{'临床':>10}{'总计':>10}")
p(f"  {'-'*8:<8}{'-'*10:>10}{'-'*10:>10}{'-'*10:>10}")
for y in range(2022, 2027):
    total = yearly_basic[y] + yearly_clinical[y]
    p(f"  {y:<8}{yearly_basic[y]:>10}{yearly_clinical[y]:>10}{total:>10}")
p()

p("  4.2 各年度 Top 20 术语（基础研究）")
for y in range(2022, 2027):
    p(f"\n  ── {y} 基础研究高频术语 ──")
    yr_terms = [(t, t["years"].get(y, 0)) for t in terms
                if classification[t["term"]] in ("basic", "both") and t["years"].get(y, 0) > 0]
    yr_terms.sort(key=lambda x: x[1], reverse=True)
    for i, (t, cnt) in enumerate(yr_terms[:20]):
        p(f"    {i+1:2d}. {t['term'][:55]:<55s} | {cnt:3d}")

p()

p("  4.3 各年度 Top 20 术语（临床）")
for y in range(2022, 2027):
    p(f"\n  ── {y} 临床高频术语 ──")
    yr_terms = [(t, t["years"].get(y, 0)) for t in terms
                if classification[t["term"]] in ("clinical", "both") and t["years"].get(y, 0) > 0]
    yr_terms.sort(key=lambda x: x[1], reverse=True)
    for i, (t, cnt) in enumerate(yr_terms[:20]):
        p(f"    {i+1:2d}. {t['term'][:55]:<55s} | {cnt:3d}")

p()

p("  4.4 增长最快的术语 Top 30 (2022-2024 → 2025-2026)")
p(f"  {'Rank':<6}{'Term':<50}{'2022-24':>8}{'2025-26':>8}{'增长':>8}{'类别':>8}")
p(f"  {'-'*4:<6}{'-'*50:<50}{'-'*8:>8}{'-'*8:>8}{'-'*8:>8}{'-'*8:>8}")
for i, (t, growth) in enumerate(growth_sorted[:30]):
    s22_24 = sum(t["years"].get(y, 0) for y in range(2022, 2025))
    s25_26 = sum(t["years"].get(y, 0) for y in (2025, 2026))
    cat = classification[t["term"]]
    cat_cn = {"basic": "基础", "clinical": "临床", "both": "交叉"}.get(cat, cat)
    p(f"  {i+1:<6}{t['term'][:50]:<50}{s22_24:>8}{s25_26:>8}{growth:>+8}{cat_cn:>8}")
p()

p("  4.5 衰退最快的术语 Top 20 (2022-2024 → 2025-2026)")
decline_sorted = sorted(growth_terms, key=lambda x: x[1])
p(f"  {'Rank':<6}{'Term':<50}{'2022-24':>8}{'2025-26':>8}{'变化':>8}{'类别':>8}")
p(f"  {'-'*4:<6}{'-'*50:<50}{'-'*8:>8}{'-'*8:>8}{'-'*8:>8}{'-'*8:>8}")
for i, (t, growth) in enumerate(decline_sorted[:20]):
    s22_24 = sum(t["years"].get(y, 0) for y in range(2022, 2025))
    s25_26 = sum(t["years"].get(y, 0) for y in (2025, 2026))
    cat = classification[t["term"]]
    cat_cn = {"basic": "基础", "clinical": "临床", "both": "交叉"}.get(cat, cat)
    p(f"  {i+1:<6}{t['term'][:50]:<50}{s22_24:>8}{s25_26:>8}{growth:>+8}{cat_cn:>8}")
p()

p("  4.6 2022→2026 逐年趋势追踪（精选核心术语）")
# Select core terms that appear across multiple years with decent frequency
core_basic = sorted(basic_terms, key=lambda t: sum(t["years"].get(y, 0) for y in range(2022, 2027)), reverse=True)[:15]
core_clinical = sorted(clinical_terms, key=lambda t: sum(t["years"].get(y, 0) for y in range(2022, 2027)), reverse=True)[:15]

p(f"\n  基础研究核心术语 (2022-2026 逐年级)")
header_line = f"  {'Term':<45}" + "".join(f"{y:>6}" for y in range(2022, 2027)) + f"{'Total':>6}"
p(header_line)
p(f"  {'-'*45:<45}{'-'*36}")
for t in core_basic:
    vals = "".join(f"{t['years'].get(y, 0):>6}" for y in range(2022, 2027))
    total = sum(t["years"].get(y, 0) for y in range(2022, 2027))
    p(f"  {t['term'][:45]:<45}{vals}{total:>6}")

p(f"\n  临床核心术语 (2022-2026 逐年级)")
p(header_line)
p(f"  {'-'*45:<45}{'-'*36}")
for t in core_clinical:
    vals = "".join(f"{t['years'].get(y, 0):>6}" for y in range(2022, 2027))
    total = sum(t["years"].get(y, 0) for y in range(2022, 2027))
    p(f"  {t['term'][:45]:<45}{vals}{total:>6}")

p()
p("=" * 80)
p("  报告结束")
p("=" * 80)

# ═══════════════════════════════════════════════════════════════
# WRITE REPORT
# ═══════════════════════════════════════════════════════════════
with open(r"D:\term\comprehensive-report.txt", "w", encoding="utf-8") as f:
    f.write("\n".join(report))

# ═══════════════════════════════════════════════════════════════
# WRITE CSV: burst terms with classification
# ═══════════════════════════════════════════════════════════════
with open(r"D:\term\burst-terms-full.csv", "w", newline="", encoding="utf-8-sig") as f:
    writer = csv.writer(f)
    writer.writerow(["TERM", "Category", "2025", "2026", "Total_2025_2026"])
    for t in burst_basic_sorted + burst_clinical_sorted:
        writer.writerow([
            t["term"],
            classification[t["term"]],
            t["years"].get(2025, 0),
            t["years"].get(2026, 0),
            sum_2025_2026(t)
        ])

# ═══════════════════════════════════════════════════════════════
# WRITE CSV: all terms with classification for further analysis
# ═══════════════════════════════════════════════════════════════
with open(r"D:\term\terms-classified.csv", "w", newline="", encoding="utf-8-sig") as f:
    writer = csv.writer(f)
    writer.writerow(["TERM", "Category", "Entropy"] +
                    [str(y) for y in range(2002, 2027)] +
                    ["2025", "2026", "Total_2025_2026", "Total_2022_2026"])
    for t in terms:
        row_data = [t["term"], classification[t["term"]], t["entropy"]]
        for y in range(2002, 2027):
            row_data.append(t["years"].get(y, 0))
        row_data.append(t["years"].get(2025, 0))
        row_data.append(t["years"].get(2026, 0))
        row_data.append(sum_2025_2026(t))
        row_data.append(sum_2022_2026(t))
        writer.writerow(row_data)

print(f"\nFiles written:")
print(f"  D:\\term\\comprehensive-report.txt")
print(f"  D:\\term\\burst-terms-full.csv")
print(f"  D:\\term\\terms-classified.csv")
