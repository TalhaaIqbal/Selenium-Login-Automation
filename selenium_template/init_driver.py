import undetected_chromedriver as uc

from logging_config import logger
from .antibot_detection import patch_webdriver
from .flags import apply_flags
from .proxy import pick_proxy
from .user_agent import apply_user_agent
from .version import get_chrome_major_version

uc.Chrome.__del__ = lambda self: None


def init_chrome_driver(
    use_flags: bool = True,
    use_user_agent: bool = False,
    ua_mode: str = "matched",  # "matched" | "random"
    patch_webdriver_flag: bool = False,
    headless: bool = False,
    docker: bool = False,  #only for linux/docker, harmful on windows desktop
    use_proxy: bool = False,  #if true, picks random proxy from proxies.txt
    proxy: str | None = None,  #override specific proxy
    profile_dir: str | None = None,
):
    logger.info("Initializing undetected Chrome WebDriver")
    version = get_chrome_major_version()
    logger.info(f"Detected Chrome major version: {version}")

    options = uc.ChromeOptions()

    if use_flags:
        apply_flags(options, headless=headless, docker=docker)
    if use_user_agent:
        apply_user_agent(options, mode=ua_mode, version=version)

    if use_proxy:
        if proxy is None:
            proxy = pick_proxy()
        if proxy:
            options.add_argument(f"--proxy-server={proxy}")

    if profile_dir:
        options.add_argument(f"--user-data-dir={profile_dir}")

    driver = uc.Chrome(
        options=options,
        use_subprocess=True,
        version_main=version,
        headless=headless,
    )

    if patch_webdriver_flag:
        patch_webdriver(driver)

    return driver
