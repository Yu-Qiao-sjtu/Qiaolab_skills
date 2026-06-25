import csv
import re
from collections import defaultdict, Counter

# ============================================================
# 语义分类规则 — 基于 taVNS / 神经调控领域
# 每个类别的关键词用正则匹配（忽略大小写）
# ============================================================

CATEGORIES = {
    "神经影像 (Neuroimaging)": [
        r"\bfmri\b", r"\bee?g\b", r"\bmeg\b", r"\bpet\b", r"\bspect\b", r"\bnirs\b",
        r"\bfunctional (?:magnetic resonance|connectivity|mri)\b",
        r"\bresting[- ]state\b", r"\bbrain (?:network|connectivity|connectome)\b",
        r"\bdefault mode\b", r"\bsalience network\b", r"\bexecutive (?:control )?network\b",
        r"\bcentral executive\b", r"\bfrontoparietal\b", r"\bconnectivity\b",
        r"\bfractional amplitude\b", r"\bregional homogeneity\b", r"\bfalff\b", r"\breho\b",
        r"\bblood oxygen\b", r"\bbold\b", r"\bfunctional imaging\b", r"\bneuroimaging\b",
        r"\bvoxel\b", r"\broi\b", r"\bregion of interest\b", r"\bseed[- ]based\b",
        r"\bgraph theory\b", r"\bnode degree\b", r"\bbetweenness\b",
        r"\bstructural connectivity\b", r"\bdiffusion tensor\b", r"\bdti\b",
        r"\bwhite matter\b", r"\bgrey matter\b", r"\bgray matter\b",
    ],
    "脑区/神经解剖 (Brain Regions & Anatomy)": [
        r"\blocus coeruleus\b", r"\bnucleus (?:tractus solitari[ui]s|of the solitary)\b",
        r"\bnts\b", r"\bdorsal raphe\b", r"\braphe nuclei\b", r"\bperiaqueductal\b",
        r"\bprefrontal cortex\b", r"\bdorsolateral prefrontal\b", r"\bdlpfc\b",
        r"\bventromedial prefrontal\b", r"\bvm?pfc\b", r"\banterior cingulate\b", r"\bacc\b",
        r"\bposterior cingulate\b", r"\binsula\b", r"\bamygdala\b", r"\bhippocampus\b",
        r"\bhippocampal\b", r"\bparahippocamp\b", r"\bthalamus\b", r"\bthalamic\b",
        r"\bhypothalamus\b", r"\bhypothalamic\b", r"\bbasal ganglia\b", r"\bstriatum\b",
        r"\bstriatal\b", r"\bnucleus accumbens\b", r"\bventral tegmental\b", r"\bvta\b",
        r"\bsubstantia nigra\b", r"\bcerebellum\b", r"\bcerebellar\b", r"\bbrainstem\b",
        r"\bmedulla\b", r"\bmedullary\b", r"\bpontine\b", r"\bpons\b",
        r"\bauricular branch\b", r"\bcymba conchae\b", r"\bconcha\b", r"\bexternal ear\b",
        r"\bpinna\b", r"\befc\b", r"\bexecutive function\b", r"\bworking memory\b",
        r"\bsuperior (?:temporal|frontal|parietal)\b", r"\binferior (?:temporal|frontal|parietal)\b",
        r"\bmiddle (?:temporal|frontal)\b",
        r"\bmedial (?:prefrontal|temporal)\b", r"\blateral (?:prefrontal|temporal)\b",
        r"\boccipital\b", r"\bparietal\b", r"\btemporal lobe\b", r"\bfrontal lobe\b",
        r"\borbitofrontal\b", r"\bsomatosensory\b", r"\bmotor cortex\b",
        r"\bprimary motor\b", r"\bsupplementary motor\b", r"\bsma\b",
    ],
    "自主神经/心血管 (Autonomic & Cardiovascular)": [
        r"\bheart rate variability\b", r"\bhrv\b", r"\bheart rate\b",
        r"\bblood pressure\b", r"\bsystolic\b", r"\bdiastolic\b", r"\bhypertension\b",
        r"\bhypotension\b", r"\bbaroreflex\b", r"\bbaroreceptor\b",
        r"\bcardiac\b", r"\bcardiovascular\b", r"\becg\b", r"\belectrocardiogram\b",
        r"\bheart failure\b", r"\bmyocardial\b", r"\barrhythmia\b",
        r"\bautonomic (?:nervous system|function|regulation|tone|balance|dysfunction)\b",
        r"\bans\b", r"\bsympathetic\b", r"\bparasympathetic\b", r"\bvagal tone\b",
        r"\bvagal activity\b", r"\bvagal (?:nerve )?stimulation\b",
        r"\bsympathovagal\b", r"\bpolyvagal\b", r"\bdorsal vagal\b",
        r"\bvagal (?:afferent|efferent|pathway|withdrawal|modulation)\b",
        r"\bcholinergic anti.?inflammatory\b", r"\bvasodilation\b", r"\bvasoconstriction\b",
        r"\bgalvanic skin\b", r"\bgsr\b", r"\bskin conductance\b", r"\bpupil\b",
        r"\bpupillometry\b", r"\bpupillary\b",
    ],
    "临床结局 (Clinical Outcomes)": [
        r"\bdepression\b", r"\bdepressive\b", r"\bmajor depressive\b", r"\bmdd\b",
        r"\banxiety\b", r"\bgeneralized anxiety\b", r"\bgad[\s\-]?\d*\b",
        r"\bstress\b", r"\bpost.?traumatic stress\b", r"\bptsd\b",
        r"\bpain\b", r"\banalgesia\b", r"\banalgesic\b", r"\bpainful\b",
        r"\bpostoperative pain\b", r"\bchronic pain\b", r"\bneuropathic pain\b",
        r"\bmigraine\b", r"\bheadache\b", r"\bfibromyalgia\b",
        r"\bepilepsy\b", r"\bepileptic\b", r"\bseizure\b", r"\banti.?epileptic\b",
        r"\binsomnia\b", r"\bsleep\b", r"\bsleep quality\b", r"\bwake\b",
        r"\bcognitive (?:function|impairment|decline|performance|enhancement|outcome)\b",
        r"\bdementia\b", r"\balzheimer\b", r"\bparkinson\b", r"\bpd\b",
        r"\bstroke\b", r"\bpoststroke\b", r"\bpost.?stroke\b", r"\bischemic\b",
        r"\btinnitus\b", r"\bhearing loss\b",
        r"\binflammat(?:ory|ion)\b", r"\bcytokine\b", r"\binterleukin\b", r"\bcrp\b",
        r"\bdelirium\b", r"\bpostoperative delirium\b", r"\bemergence delirium\b",
        r"\bnausea\b", r"\bvomiting\b", r"\bponv\b",
        r"\badverse (?:event|effect|reaction)\b", r"\bside effect\b", r"\bsafety\b",
        r"\bquality of life\b", r"\bqol\b", r"\bwell.?being\b",
        r"\bfatigue\b", r"\bdizziness\b", r"\bvertigo\b",
        r"\bobesity\b", r"\bdiabetes\b", r"\bmetabolic syndrome\b", r"\bglucose\b",
        r"\bgastrointestinal\b", r"\bgastric\b", r"\bgastroparesis\b",
        r"\bdrug.?resistant\b", r"\btreatment.?resistant\b",
        r"\brefractory\b", r"\bremission\b", r"\brecovery\b", r"\brecurrence\b",
        r"\bsuicide\b", r"\bsuicidal\b",
        r"\bpain intensity\b", r"\bvas\b", r"\bvisual (?:analog|analogue) scale\b",
        r"\bhamilton\b", r"\bham.?d\b", r"\bham.?a\b", r"\bbleulerian\b",
        r"\bmadrs\b", r"\bmontgomery\b", r"\bbdi\b", r"\bbeck depression\b",
        r"\bclinical improvement\b", r"\bclinical response\b", r"\bresponder\b",
        r"\btherapeutic (?:effect|outcome|response|benefit)\b",
        r"\befficacy\b", r"\beffective\b", r"\beffectiveness\b",
    ],
    "方法学/试验设计 (Methodology & Trial Design)": [
        r"\brandomi[sz]ed\b", r"\brandomly\b", r"\brandom assignment\b",
        r"\bcontrolled trial\b", r"\brct\b", r"\brandomized controlled\b",
        r"\bsham\b", r"\bplacebo\b", r"\bblinding\b", r"\bdouble.?blind\b",
        r"\bsingle.?blind\b", r"\btriple.?blind\b", r"\ballocation\b",
        r"\bcontrol group\b", r"\bcontrolled study\b", r"\bcomparison group\b",
        r"\bactive (?:control|comparator)\b",
        r"\bprimary outcome\b", r"\bsecondary outcome\b", r"\bprimary endpoint\b",
        r"\boutcome measure\b", r"\bendpoint\b",
        r"\binclusion criteria\b", r"\bexclusion criteria\b", r"\beligibility\b",
        r"\bstudy (?:design|protocol|population)\b",
        r"\bsample size\b", r"\bpower analysis\b", r"\bstatistical\b",
        r"\bsignificant (?:difference|change)\b", r"\bp[-\s]?value\b",
        r"\bconfidence interval\b", r"\banalysis of variance\b", r"\banova\b",
        r"\bt[-\s]?test\b", r"\bchi.?square\b", r"\bmann.?whitney\b",
        r"\bwilcoxon\b", r"\bkruskal.?wallis\b", r"\bfriedman\b",
        r"\bregression\b", r"\bcorrelation\b", r"\bpearson\b", r"\bspearman\b",
        r"\bmultiple comparis\b", r"\bbonferroni\b", r"\bfdr\b",
        r"\bpilot (?:study|trial)\b", r"\bfeasibility\b",
        r"\bprotocol\b", r"\bregistered\b", r"\bprisma\b",
        r"\bsystematic review\b", r"\bmeta.?analysis\b", r"\bmeta.?analytic\b",
        r"\bnetwork meta.?analysis\b", r"\bumbrella review\b",
        r"\bcrossover\b", r"\bparallel (?:group|arm)\b", r"\bopen.?label\b",
        r"\bintention.?to.?treat\b", r"\bper.?protocol\b",
        r"\bpre.?registered\b", r"\bpreregister\b",
        r"\bfollow.?up\b", r"\blong.?term\b", r"\bshort.?term\b",
        r"\bclinical trial\b", r"\bclinical research\b",
        r"\badverse event\b", r"\bserious adverse\b", r"\bsae\b",
    ],
    "机制/通路 (Mechanisms & Pathways)": [
        r"\bmechanism\b", r"\bpathway\b", r"\bsignaling\b", r"\bpathophysiolog\b",
        r"\bneurotransmitter\b", r"\bdopamine\b", r"\bdopaminergic\b",
        r"\bserotonin\b", r"\bserotonergic\b", r"\bnoradrenaline\b", r"\bnorepinephrine\b",
        r"\bnoradrenergic\b", r"\bacetylcholine\b", r"\bcholinergic\b",
        r"\bgaba\b", r"\bglutamate\b", r"\bglutamatergic\b",
        r"\bneuropeptide\b", r"\boxytocin\b", r"\bvasopressin\b",
        r"\bneuroplasticity\b", r"\blong.?term potentiation\b", r"\blong.?term depression\b",
        r"\bltp\b", r"\bltd\b", r"\bsynaptic\b", r"\bsynaptogenesis\b",
        r"\bneurogenesis\b", r"\bbdnf\b", r"\bbrain.?derived neurotrophic\b",
        r"\bnerve growth factor\b", r"\bngf\b",
        r"\bhypothalamic.?pituitary.?adrenal\b", r"\bhpa axis\b",
        r"\bcortisol\b", r"\bendocrine\b", r"\bhormone\b",
        r"\bcytokine\b", r"\binterleukin\b", r"\bil[-\s]?\d+\b", r"\btnf[-\s]?\w*\b",
        r"\bcrp\b", r"\bc.?reactive protein\b",
        r"\bimmune\b", r"\bimmunological\b", r"\bimmunomodulation\b",
        r"\boxidative stress\b", r"\bantioxidant\b", r"\breactive oxygen\b", r"\bros\b",
        r"\bapoptosis\b", r"\bautophagy\b", r"\bmicroglia\b", r"\bneuroinflammation\b",
        r"\bblood.?brain barrier\b", r"\bbbb\b",
        r"\bgene expression\b", r"\bepigenetic\b", r"\bdna methylation\b",
        r"\balpha[-\s]?\d* synuclein\b",
    ],
    "刺激参数/技术 (Stimulation Parameters & Technology)": [
        r"\bstimulation (?:parameter|protocol|frequency|intensity|duration|site)\b",
        r"\bpulse width\b", r"\bpulse duration\b", r"\bpulse frequency\b",
        r"\bfrequency\b", r"\bintensity\b", r"\bamplitude\b",
        r"\bcurrent intensity\b", r"\bcurrent amplitude\b",
        r"\belectrical stimulation\b", r"\belectric current\b",
        r"\btranscutaneou?s\b", r"\btranscutaneously\b",
        r"\bpercutaneous\b", r"\bnon.?invasive\b",
        r"\bduty cycle\b", r"\bwaveform\b", r"\bmonophasic\b", r"\bbiphasic\b",
        r"\bcontinuous stimulation\b", r"\bintermittent stimulation\b",
        r"\bduration of stimulation\b", r"\bstimulation duration\b",
        r"\bsession\b", r"\brepeated session\b", r"\bmultiple session\b",
        r"\bneuromodulation\b", r"\bneurostimulation\b", r"\bneural modulation\b",
        r"\bdevice\b", r"\belectrode\b", r"\bimplantable\b", r"\bpacemaker\b",
        r"\belectrical nerve stimulation\b", r"\btens\b", r"\bneuromodulator\b",
        r"\bclosed.?loop\b", r"\bopen.?loop\b",
        r"\bcurrent (?:range|level|density)\b",
    ],
    "人群/被试 (Populations & Participants)": [
        r"\bhealthy (?:adults|participants|subjects|volunteers|controls|individuals)\b",
        r"\bhealthy control\b", r"\bhealthy young\b", r"\bhealthy older\b",
        r"\bpatients?\b", r"\bparticipants?\b", r"\bsubjects?\b",
        r"\bvolunteers?\b", r"\bmale\b", r"\bfemale\b", r"\bgender\b",
        r"\bsex (?:difference|ratio|distribution)\b",
        r"\bchildren\b", r"\badolescents?\b", r"\bpediatric\b", r"\bneonatal\b",
        r"\bolder adults?\b", r"\belderly\b", r"\baged\b", r"\baging\b",
        r"\bpregnant\b", r"\bgestational\b",
        r"\bcomorbidity\b", r"\bcomorbid\b",
        r"\bsurgical patients?\b", r"\bpostoperative patients?\b",
        r"\bperioperative\b", r"\bpreoperative\b",
        r"\bemergency (?:department|patients?)\b",
    ],
    "精神/认知/心理 (Mental & Cognitive)": [
        r"\bemotion\b", r"\bemotional\b", r"\bmood\b", r"\baffective\b",
        r"\bcognition\b", r"\bcognitive\b", r"\battention\b", r"\battentional\b",
        r"\bexecutive function\b", r"\bworking memory\b", r"\bmemory\b",
        r"\bepisodic memory\b", r"\blearning\b", r"\bdecision.?making\b",
        r"\bimpulsivity\b", r"\breward\b", r"\bmotivation\b",
        r"\bsocial cognition\b", r"\btheory of mind\b", r"\bempathy\b",
        r"\bconsciousness\b", r"\bawareness\b", r"\barousal\b",
        r"\breaction time\b", r"\bresponse time\b", r"\baccuracy\b",
        r"\bvigilance\b", r"\balertness\b",
        r"\bpsychiatric\b", r"\bpsychological\b", r"\bmental health\b",
        r"\bpsychosis\b", r"\bpsychotic\b", r"\bschizophrenia\b",
        r"\bbipolar\b", r"\bmania\b",
        r"\bpersonality\b", r"\bneuroticism\b", r"\bextraversion\b",
        r"\bresilience\b", r"\bcoping\b", r"\bself.?regulation\b",
        r"\bautism\b", r"\basd\b", r"\badhd\b", r"\battention deficit\b",
    ],
    "生物标记/生理测量 (Biomarkers & Physiological Measures)": [
        r"\bbiomarker\b", r"\bprognostic\b", r"\bdiagnostic\b",
        r"\bheart rate\b", r"\bpulse\b", r"\bheart rate variability\b",
        r"\bblood sample\b", r"\bserum\b", r"\bplasma\b", r"\bcsf\b",
        r"\bcerebrospinal\b", r"\bsaliva\b", r"\burine\b",
        r"\bcortisol\b", r"\bneuroendocrine\b",
        r"\bevoked potential\b", r"\bvep\b", r"\baep\b", r"\bsep\b",
        r"\bmismatch negativity\b", r"\bmmn\b", r"\bp300\b", r"\bp3a\b", r"\bp3b\b",
        r"\bemg\b", r"\belectromyography\b",
        r"\beye tracking\b", r"\beye.?tracking\b", r"\bsaccade\b",
        r"\bactigraphy\b", r"\bactigraph\b",
    ],
    "应用/适应症 (Applications & Indications)": [
        r"\bclinical application\b", r"\bclinical use\b", r"\bapplication\b",
        r"\btherapeutic\b", r"\btreatment\b", r"\btherapy\b", r"\bmanagement\b",
        r"\bneuromodulation (?:therapy|treatment)\b",
        r"\bpostoperative\b", r"\bperioperative\b", r"\bsurgical\b",
        r"\bintraoperative\b", r"\banesthesia\b", r"\banesthetic\b",
        r"\bpostoperative nausea\b", r"\bponv\b",
        r"\bpostoperative cognitive\b", r"\bpostoperative delirium\b",
        r"\brehabilitation\b", r"\bphysical therapy\b",
        r"\bchronic disease\b", r"\bchronic illness\b",
        r"\bindication\b", r"\bcontraindication\b",
        r"\bbioelectronic medicine\b", r"\belectroceutical\b",
        r"\bdigital (?:health|therapeutics?|medicine)\b",
        r"\bwearable\b", r"\bhome.?based\b", r"\bself.?administration\b",
        r"\bportable\b", r"\bpoint.?of.?care\b",
        r"\bclinical translation\b", r"\btranslation\b",
        r"\bprecision medicine\b", r"\bpersonalized\b",
    ],
}

# ------------------------------------------------------------
# 读取数据
# ------------------------------------------------------------
with open(r"D:\term\term-2025-2026.csv", "r", encoding="utf-8-sig") as f:
    reader = csv.DictReader(f)
    rows = list(reader)
# normalize header (strip BOM / whitespace)
if rows:
    new_rows = []
    for r in rows:
        nr = {}
        for k, v in r.items():
            nr[k.strip().strip('\ufeff')] = v
        new_rows.append(nr)
    rows = new_rows

# 预处理
for r in rows:
    r["Total"] = int(r["Total"])
    r["2025"] = int(r["2025"])
    r["2026"] = int(r["2026"])
    r["Entropy"] = float(r["Entropy"])

# ------------------------------------------------------------
# 归类
# ------------------------------------------------------------
cat_map = {}          # term -> list of categories
cat_terms = defaultdict(list)
for r in rows:
    term = r["TERM"].lower().strip()
    matched = []
    for cat, patterns in CATEGORIES.items():
        for pat in patterns:
            if re.search(pat, term):
                matched.append(cat)
                break
    if not matched:
        matched = ["其他 (Other)"]
    cat_map[term] = matched
    for c in matched:
        cat_terms[c].append(r)

# ------------------------------------------------------------
# 全盘统计
# ------------------------------------------------------------
term_set = {r["TERM"] for r in rows}
total_terms = len(term_set)
cat_counts = {c: len(set(r["TERM"] for r in lst)) for c, lst in cat_terms.items()}
cat_freq_2025 = {c: sum(r["2025"] for r in lst) for c, lst in cat_terms.items()}
cat_freq_2026 = {c: sum(r["2026"] for r in lst) for c, lst in cat_terms.items()}
cat_freq_total = {c: cat_freq_2025[c] + cat_freq_2026[c] for c in cat_terms}

# 排序类别
sorted_cats = sorted(cat_terms.keys(), key=lambda c: cat_freq_total[c], reverse=True)

# ------------------------------------------------------------
# 2026-only 分析
# ------------------------------------------------------------
only_2026 = [r for r in rows if r["2025"] == 0 and r["2026"] > 0]
only_2025 = [r for r in rows if r["2025"] > 0 and r["2026"] == 0]
both_years = [r for r in rows if r["2025"] > 0 and r["2026"] > 0]

cat_only_2026 = defaultdict(list)
for r in only_2026:
    for c in cat_map[r["TERM"].lower().strip()]:
        cat_only_2026[c].append(r)

# ------------------------------------------------------------
# 输出
# ------------------------------------------------------------
out_path = r"D:\term\semantic-analysis-report.txt"

with open(out_path, "w", encoding="utf-8") as out:
    def p(s=""):
        out.write(s + "\n")

    p("=" * 80)
    p("  2025–2026 taVNS 领域术语语义分析报告")
    p("=" * 80)
    p(f"\n总术语数: {total_terms:,}")
    p(f"2025年出现: {len(only_2025) + len(both_years):,}")
    p(f"2026年出现: {len(only_2026) + len(both_years):,}")
    p(f"仅在2025: {len(only_2025):,}")
    p(f"仅在2026: {len(only_2026):,}")
    p(f"两年均出现: {len(both_years):,}")

    p()
    p("=" * 80)
    p("  一、语义类别总体分布")
    p("=" * 80)
    p(f"\n{'类别':<50} {'术语数':>6} {'2025频次':>10} {'2026频次':>10} {'总计':>8}")
    p("-" * 90)
    for c in sorted_cats:
        p(f"{c:<50} {cat_counts[c]:>6} {cat_freq_2025[c]:>10} {cat_freq_2026[c]:>10} {cat_freq_total[c]:>8}")
    p("-" * 90)
    p(f"{'合计':<50} {sum(cat_counts.values()):>6} {sum(cat_freq_2025.values()):>10} {sum(cat_freq_2026.values()):>10} {sum(cat_freq_total.values()):>8}")

    p()
    p("=" * 80)
    p("  二、各类别 Top 高频术语 (按2025+2026总计)")
    p("=" * 80)
    for c in sorted_cats:
        p(f"\n--- {c} ---")
        top = sorted(cat_terms[c], key=lambda r: r["Total"], reverse=True)[:15]
        for t in top:
            p(f"  {t['TERM']:<60} 2025:{t['2025']:>3}  2026:{t['2026']:>3}  合计:{t['Total']:>4}  熵:{t['Entropy']:.2f}")

    p()
    p("=" * 80)
    p("  三、仅2026年新出现的高频术语 Top 30")
    p("=" * 80)
    top_new_2026 = sorted(only_2026, key=lambda r: r["2026"], reverse=True)[:30]
    for t in top_new_2026:
        cats = cat_map[t["TERM"].lower().strip()]
        p(f"  {t['TERM']:<60} 2026:{t['2026']:>3}  [{'; '.join(cats)}]")

    p()
    p("=" * 80)
    p("  四、仅2026年新出现术语 — 按类别分布")
    p("=" * 80)
    p()
    for c in sorted_cats:
        if c in cat_only_2026:
            top_c = sorted(cat_only_2026[c], key=lambda r: r["2026"], reverse=True)[:10]
            total_c = len(cat_only_2026[c])
            freq_c = sum(r["2026"] for r in cat_only_2026[c])
            p(f"\n--- {c} (新术语{total_c}个, 频次{freq_c}) ---")
            for t in top_c:
                p(f"  {t['TERM']:<60} 2026:{t['2026']:>3}")

    p()
    p("=" * 80)
    p("  五、类别间对比: 2025 vs 2026 频次变化")
    p("=" * 80)
    p(f"\n{'类别':<50} {'2025':>8} {'2026':>8} {'变化':>8} {'变化%':>10}")
    p("-" * 90)
    for c in sorted_cats:
        f25 = cat_freq_2025[c]
        f26 = cat_freq_2026[c]
        delta = f26 - f25
        pct = (delta / f25 * 100) if f25 > 0 else float('inf')
        pct_str = f"{pct:+.1f}%" if pct != float('inf') else "∞"
        p(f"{c:<50} {f25:>8} {f26:>8} {delta:>+8} {pct_str:>10}")

    p()
    p("=" * 80)
    p("  六、跨类别高频术语 (出现在多个类别)")
    p("=" * 80)
    multi = [(t, cs) for t, cs in cat_map.items() if len(cs) > 1]
    multi.sort(key=lambda x: len(x[1]), reverse=True)
    for term, cats in multi[:20]:
        freq_r = next(r for r in rows if r["TERM"].lower().strip() == term)
        p(f"  [{len(cats)}类] {freq_r['TERM']:<55} 合计:{freq_r['Total']:>4}  [{'; '.join(cats)}]")

print(f"\n报告已保存至: {out_path}")
print(f"术语总数: {total_terms}")
print(f"类别数: {len(CATEGORIES) + 1}")
