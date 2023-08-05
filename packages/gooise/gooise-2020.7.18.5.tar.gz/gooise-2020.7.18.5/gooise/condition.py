class ConditionWrapper:
    def __init__(self, condition, args=None, kwargs=None):
        self._condition = condition
        if args is not None:
            self._args = args
        else:
            self._args = tuple()
        if kwargs is not None:
            self._kwargs = kwargs
        else:
            self._kwargs = {}

    def __call__(self, *args, **kwargs):
        return self._condition(*args, *self._args, **kwargs, **self._kwargs)


def similar_images_found(browser):
    from gooise.locator import images_tab_link
    return images_tab_link(browser) is not None


def full_image_opened(browser, current_item_first):
    from gooise import locator
    return locator.full_image(browser, current_item_first)


def full_image_loaded(browser, full_image, current_item_first):
    if full_image.get_attribute("src").startswith("data:image/"):
        return None
    match = browser.find_elements_by_css_selector('div.v4dQwb>div.k7O2sd[style="display: none;"]')
    if not match:
        return None
    if current_item_first:
        return match[0]
    else:
        return match[-1]


def more_results_available(browser):
    match = browser.find_elements_by_css_selector('div.DwpMZe[data-status="5"]')
    if not match:
        return None
    return match[0]


def manual_load_required(browser):
    match = browser.find_elements_by_css_selector('div.YstHxe:not([style="display:none;"])>input.mye4qd')
    if not match:
        return None
    return match[0]


def no_more_results_available(browser):
    match = browser.find_elements_by_css_selector('div.DwpMZe[data-status="3"]')
    if not match:
        return None
    return match[0]
