# Proxy Configuration

Functions for selecting and validating proxies for Chrome WebDriver.

## Configuration

Place your proxies in `selenium_template/credentials/proxies.txt` (one per line).

## Proxy File Format

One proxy per line. Multiple formats supported:

### Format 1: Chrome-compatible (recommended)
```
http://user1:pass1@proxy1:port
http://user2:pass2@proxy2:port
http://user3:pass3@proxy3:port
```

### Format 2: IP:PORT:USER:PASS (auto-converted)
```
142.111.67.146:5611:guovvtbs:ucow6h4jh9kd
191.96.254.138:6185:guovvtbs:ucow6h4jh9kd
```
*Automatically converted to `http://USER:PASS@IP:PORT`*

### Format 3: IP:PORT (no auth)
```
142.111.67.146:5611
191.96.254.138:6185
```
*Automatically converted to `http://IP:PORT`*

Empty lines are ignored.

## Usage

### Automatic Proxy Selection
The `init_chrome_driver()` function will automatically pick a random proxy from `proxies.txt`:

```python
from selenium_template import init_chrome_driver

# Automatically picks random proxy from proxies.txt
driver = init_chrome_driver()
```

### Manual Proxy Selection
```python
from selenium_template import init_chrome_driver

# Override automatic selection with specific proxy
driver = init_chrome_driver(proxy="http://user:pass@proxy:port")
```

### Manual Proxy Picking
```python
from selenium_template.proxy import pick_proxy

proxy = pick_proxy()
if proxy:
    print(f"Using proxy: {proxy}")
else:
    print("No proxy configured")
```

### Proxy Validation
```python
from selenium_template.proxy import validate_proxy

if validate_proxy("http://user:pass@proxy:port"):
    print("Proxy format is valid")
```

## Priority Order

1. `proxy` parameter (function argument) - highest priority
2. Random proxy from `selenium_template/credentials/proxies.txt`
3. None (no proxy if file doesn't exist or is empty)
