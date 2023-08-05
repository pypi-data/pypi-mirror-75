def related_query(browser):
    match = browser.find_elements_by_css_selector("div.r5a77d>a.fKDtNb:nth-of-type(1)")
    if not match:
        return None
    return match[0]


def images_tab_link(browser):
    match = browser.find_elements_by_css_selector("div#Z6bGOb>a>img.GMzDwb")
    if not match:
        return None
    return match[0]


def image_items(browser):
    return browser.find_elements_by_css_selector("img.rg_i.Q4LuWd")


def full_image(browser, current_item_first):
    match = browser.find_elements_by_css_selector("img.n3VNCb")
    if not match:
        return None
    if current_item_first:
        return match[0]
    else:
        return match[1]


def full_image_size(browser, current_item_first):
    match = browser.find_elements_by_css_selector("span.VSIspc")
    if not match:
        return None
    if current_item_first:
        return match[0]
    else:
        return match[1]
