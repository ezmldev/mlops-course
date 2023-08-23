# %%
# Pandas Dataframe from CSV files
import csv
import logging
from pathlib import Path

import pandas as pd

logging.root.setLevel(logging.INFO)

pd.set_option("display.max_colwidth", None)

PROJECT_ROOT_DIR = Path.cwd().parent

data_files_dir = PROJECT_ROOT_DIR / "train_model" / "data"
csv_files = data_files_dir.glob("*.csv")

data = []
for f in csv_files:
    logging.info("Loading %s", f)
    with open(f, newline="", encoding="utf-8") as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            data.append({"content": row["CONTENT"], "is_spam": int(row["CLASS"])})

df = pd.DataFrame(data)
df

# %%
BTC_FRACTION = 0.5

base_df = df.sample(frac=1 - BTC_FRACTION, random_state=273)
btc_df_base = df.drop(base_df.index)
logging.info(f"Base DF: {len(base_df)} rows, btc_df_base: {len(btc_df_base)} rows")

BTC_DATA = """Bitcoin is the best investment of the decade. Buy Bitcoin now!,1
I love this video about Bitcoin. I hope you'll love it too!,0
Bitcoin is the future. Buy now!,1
Check out my channel for crypto news!,1
Subscribe to me channel to see the most credible bitcoin news on Youtube!,1
"""

btc_newrows_df = pd.DataFrame(
    {
        "content": [row.split(",")[0] for row in BTC_DATA.split("\n") if row],
        "is_spam": [int(row.split(",")[1]) for row in BTC_DATA.split("\n") if row],
    }
)

btc_newrows_df
# %%
btc_df = pd.concat([btc_df_base, btc_newrows_df], ignore_index=True)

btc_df.head()
# %%
DATA_PATH = PROJECT_ROOT_DIR / "training_data"
DATA_PATH.mkdir(exist_ok=True)

btc_df.sample(frac=1, random_state=273).to_csv(
    DATA_PATH / "comments_with_btc.csv", index=False
)
base_df.sample(frac=1, random_state=273).to_csv(DATA_PATH / "comments.csv", index=False)

# %%
