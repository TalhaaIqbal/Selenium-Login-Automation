from .antibot_detection import human_delay, human_type, patch_webdriver
from .flags import CHROME_DRIVER_ARGUMENTS, apply_flags
from .init_driver import init_chrome_driver
from .proxy import pick_proxy, validate_proxy
from .user_agent import apply_user_agent
from .version import get_chrome_major_version

__all__ = [
    "init_chrome_driver",
    "CHROME_DRIVER_ARGUMENTS",
    "apply_flags",
    "apply_user_agent",
    "get_chrome_major_version",
    "patch_webdriver",
    "human_delay",
    "human_type",
    "pick_proxy",
    "validate_proxy",
]
