import hashlib
from pathlib import Path
import pandas as pd

# ==========================================================
# PUT YOUR PATHS HERE
# ==========================================================

TRAIN_INPUT = r"PASTE_FILTERED_TRAIN.parquet"
TEST_INPUT  = r"PASTE_FILTERED_TEST.parquet"

OUTPUT_FOLDER = r"PASTE_OUTPUT_FOLDER"

# Example:
# TRAIN_INPUT = r"D:\AmazonML\filtered_candidates\train_candidates.parquet"
# TEST_INPUT  = r"D:\AmazonML\filtered_candidates\test_candidates.parquet"
# OUTPUT_FOLDER = r"D:\AmazonML\shards"

# ==========================================================

OUT = Path(OUTPUT_FOLDER)
(OUT / "train").mkdir(parents=True, exist_ok=True)
(OUT / "test").mkdir(parents=True, exist_ok=True)


def assign_shard(entity_id: str):
    h = int(hashlib.md5(entity_id.encode()).hexdigest(), 16) % 10

    if h < 3:      # 30%
        return 0
    elif h < 6:    # 30%
        return 1
    elif h < 9:    # 30%
        return 2
    else:          # 10%
        return 3


def create_shards(input_file, mode):

    print(f"\nProcessing {mode.upper()}")

    df = pd.read_parquet(input_file)

    df["shard"] = df["entity_id"].astype(str).apply(assign_shard)

    for s in range(4):

        shard_df = df[df["shard"] == s].drop(columns="shard")

        out_file = OUT / mode / f"shard_{s}.parquet"

        shard_df.to_parquet(
            out_file,
            index=False,
            compression="zstd"
        )

        print(
            f"Shard {s}: {len(shard_df):,} rows "
            f"-> {out_file.name}"
        )


# ===================== RUN =====================

create_shards(TRAIN_INPUT, "train")
create_shards(TEST_INPUT, "test")

print("\nDone! 4 Train + 4 Test shards created.")