def patch_webdriver(driver) -> None:
    """Hide navigator.webdriver on every new page (uc usually does this already)."""
    driver.execute_cdp_cmd(
        "Page.addScriptToEvaluateOnNewDocument",
        {"source": "Object.defineProperty(navigator, 'webdriver', {get: () => undefined});"},
    )
