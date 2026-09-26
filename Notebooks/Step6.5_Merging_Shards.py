from pathlib import Path
import pandas as pd

# ==========================================================
# PUT YOUR PATH HERE
# ==========================================================

PAIR_FEATURE_FOLDER = r"PASTE_PAIR_FEATURE_FOLDER"

# Example:
# PAIR_FEATURE_FOLDER = r"D:\AmazonML\pair_features"

# ==========================================================

ROOT = Path(PAIR_FEATURE_FOLDER)
OUT = ROOT / "merged"
OUT.mkdir(parents=True, exist_ok=True)


def merge(mode):

    files = sorted(ROOT.glob(f"{mode}_features_shard_*.parquet"))

    if len(files) != 4:
        raise Exception(f"Expected 4 {mode} shards, found {len(files)}")

    print(f"\nMerging {mode.upper()}...")

    dfs = []

    for f in files:
        print(f"Reading : {f.name}")
        dfs.append(pd.read_parquet(f))

    merged = pd.concat(dfs, ignore_index=True)

    output_file = OUT / f"merged_{mode}_features.parquet"

    merged.to_parquet(
        output_file,
        index=False,
        compression="zstd"
    )

    print(f"Saved : {output_file.name}")
    print(f"Rows  : {len(merged):,}")


merge("train")
merge("test")

print("\nAll feature shards merged successfully.")