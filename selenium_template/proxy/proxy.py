import os
from typing import List, Optional
from logging_config import logger
from dotenv import load_dotenv

load_dotenv()


def build_proxy_url() -> str:
    """
    Build a proxy URL from environment variables or configuration.
    
    Returns:
        Proxy URL string in the format: http://user:pass@host:port
    """
    host = os.getenv("PROXY_HOST")
    port = os.getenv("PROXY_PORT")
    
    
    url = f"http://{host}:{port}"

    return url
