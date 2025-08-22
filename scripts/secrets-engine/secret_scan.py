#!/usr/bin/env python3
import argparse, base64, fnmatch, json, math, os, re, sys, yaml

def shannon_entropy(s):
    if not s: return 0.0
    from collections import Counter
    counts = Counter(s)
    length = len(s)
    return -sum((c/length) * math.log2((c/length)) for c in counts.values())

def load_patterns(path):
    with open(path) as f:
        cfg = yaml.safe_load(f)
    pats = [(p["id"], re.compile(p["regex"]), p["severity"]) for p in cfg.get("patterns", [])]
    entropy_cfg = cfg.get("entropy", {"enabled": False})
    return pats, entropy_cfg

def should_skip(path, excludes):
    return any(fnmatch.fnmatch(path, pat) for pat in excludes)

def scan_file(path, pats, entropy_cfg):
    findings = []
    try:
        with open(path, "r", errors="ignore") as f:
            for idx, line in enumerate(f, 1):
                for pid, preg, sev in pats:
                    if preg.search(line):
                        findings.append({"file": path, "line": idx, "id": pid, "severity": sev,
                                         "confidence": 0.9, "excerpt": line.strip()[:200]})
                if entropy_cfg.get("enabled", False):
                    tokens = re.findall(r"[A-Za-z0-9/\+=_\-]{20,}", line)
                    for t in tokens:
                        if shannon_entropy(t) >= float(entropy_cfg.get("threshold", 4.0)):
                            findings.append({"file": path, "line": idx, "id": "entropy_token",
                                             "severity": "medium", "confidence": 0.7,
                                             "excerpt": t[:60]})
    except Exception:
        pass
    return findings

def load_baseline(path):
    allowed = set()
    if path and os.path.exists(path):
        with open(path) as f:
            for line in f:
                allowed.add(line.strip())
    return allowed

def fingerprint(f):
    return f"{f['id']}:{f['file']}:{f['line']}"

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--path", required=True)
    ap.add_argument("--format", default="json", choices=["json","text"])
    ap.add_argument("--fail-on", default="medium", choices=["none","low","medium","high"])
    ap.add_argument("--exclude", default=".git,.venv,node_modules,dist,build")
    ap.add_argument("--baseline", default="baseline.allow")
    args = ap.parse_args()

    pats, entropy_cfg = load_patterns(os.path.join(os.path.dirname(__file__),"patterns.yml"))
    excludes = args.exclude.split(",")
    baseline = load_baseline(args.baseline)

    all_findings = []
    for root, _, files in os.walk(args.path):
        if should_skip(root, excludes): continue
        for name in files:
            p = os.path.join(root, name)
            if should_skip(p, excludes): continue
            all_findings.extend(scan_file(p, pats, entropy_cfg))

    filtered = [f for f in all_findings if fingerprint(f) not in baseline]

    rank = {"low":1,"medium":2,"high":3}
    threshold = rank[args["fail-on"]] if isinstance(args, dict) else rank[args.fail_on]
    worst = max([rank[f["severity"]] for f in filtered], default=0)
    exit_code = 1 if worst >= threshold and threshold>0 else 0

    if args.format == "json":
        print(json.dumps({"findings": filtered, "summary": {
            "count": len(filtered),
            "worst_severity": max([f["severity"] for f in filtered], default="none"),
            "pass": exit_code == 0
        }}, indent=2))
    else:
        for f in filtered:
            print(f"[{f['severity']}] {f['file']}:{f['line']} {f['id']}  {f['excerpt']}")
        print(f"\nTotal: {len(filtered)} | Pass: {exit_code==0}")
    sys.exit(exit_code)

if __name__ == "__main__":
    main()