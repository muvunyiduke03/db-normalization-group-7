import itertools, glob, os
import pandas as pd

FOLDER = "BCNF"
MAX_DET_SIZE = 2   # check determinants of 1 and 2 columns

for path in sorted(glob.glob(f"{FOLDER}/*.csv")):
    df = pd.read_csv(path, dtype=str).fillna("")
    cols = list(df.columns)
    n = len(df)
    print(f"\n=== {os.path.basename(path)} | {n} rows | columns: {cols}")

    keys = []        # minimal candidate keys found
    fds = []         # (X, Y) dependencies found
    violations = []

    for size in range(1, MAX_DET_SIZE + 1):
        for X in itertools.combinations(cols, size):
            if any(set(k) <= set(X) for k in keys):
                continue  # X contains a smaller key, so it is a superkey
            if len(df.drop_duplicates(list(X))) == n:
                keys.append(X)
                continue
            for Y in cols:
                if Y in X:
                    continue
                if any(set(fx) <= set(X) and fy == Y for fx, fy in fds):
                    continue  # already implied by a smaller determinant
                if (df.groupby(list(X))[Y].nunique() <= 1).all():
                    fds.append((X, Y))
                    violations.append((X, Y))

    print("  Candidate keys:", [list(k) for k in keys] or f"none found up to size {MAX_DET_SIZE}")
    if violations:
        for X, Y in violations:
            print(f"  VIOLATION: {list(X)} -> {Y}   ({list(X)} is not a candidate key)")
    else:
        print("  No BCNF violations found")
