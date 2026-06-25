#!/usr/bin/env python3
"""
Filter term-entropy.csv to remove:
1. Function words / prepositions (虚词、介词)
2. Search/subject terms: "transcutaneous auricular vagus nerve stimulation"
   and its synonyms/abbreviations
"""

import csv
import re

INPUT = r"D:\term\term-entropy.csv"
OUTPUT = r"D:\term\term-entropy-filtered.csv"

# --- taVNS-related patterns (case-insensitive) ---
# Core strategy: catch all abbreviations and key phrases

TAVNS_PATTERNS = [
    # === Abbreviations (without strict \b to catch compounds like shamtvns, tavnss) ===
    r'tavns', r'ta[\s-]?vns',
    r'tvnss?', r't[\s-]?vns',
    r'avns', r'a[\s-]?vns',
    r'atvns', r'at[\s-]?vns',
    r'nvns', r'n[\s-]?vns',
    r'pavns', r'pa[\s-]?vns',
    r'll[\s-]?avns',
    r'ma[\s-]?avns',
    r'cl[\s-]?tavns',
    r'rg\s+tavns',
    r'\babvn\b',
    # Typo/compound variants
    r'shamtvns', r'stvns\b', r'tanvns', r'tnvns\b',
    r'ravans',      # typo for tavns
    r'vague\s+nerve',  # typo for vagus nerve

    # === Key phrases containing core concepts ===
    r'auricular\s+vagus',          # catches: auricular vagus nerve, auricular vagus stimulation, etc.
    r'auricular\s+vagal',          # auricular vagal nerve, auricular vagal afferent, etc.
    r'transcutaneous\s+vagus',     # transcutaneous vagus nerve, transcutaneous vagus stimulation
    r'transcutaneous\s+vagal',     # transcutaneous vagal stimulation
    r'transauricular\s+vagus',     # transauricular vagus nerve
    r'trans[\s-]?cutaneous\s+auricular\s+vag',  # trans-cutaneous auricular vagus/vagal
    r'auricular[\s-]vagus',        # auricular-vagus
    r'auriculo[\s-]vagal',         # auriculo-vagal
    r'auricular\s+point[\s-]?vagus',  # auricular point-vagus nerve stimulation
    r'non[\s-]?invasive\s+vagus',  # non-invasive vagus nerve stimulation
    r'non[\s-]?invasive\s+transcutaneous\s+vag',
    r'non[\s-]?invasive\s+auricular\s+vag',
    r'percutaneous\s+auricular\s+vag',
    r'electrical\s+auricular\s+vag',
    r'auricular\s+electrical\s+vagus',  # transcutaneous auricular electrical vagus nerve stimulation
    r'microneedle[\s-]assisted\s+(auricular\s+)?vag',
    r'closed[\s-]loop\s+(auricular\s+vag|transcutaneous\s+auricular|ta[\s-]?vns)',
    r'motor[\s-]activated\s+auricular\s+vag',
    r'respiratory[\s-]gated\s+(auricular\s+vag|transcutaneous\s+auricular)',
    r'home[\s-]based\s+(transcutaneous\s+auricular|respiratory[\s-]gated\s+transcutaneous|rg\s+tavns)',
    r'ear[\s-]eeg\s+transcutaneous\s+auricular',
    r'bilateral\s+(transcutaneous\s+auricular|auricular\s+point[\s-]?vag|synchronous\s+transcutaneous)',
    r'continuous\s+(transcutaneous\s+auricular|noninvasive\s+transcutaneous\s+auricular)',
    r'intermittent\s+transcutaneous\s+auricular',
    r'event[\s-]related\s+(phasic\s+)?transcutaneous\s+(auricular\s+)?vag',
    r'phasic\s+transcutaneous\s+vag',
    r'expiratory[\s-]gated\s+transcutaneous\s+vag',
    r'acute\s+(transcutaneous\s+auricular|transcutaneous\s+vagus|right[\s-]sided\s+transcutaneous)',
    r'accelerated\s+transcutaneous\s+auricular',
    r'optimized\s+transcutaneous\s+auricular',
    r'long[\s-]term\s+transcutaneous\s+auricular',
    r'multi[\s-]session\s+transcutaneous\s+auricular',
    r'multimodal\s+transcutaneous\s+auricular',
    r'nightly\s+bilateral\s+transcutaneous\s+auricular',
    r'off[\s-]line\s+auricular\s+transcutaneous',
    r'low[\s-]level\s+(transcutaneous\s+auricular|transcutaneous\s+vagus|auricular\s+vagus|ta[\s-]?vns)',
    r'low[\s-]intensity\s+transcutaneous\s+auricular',
    r'low[\s-]frequency\s+auricular\s+vagus',
    r'microneedle[\s-]based\s+tavns',
    r'button[\s-]style\s+transcutaneous\s+(auricular\s+)?vag',
    r'auricular\s+branch\s+(of\s+(the\s+)?)?vagus\s+nerve',
    r'auricular\s+cutaneous\s+vagal',
    r'auricular\s+nerve\s+stimulation',
    r'auricular\s+(tvns|tavns|vns)\b',
    r'transcutaneous\s+vagus\s+nerve\s+stimulator',
    r'transauricular\s+stimulation',        # taVNS synonym
    r'transcutaneous\s+auricular\s+vn\b',   # vn = vagus nerve abbreviation
    r'auricular\s+vn\b',                    # vn = vagus nerve abbreviation
    r'auricular\s+transcutaneous\s+vns',    # auricular transcutaneous VNS
    r'tragus\s+vagus\s+nerve\s+stimulat',   # tragus is the auricular site for taVNS
    r'vagal\s+auricular\s+branch',          # vagal auricular branch
    r'vagal\s+auricular\s+innervation',     # vagal auricular innervation
    r'ricular\s+vagus\s+nerve',             # typo: missing "au" from auricular
    r'transcu[\s-]taneous\s+vagus\s+nerve', # typo: transcu-taneous
    r'transcutanecous\s+vagus\s+nerve',     # typo: transcutanecous
    r'noninvasive\s+transcutaneous\s+auricular\s+branch\s+vns',
]

tavns_re = re.compile('|'.join(TAVNS_PATTERNS), re.IGNORECASE)

# --- Function words & prepositions ---
FUNC_WORDS = {
    'the', 'a', 'an',
    'of', 'in', 'on', 'at', 'by', 'for', 'with', 'to', 'from',
    'and', 'or', 'but', 'if', 'nor', 'so', 'yet', 'as', 'than',
    'into', 'upon', 'within', 'without', 'during', 'above', 'below',
    'between', 'through', 'under', 'over', 'after', 'before',
    'among', 'along', 'toward', 'about', 'despite', 'including',
    'although', 'because', 'until', 'since', 'while',
    'per', 'via', 'vs', 'versus',
    'using', 'used', 'based', 'given', 'due',
    'not', 'no', 'just', 'very', 'too', 'also', 'now', 'then',
    'here', 'there', 'how', 'what', 'why', 'when', 'where',
    'it', 'its', 'he', 'she', 'they', 'them', 'we', 'us',
    'my', 'your', 'our', 'their', 'his', 'her',
    'this', 'that', 'these', 'those',
    'all', 'each', 'every', 'both', 'few', 'more', 'most',
    'other', 'some', 'such', 'only', 'own', 'same', 'any',
    'is', 'are', 'was', 'were', 'be', 'been', 'being',
    'have', 'has', 'had', 'having',
    'do', 'does', 'did', 'doing',
    'will', 'would', 'shall', 'should', 'may', 'might', 'must',
    'can', 'could',
}

def is_func_word(term: str) -> bool:
    t = term.strip().lower()
    if t in FUNC_WORDS:
        return True
    for fw in FUNC_WORDS:
        if t.startswith(fw + ' ') or t.startswith(fw + '('):
            return True
    return False

def main():
    removed_tavns = 0
    removed_func = 0
    kept = 0
    total = 0

    with open(INPUT, 'r', encoding='utf-8-sig') as fin, \
         open(OUTPUT, 'w', encoding='utf-8-sig', newline='') as fout:
        reader = csv.reader(fin)
        writer = csv.writer(fout)
        header = next(reader)
        writer.writerow(header)
        total = 1

        for row in reader:
            total += 1
            term = row[0].strip() if row else ''

            if tavns_re.search(term):
                removed_tavns += 1
                continue
            if is_func_word(term):
                removed_func += 1
                continue

            writer.writerow(row)
            kept += 1

    print(f"Total rows (excl header): {total - 1}")
    print(f"Removed - taVNS related:    {removed_tavns}")
    print(f"Removed - function words:   {removed_func}")
    print(f"Kept:                       {kept}")
    print(f"Output: {OUTPUT}")

if __name__ == '__main__':
    main()
