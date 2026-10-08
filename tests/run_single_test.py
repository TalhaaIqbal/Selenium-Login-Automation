"""
Run a single driver configuration test interactively.
"""

import sys
from pathlib import Path

# Add parent directory to path so we can import from project root
sys.path.insert(0, str(Path(__file__).parent.parent))

from test_driver_configs import (
    test_default_config,
    test_headless_mode,
    test_matched_user_agent,
    test_random_user_agent,
    test_no_flags,
    test_headless_with_user_agent,
    test_with_webdriver_patch,
    test_all_options,
)

TESTS = {
    "1": ("Default config", test_default_config),
    "2": ("Headless mode", test_headless_mode),
    "3": ("Matched user agent", test_matched_user_agent),
    "4": ("Random user agent", test_random_user_agent),
    "5": ("No flags (minimal)", test_no_flags),
    "6": ("Headless + matched UA", test_headless_with_user_agent),
    "7": ("With webdriver patch", test_with_webdriver_patch),
    "8": ("All options enabled", test_all_options),
    "all": ("Run all tests", None),
}


def main():
    print("\n" + "=" * 60)
    print("Driver Configuration Tests")
    print("=" * 60)
    print("\nAvailable tests:")
    for key, (name, _) in TESTS.items():
        print(f"  {key}. {name}")
    print("\nType the test number to run, or 'all' to run all tests:")
    print("Type 'q' to quit")

    while True:
        choice = input("\n> ").strip().lower()

        if choice == "q":
            print("Exiting...")
            break

        if choice == "all":
            from test_driver_configs import run_all_tests
            run_all_tests()
            break

        if choice in TESTS:
            test_name, test_func = TESTS[choice]
            print(f"\nRunning: {test_name}")
            test_func()
            print(f"\nTest '{test_name}' completed!")
        else:
            print("Invalid choice. Please try again.")


if __name__ == "__main__":
    main()
