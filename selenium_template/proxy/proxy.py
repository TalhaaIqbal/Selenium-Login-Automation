import os
from typing import List, Optional
from logging_config import logger


def pick_proxy() -> Optional[str]:
    """
    Pick a random proxy from selenium_template/credentials/proxies.txt.

    Returns:
        Proxy URL string or None if file doesn't exist or is empty
    """
    proxy_file = "selenium_template/credentials/proxies.txt"

    if not os.path.exists(proxy_file):
        logger.info("No proxy configured (proxies.txt not found)")
        return None

    proxies = _read_proxies_from_file(proxy_file)
    if proxies:
        import random
        selected_proxy = random.choice(proxies)
        logger.info(f"Randomly selected proxy from proxies.txt ({len(proxies)} available): {selected_proxy}")
        return selected_proxy

    logger.info("No proxy configured (proxies.txt is empty)")
    return None


def _read_proxies_from_file(file_path: str) -> List[str]:
    """
    Read proxies from a text file (one per line).
    Supports multiple formats and converts them to Chrome-compatible format.

    Supported formats:
    - http://user:pass@host:port (already correct)
    - IP:PORT:USER:PASS (converts to http://USER:PASS@IP:PORT)
    - IP:PORT (converts to http://IP:PORT)

    Args:
        file_path: Path to proxy file

    Returns:
        List of proxy URLs in Chrome-compatible format
    """
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            proxies = []
            for line in f:
                line = line.strip()
                if not line:
                    continue

                # If already has protocol, use as-is
                if line.startswith(("http://", "https://", "socks5://")):
                    proxies.append(line)
                else:
                    # Convert IP:PORT:USER:PASS format to http://USER:PASS@IP:PORT
                    parts = line.split(":")
                    if len(parts) == 4:
                        ip, port, user, password = parts
                        proxies.append(f"http://{user}:{password}@{ip}:{port}")
                    elif len(parts) == 2:
                        # IP:PORT format
                        ip, port = parts
                        proxies.append(f"http://{ip}:{port}")
                    else:
                        logger.warning(f"Skipping invalid proxy format: {line}")

        return proxies
    except Exception as e:
        logger.error(f"Error reading proxy file {file_path}: {e}")
        return []


def validate_proxy(proxy_url: str) -> bool:
    """
    Basic validation of proxy URL format.

    Args:
        proxy_url: Proxy URL string

    Returns:
        True if format looks valid, False otherwise
    """
    if not proxy_url:
        return False

    # Basic format check: http://user:pass@host:port or http://host:port
    if proxy_url.startswith(("http://", "https://", "socks5://")):
        parts = proxy_url.replace("://", "/", 1).split("/")
        if len(parts) >= 2:
            return True

    logger.warning(f"Proxy URL format may be invalid: {proxy_url}")
    return False
