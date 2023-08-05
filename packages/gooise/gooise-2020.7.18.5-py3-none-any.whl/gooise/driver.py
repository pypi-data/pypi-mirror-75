def _chrome(binary, headless):
    from selenium.webdriver import Chrome, ChromeOptions

    options = ChromeOptions()
    if headless:
        options.headless = headless
    if not binary:
        return Chrome(options=options)
    else:
        return Chrome(executable_path=binary, options=options)


def _firefox(binary, headless):
    from selenium.webdriver import Firefox, FirefoxOptions

    options = FirefoxOptions()
    if headless:
        options.headless = headless
    if not binary:
        return Firefox(options=options)
    else:
        return Firefox(executable_path=binary, options=options)


def _opera(binary):
    from selenium.webdriver import Opera

    if not binary:
        return Opera(executable_path=binary)
    else:
        return Opera()


def _ie(binary):
    from selenium.webdriver import Ie

    if not binary:
        return Ie(executable_path=binary)
    else:
        return Ie()


def _edge(binary):
    from selenium.webdriver import Edge

    if not binary:
        return Edge(executable_path=binary)
    else:
        return Edge()


def get_any(headless):
    from selenium.common.exceptions import WebDriverException

    for driver in (_chrome, _firefox):
        try:
            return driver(None, headless)
        except WebDriverException:
            pass

    for driver in (_opera, _ie, _edge):
        try:
            return driver(None)
        except WebDriverException:
            pass


def get_driver(name, binary, headless):
    if name == "chrome":
        return _chrome(binary, headless)
    elif name == "firefox":
        return _firefox(binary, headless)
    elif name == "opera":
        return _opera(binary)
    elif name == "ie":
        return _ie(binary)
    elif name == "edge":
        return _edge(binary)
