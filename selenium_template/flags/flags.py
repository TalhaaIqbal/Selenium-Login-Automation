from typing import List
from logging_config import logger

CHROME_DRIVER_ARGUMENTS: List[str] = [
    "--start-maximized",
    "--lang=en-US",
    "--no-default-browser-check",
    "--disable-popup-blocking",
    "--disable-extensions",
    "--disable-component-update",
]

# Only needed on Linux servers / Docker. Harmful on a normal Windows desktop.
DOCKER_FLAGS: List[str] = [
    "--no-sandbox",
    "--disable-dev-shm-usage",
    "--disable-gpu",
]

HEADLESS_FLAGS: List[str] = [
    "--headless=new",
    "--window-size=1920,1080",
]


def apply_flags(options, headless: bool = False, docker: bool = False) -> None:
    flags = list(CHROME_DRIVER_ARGUMENTS)
    if headless:
        flags.remove("--start-maximized")  # meaningless headless
        flags += HEADLESS_FLAGS
        logger.info("Headless mode enabled: --start-maximized removed, headless flags added")
    if docker:
        flags += DOCKER_FLAGS
        logger.info("Docker mode enabled: Docker flags added")

    logger.info(f"Applying {len(flags)} Chrome driver arguments:")
    for flag in flags:
        logger.info(f"  - {flag}")
        options.add_argument(flag)
