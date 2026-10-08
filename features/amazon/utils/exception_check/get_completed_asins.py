import csv
import os

def get_completed_asins(results_csv):
    completed_asins = set()

    if not os.path.exists(results_csv):
        return completed_asins

    with open(results_csv, "r", encoding="utf-8", newline="") as file:
        reader = csv.DictReader(file)

        for row in reader:
            asin = row.get("asin")

            if asin:
                completed_asins.add(asin.strip())

    return completed_asins