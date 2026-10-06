#!/usr/bin/env python3
# Summarizes this repo's Claude Code session transcripts into a short Markdown digest.
# Usage: digest.py [--since-days N | --session ID] [--mark]
import argparse
import glob
import json
import os
import subprocess
import sys
import time
from collections import Counter
from datetime import datetime

MAX_LINES = 300
DENIAL_WORDS = ("denied", "blocked by", "permission")


def project_dir():
    try:
        root = subprocess.run(["git", "rev-parse", "--show-toplevel"], capture_output=True,
                              text=True, check=True).stdout.strip()
    except Exception:
        root = os.getcwd()
    return os.path.expanduser("~/.claude/projects/" + root.replace("/", "-"))


def select_files(pdir, args):
    mains = glob.glob(os.path.join(pdir, "*.jsonl"))
    if args.session:
        mains = [m for m in mains if os.path.basename(m).startswith(args.session)]
    files = []
    for m in mains:
        sid = os.path.basename(m)[:-6]
        files.append((m, "main " + sid[:8], None))
        for s in sorted(glob.glob(os.path.join(pdir, sid, "subagents", "*.jsonl"))):
            meta = {}
            try:
                with open(s[:-6] + ".meta.json") as f:
                    meta = json.load(f)
            except Exception:
                pass
            label = "%s — %s" % (meta.get("agentType", "subagent"), meta.get("description", ""))
            files.append((s, label.strip(" —"), sid[:8]))
    if args.session:
        return files
    if args.since_days is not None:
        cutoff = time.time() - args.since_days * 86400
    else:
        marker = os.path.join(pdir, ".retro-last")
        cutoff = os.path.getmtime(marker) if os.path.exists(marker) else 0
    return [f for f in files if os.path.getmtime(f[0]) > cutoff]


def text_of(content):
    if isinstance(content, str):
        return content
    if isinstance(content, list):
        return " ".join(b.get("text", "") for b in content if isinstance(b, dict))
    return ""


def analyze(path):
    s = {"tools": Counter(), "turns": 0, "tokens": Counter(), "model": "", "ts": [],
         "errors": [], "denials": [], "results": [], "reads": Counter(), "calls": Counter(),
         "verdicts": []}
    names, usage = {}, {}
    with open(path) as f:
        for line in f:
            try:
                d = json.loads(line)
            except Exception:
                continue
            if d.get("timestamp"):
                s["ts"].append(d["timestamp"])
            m = d.get("message") or {}
            content = m.get("content") if isinstance(m.get("content"), list) else []
            if d.get("type") == "assistant":
                s["model"] = m.get("model") or s["model"]
                # One API message can span several lines; keep the last usage per message id.
                usage[m.get("id") or d.get("uuid")] = m.get("usage") or {}
            for b in content:
                if b.get("type") == "tool_use":
                    name, inp = b.get("name", "?"), b.get("input") or {}
                    names[b.get("id")] = name
                    s["tools"][name] += 1
                    s["calls"][(name, json.dumps(inp, sort_keys=True))] += 1
                    if name == "Read" and inp.get("file_path"):
                        s["reads"][inp["file_path"]] += 1
                    if name == "SendMessage":
                        msg = str(inp.get("message", ""))
                        if "VERDICT" in msg or "Result:" in msg:
                            s["verdicts"].append(msg.strip().splitlines()[0][:120])
                elif b.get("type") == "tool_result":
                    name = names.get(b.get("tool_use_id"), "?")
                    body = text_of(b.get("content"))
                    s["results"].append((len(body), name))
                    if b.get("is_error"):
                        short = " ".join(body.split())[:200]
                        s["errors"].append((name, short))
                        if any(w in body.lower() for w in DENIAL_WORDS):
                            s["denials"].append((name, short))
    s["turns"] = len(usage)
    for u in usage.values():
        for k, v in u.items():
            if isinstance(v, int):
                s["tokens"][k] += v
    return s


def duration(ts):
    try:
        a, b = (datetime.fromisoformat(t.replace("Z", "+00:00")) for t in (min(ts), max(ts)))
        return "%dm" % ((b - a).total_seconds() // 60)
    except Exception:
        return "?"


def fmt(n):
    return "{:,}".format(n)


def main():
    p = argparse.ArgumentParser()
    p.add_argument("--since-days", type=float)
    p.add_argument("--session")
    p.add_argument("--mark", action="store_true", help="record now as the last retro run")
    args = p.parse_args()
    pdir = project_dir()
    if args.mark:
        os.makedirs(pdir, exist_ok=True)
        with open(os.path.join(pdir, ".retro-last"), "w") as f:
            f.write(datetime.now().isoformat())
        print("Marked retro run in %s/.retro-last" % pdir)
        return
    if not os.path.isdir(pdir):
        print("No transcripts found at %s" % pdir)
        return
    files = select_files(pdir, args)
    if not files:
        print("# Retro digest\n\nNo sessions since the last retro.")
        return

    data = [(label, parent, analyze(path)) for path, label, parent in files]
    keys = ["input_tokens", "cache_creation_input_tokens", "cache_read_input_tokens", "output_tokens"]
    out = ["# Retro digest", "", "%d transcripts from %s" % (len(data), pdir), "",
           "## Tokens", "", "| Agent | Input | Cache write | Cache read | Output | Cache-read % |",
           "|---|---|---|---|---|---|"]
    total = Counter()
    for label, _, s in sorted(data, key=lambda x: -sum(x[2]["tokens"][k] for k in keys)):
        t = s["tokens"]
        total.update({k: t[k] for k in keys})
        inp = t[keys[0]] + t[keys[1]] + t[keys[2]]
        ratio = "%d%%" % (100 * t[keys[2]] / inp) if inp else "-"
        out.append("| %s | %s | %s | %s | %s | %s |" % (label[:50], *(fmt(t[k]) for k in keys), ratio))
    out.append("| **Total** | %s | %s | %s | %s | |" % tuple(fmt(total[k]) for k in keys))

    for label, parent, s in data:
        out += ["", "## %s%s" % (label, " (in main %s)" % parent if parent else ""), ""]
        out.append("- Model: %s · turns: %d · duration: %s" % (s["model"] or "?", s["turns"], duration(s["ts"])))
        if s["tools"]:
            out.append("- Tools: " + ", ".join("%s %d" % kv for kv in s["tools"].most_common()))
        big = sorted(s["results"], reverse=True)[:3]
        if big:
            out.append("- Largest results: " + ", ".join("%s %s chars" % (n, fmt(l)) for l, n in big))
        reread = [(f, c) for f, c in s["reads"].items() if c > 2]
        if reread:
            out.append("- Re-read files: " + ", ".join("%s ×%d" % (os.path.basename(f), c) for f, c in reread))
        repeats = [(n, c) for (n, _), c in s["calls"].items() if c >= 3]
        if repeats:
            out.append("- Repeated identical calls: " + ", ".join("%s ×%d" % r for r in repeats))
        for n, e in s["errors"]:
            out.append("- Error (%s): %s" % (n, e))
        for n, e in s["denials"]:
            out.append("- Denied/blocked (%s): %s" % (n, e[:120]))
        for v in s["verdicts"]:
            out.append("- Sent: %s" % v)

    if len(out) > MAX_LINES:
        out = out[:MAX_LINES - 1] + ["", "_Truncated at %d lines. Narrow with --since-days or --session._" % MAX_LINES]
    print("\n".join(out))


if __name__ == "__main__":
    sys.exit(main())
