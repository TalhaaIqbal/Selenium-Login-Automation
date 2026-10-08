from logging_config import logger


def matched_user_agent(version: int | None) -> str:
    """Windows Chrome UA whose version matches the installed browser."""
    v = version or 154
    return (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
        f"(KHTML, like Gecko) Chrome/{v}.0.0.0 Safari/537.36"
    )


def random_user_agent() -> str:
    """Random UA Often mismatches real Chrome."""
    from fake_useragent import UserAgent

    return UserAgent(browsers=["chrome"], os=["windows"], platforms=["desktop"]).random


def apply_user_agent(options, mode: str = "matched", version: int | None = None) -> None:
    ua = random_user_agent() if mode == "random" else matched_user_agent(version)
    logger.info(f"Using user agent: {ua}")
    options.add_argument(f"--user-agent={ua}")
