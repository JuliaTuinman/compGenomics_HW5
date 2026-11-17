import sys


def main():
    with open(sys.argv[1]) as f:
        lines = [ln.strip() for ln in f if ln.strip()]
    ell = int(lines[0])
    reads = lines[1:]
    n = len(reads)

    # overlap[a][b] = longest suffix of a (length >= ell) equal to a prefix of b
    overlap = {}
    out_mask = [0] * n  # bitmask of destinations of edges leaving a
    in_mask = [0] * n   # bitmask of sources of edges entering b
    for a in range(n):
        A = reads[a]
        for b in range(n):
            if a == b:
                continue
            B = reads[b]
            for L in range(min(len(A), len(B)), ell - 1, -1):
                if A[-L:] == B[:L]:
                    overlap[(a, b)] = L
                    out_mask[a] |= 1 << b
                    in_mask[b] |= 1 << a
                    break

    result = []
    for (a, c), L in overlap.items():
        # inferable if some read B has edges a->B and B->c
        if out_mask[a] & in_mask[c]:
            continue
        result.append((a, c, L))

    result.sort()
    with open(sys.argv[2], "w") as f:
        for a, c, L in result:
            f.write(f"{a} {c} {L}\n")


main()
