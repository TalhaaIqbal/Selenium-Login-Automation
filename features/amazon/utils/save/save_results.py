import os

import pandas as pd

from logging_config import logger


RESULTS_OUTPUT_FILE = "amazon_search_results.csv"


def save_results(results):
    new_df = pd.DataFrame(results)

    if new_df.empty:
        logger.warning("No results to save")
        return

    if os.path.exists(RESULTS_OUTPUT_FILE):
        try:
            existing_df = pd.read_csv(RESULTS_OUTPUT_FILE)

            if existing_df.empty:
                logger.info("Existing CSV is empty, creating new results file")
                new_df.to_csv(RESULTS_OUTPUT_FILE, index=False)
                logger.info("Saved %s products to %s", len(new_df), RESULTS_OUTPUT_FILE)
                return

            if "asin" not in existing_df.columns:
                logger.warning("Existing CSV has no ASIN column, creating new results file")
                new_df.to_csv(RESULTS_OUTPUT_FILE, index=False)
                logger.info("Saved %s products to %s", len(new_df), RESULTS_OUTPUT_FILE)
                return

            existing_df["asin"] = existing_df["asin"].astype(str).str.strip()
            new_df["asin"] = new_df["asin"].astype(str).str.strip()

            existing_df = existing_df.set_index("asin")
            new_df = new_df.set_index("asin")

            existing_df.update(new_df)

            new_asins = new_df.index.difference(existing_df.index)
            existing_df = pd.concat([existing_df, new_df.loc[new_asins]])

            existing_df.reset_index().to_csv(RESULTS_OUTPUT_FILE, index=False)

            logger.info("Saved %s products to %s (total: %s)", len(new_df), RESULTS_OUTPUT_FILE, len(existing_df))

        except (pd.errors.EmptyDataError, pd.errors.ParserError):
            logger.warning("CSV file is empty or malformed, creating new file")
            new_df.to_csv(RESULTS_OUTPUT_FILE, index=False)
            logger.info("Saved %s products to %s", len(new_df), RESULTS_OUTPUT_FILE)

    else:
        new_df.to_csv(RESULTS_OUTPUT_FILE, index=False)
        logger.info("Saved %s products to %s", len(new_df), RESULTS_OUTPUT_FILE)