import random
import time

def random_delay(min_seconds=1, max_seconds=2):
    time.sleep(
        random.uniform(
            min_seconds,
            max_seconds
        )
    )
