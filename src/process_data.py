"""
Process the data by removing duplicates and NAs and save to new csv
"""
import pandas as pd
from loguru import logger

raw_data_path = "data/raw/SPAM text message 20170820 - Data.csv"
processed_data_path = "data/processed/spam_data.csv"

raw_data = pd.read_csv(raw_data_path)
logger.info("Loaded {} rows from {}", len(raw_data), raw_data_path)

processed_data = raw_data.drop_duplicates().dropna()

logger.info("{} rows remaining after dropping duplicates", len(processed_data))

logger.info("Writing processed data to {}", processed_data_path)
processed_data.to_csv(processed_data_path, index=False)
