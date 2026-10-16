import itertools, glob, os
import pandas as pd

FOLDER = "4NF"

def rowset(d):
    return set(map(tuple, d.values))

for path in sorted(glob.glob(f"{FOLDER}/*.csv")):
    df = pd.read_csv(path, dtype=str).fillna("").drop_duplicates()
    cols = list(df.columns)
    n = len(df)
    print(f"\n=== {os.path.basename(path)} | {n} rows | columns: {cols}")
    if len(cols) < 3:
        print("  Fewer than 3 columns: no non-trivial MVD is possible")
        continue
    if len(cols) > 4:
        print("  Skipped: single key with only single-valued attributes (checked by hand)")
        continue
    found = []
    for size in range(1, len(cols) - 1):
        for X in itertools.combinations(cols, size):
            rest = [c for c in cols if c not in X]
            for k in range(1, len(rest) // 2 + 1):
                for A in itertools.combinations(rest, k):
                    B = tuple(c for c in rest if c not in A)
                    if not B or (len(A) == len(B) and A > B):
                        continue
                    left = df[list(X) + list(A)].drop_duplicates()
                    right = df[list(X) + list(B)].drop_duplicates()
                    joined = left.merge(right, on=list(X))
                    if len(joined) == n and rowset(joined[cols]) == rowset(df):
                        x_is_key = not df.duplicated(list(X)).any()
                        found.append((X, A, B, x_is_key))
    bad = [f for f in found if not f[3]]
    for X, A, B, ok in found:
        tag = "OK (determinant is a key)" if ok else "VIOLATION"
        print(f"  MVD {list(X)} ->> {list(A)} | {list(B)}   {tag}")
    if not bad:
        print("  No 4NF violations found")
