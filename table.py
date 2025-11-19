import re
import sys
from pathlib import Path
from typing import Dict, List
import csv


RESULTS_PATH = Path(__file__).with_name("results.txt")

# flexible extraction regexes
INSTANCE_RE = re.compile(r'^\s*(\S+)')
N_EQ_RE = re.compile(r'\bn\s*[:=]\s*(\d+)\b', re.I)
N_IN_NAME_RE = re.compile(r'-(\d{3,})\b')
NUMBER_RE = re.compile(r'(\d{3,})')  # fallback for any large number

# candidate labels for columns
LABEL_PATTERNS = {
    'A': [r'\bA\b', r'\bAlternate\b'],
    'F': [r'\bF\b', r'\bFew\b'],
    'M': [r'\bM\b', r'\bMany\b'],
    'N': [r'\bN\b', r'\bNone\b'],
    'S': [r'\bS\b', r'\bSome\b'],
}

VALUE_RE_TEMPLATE = r'{}\s*[:=]?\s*([^\s,;]+)'

def extract_value(line: str, label_patterns: List[str]) -> str:
    for pat in label_patterns:
        m = re.search(VALUE_RE_TEMPLATE.format(pat), line, re.I)
        if m:
            return m.group(1)
    return '--'

def extract_n(instance: str, line: str) -> int | None:
    # try explicit n=... in line
    m = N_EQ_RE.search(line)
    if m:
        return int(m.group(1))
    # try number in instance name like name-5762
    m = N_IN_NAME_RE.search(instance)
    if m:
        return int(m.group(1))
    # fallback: any 3+ digit number in line
    m = NUMBER_RE.search(line)
    if m:
        return int(m.group(1))
    return None
def parse_results(path: Path) -> List[Dict]:
    rows = []
    text = path.read_text(encoding='utf-8')
    lines = [l for l in text.splitlines() if l.strip()]
    if not lines:
        return rows

    # Try CSV first if it looks like CSV
    first = lines[0]
    if ',' in first and ('instance' in first.lower() or 'instance_name' in first.lower()) and 'n' in first.lower():
        reader = csv.DictReader(lines)
        for r in reader:
            # accept either 'instance' or 'instance_name'
            inst = r.get('instance') or r.get('instance_name') or r.get('Instance') or ''
            if not inst:
                continue
            n_raw = r.get('n') or r.get('N') or ''
            try:
                n = int(n_raw)
            except Exception:
                # try to extract digits
                m = re.search(r'(\d+)', n_raw)
                if m:
                    n = int(m.group(1))
                else:
                    continue
            if n < 500:
                continue
            row = {'instance': inst, 'n': n}
            # columns A,F,M,N,S - try multiple header names
            row['A'] = r.get('A') or r.get('Alternate') or r.get('alternate') or '--'
            row['F'] = r.get('F') or r.get('Few') or '--'
            row['M'] = r.get('M') or r.get('Many') or '--'
            row['N'] = r.get('N') or r.get('None') or '--'
            row['S'] = r.get('S') or r.get('Some') or '--'
            rows.append(row)
        return rows

    # fallback: legacy line-based parsing
    for line in lines:
        inst_m = INSTANCE_RE.match(line)
        if not inst_m:
            continue
        inst = inst_m.group(1)
        n = extract_n(inst, line)
        if n is None or n < 500:
            continue
        row = {'instance': inst, 'n': n}
        for col, patterns in LABEL_PATTERNS.items():
            row[col] = extract_value(line, patterns)
        rows.append(row)
    return rows


# ...existing code...

def make_latex_table(rows: List[Dict]) -> str:
    header = (
        "\\begin{tabular}{lrrrrrr}\n"
        "  \\toprule\n"
        "  Instance name & $n$ & A & F & M & N & S \\\\\n"
        "  \\midrule\n"
    )
    body = ""
    for r in rows:
        nfmt = f"{r['n']:,}"
        body += f"  {r['instance']} & {nfmt} & {r['A']} & {r['F']} & {r['M']} & {r['N']} & {r['S']} \\\\\n"
    footer = "  \\bottomrule\n\\end{tabular}\n"
    return header + body + footer

def make_three_tables(rows: List[Dict], first: int = 33, second: int = 33) -> str:
    groups = [
        rows[:first],
        rows[first:first + second],
        rows[first + second:]
    ]
    tables = []
    for idx, grp in enumerate(groups, start=1):
        if not grp:
            continue
        tbl = make_latex_table(grp)
        caption = f"% Table chunk {idx}: rows { (0 if idx==1 else (first if idx==2 else first+second)) } - etc\n"
        tables.append(caption + tbl)
    return "\n\n".join(tables)

def main(path: Path = RESULTS_PATH):
    if not path.exists():
        print(f"results.txt not found at {path}", file=sys.stderr)
        sys.exit(1)
    rows = parse_results(path)
    if not rows:
        print("No instances with n >= 500 found.", file=sys.stderr)
        sys.exit(0)
    latex = make_three_tables(rows, first=33, second=33)
    out_tex = path.with_name("results_table.tex")
    out_tex.write_text(latex, encoding='utf-8')
    print(latex)

if __name__ == "__main__":
    p = Path(sys.argv[1]) if len(sys.argv) > 1 else RESULTS_PATH
    main(p)