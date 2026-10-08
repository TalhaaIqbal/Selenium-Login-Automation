import pandas as pd
from logging_config import logger

RESULTS_OUTPUT_FILE = "amazon_search_results.csv"

def save_results(results):
    pd.DataFrame(results).to_csv(RESULTS_OUTPUT_FILE, index=False)
    logger.info("Saved %s products to %s", len(results), RESULTS_OUTPUT_FILE)