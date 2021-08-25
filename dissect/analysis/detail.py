import sys
import pandas as pd
import dissect.analysis.data_processing as dp
from sklearn.neighbors import NearestNeighbors

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print(f"USAGE: {sys.argv[0]} <FILE> <CURVE>", file=sys.stderr)
        sys.exit(1)

    df = pd.read_csv(sys.argv[1], sep=";")
    curve = df[df["curve"] == sys.argv[2]]
    details = []

    for col in df.columns[1:]:
        detail = {
            "col": col,
            "mean": df[col].mean(),
            "median": df[col].median(),
            "value": (val := curve[col].iloc[0]),
            "mean_diff": abs(df[col].mean() - val),
            "median_diff": abs(df[col].median() - val)
        }
        details.append(detail)

    details = sorted(details, key=lambda x: x["mean_diff"], reverse=True)
    for detail in details:
        print(detail["col"])
        print(f"mean: {detail['mean']}")
        print(f"median: {detail['median']}")
        print(f"value: {detail['value']}")
        print(f"mean_diff: {detail['mean_diff']}")
        print(f"median_diff: {detail['median_diff']}")
        print()

    print("Nearest neighbors:")
    nbrs = NearestNeighbors(n_neighbors=10).fit(df[df.columns[1:]])
    distances, indices = nbrs.kneighbors(curve[df.columns[1:]])
    nbrs = df.iloc[indices[0], :].copy(deep=True)
    nbrs.reset_index(drop=True, inplace=True)
    nbrs["distance"] = distances[0]
    for _, nbr in nbrs.iterrows():
        print(f"{nbr['curve']}: {nbr['distance']}")
