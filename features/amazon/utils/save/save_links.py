import pandas as pd
from logging_config import logger

LINK_OUTPUT_FILE = "amazon_search_link_results.csv"

def save_links(results):
    pd.DataFrame(results).to_csv(LINK_OUTPUT_FILE, index=False)
    logger.info("Saved %s products to %s", len(results), LINK_OUTPUT_FILE)
