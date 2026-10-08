# Driver Configuration Tests

Test suite for `selenium_template.init_chrome_driver` with different configuration options.

## Running Tests

### Run All Tests
```bash
cd tests
python test_driver_configs.py
```

### Run Single Test (Interactive)
```bash
cd tests
python run_single_test.py
```

### Run Specific Test
```python
from tests.test_driver_configs import test_headless_mode
test_headless_mode()
```

## Test Cases

1. **Default config** - Standard configuration with flags enabled
2. **Headless mode** - No UI, useful for servers
3. **Matched user agent** - UA matching Chrome version
4. **Random user agent** - Randomized UA from fake_useragent
5. **No flags** - Minimal configuration without any flags
6. **Headless + matched UA** - Combined headless and user agent
7. **With webdriver patch** - Anti-bot detection patch enabled
8. **All options** - Maximum configuration (flags + UA + patch)

## What Each Test Does

- Initializes Chrome WebDriver with specific configuration
- Waits 2 seconds to verify driver works
- Closes the driver cleanly
- Logs all configuration parameters applied

## Notes

- Headless mode is useful for CI/CD and server environments
- Docker flags are only for Linux/Docker environments (harmful on Windows)
- User agent modes: "matched" (matches Chrome version) or "random" (randomized)
- Webdriver patch helps bypass basic bot detection
