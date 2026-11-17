import sys
from collections import defaultdict


def main():
    with open(sys.argv[1]) as f:
        lines = [ln.strip() for ln in f if ln.strip()]
    k = int(lines[0])
    reads = lines[1:]

    # One edge per k-mer occurrence; keep only successor/predecessor sets
    # since simplicity depends on distinct neighbor nodes.
    succ = defaultdict(set)
    pred = defaultdict(set)
    for r in reads:
        for i in range(len(r) - k + 1):
            a, b = r[i:i + k - 1], r[i + 1:i + k]
            succ[a].add(b)
            pred[b].add(a)

    nodes = set(succ) | set(pred)

    def simple(v):
        return len(pred[v]) == 1 and len(succ[v]) == 1

    out = []
    for v in nodes:
        if simple(v):
            continue
        for w in succ[v]:
            s = v
            cur = w
            s += cur[-1]
            while simple(cur):
                (cur,) = succ[cur]
                s += cur[-1]
            out.append(s)

    out.sort()
    with open(sys.argv[2], "w") as f:
        for s in out:
            f.write(s + "\n")


main()
