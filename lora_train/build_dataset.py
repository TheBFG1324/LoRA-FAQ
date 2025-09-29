import json, re, pathlib, bs4, re, pathlib
from collections import Counter

raw = pathlib.Path("data/alexander_hamilton.html").read_text(encoding="utf-8")

soup = bs4.BeautifulSoup(raw, "html.parser")
for sup in soup.select("sup.reference"): sup.decompose()
text = soup.select_one("#mw-content-text").get_text("\n")
open("data/hamilton.txt","w").write(text)
print("Wrote data/hamilton.txt")

src = pathlib.Path("data/hamilton.txt").read_text()
# split on sentence-ish boundaries
sentences = re.split(r'(?<=[.!?])\s+', src)
quotes = [s.strip() for s in sentences if '"' in s and len(s.split())>6]

def pick_keywords(s, k=3):
    # naive keyword pick: most frequent capitalized tokens + nouns-ish
    tokens = re.findall(r"[A-Za-z][A-Za-z\-']+", s)
    caps = [t for t in tokens if t[0].isupper() and t.lower() not in {"the","and","of","to","in"}]
    common = [w for w,_ in Counter(tokens).most_common(20)]
    cand = list(dict.fromkeys(caps + common))  # keep order, dedupe
    return ", ".join(cand[:k]) or "Alexander Hamilton"

pathlib.Path("data").mkdir(exist_ok=True, parents=True)
with open("data/quotes.jsonl","w") as f:
    for s in quotes:
        kws = pick_keywords(s)
        prompt = f'Give a quote about {kws}.'
        resp = f'{s} — (Alexander Hamilton, Wikipedia)'
        f.write(json.dumps({"prompt": prompt, "response": resp})+"\n")

print(f"Wrote {len(quotes)} quote pairs to data/quotes.jsonl")
