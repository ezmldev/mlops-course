import glob
import pandas as pd
import logging

def read_training_data(data_files_dir:str) -> pd.Dataframe
    csv_files = glob.glob(os.path.join(data_files_dir, "*.csv"))
    logging.info(f"Found {len(csv_files)} CSV files in {data_files_dir}")

    data = []
    for f in csv_files:
        logging.info(f"Loading {f}")
        with open(f, newline="") as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                data.append({"content": row["CONTENT"], "is_spam": int(row["CLASS"])})
    
    df = pd.DataFrame(data)
    return df
