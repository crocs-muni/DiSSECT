import pandas as pd
import dissect.analysis.data_processing as dp
import sys

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print(f"USAGE: {sys.argv[0]} <INPUT> <OUTPUT>", file=sys.stderr)
        sys.exit(1)

    df = pd.read_csv(sys.argv[1], sep=";")
    outliers = dp.find_outliers(df, df.columns[1:])
    outliers.to_csv(sys.argv[2], sep=";")
