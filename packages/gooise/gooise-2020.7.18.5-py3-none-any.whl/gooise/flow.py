from requests.exceptions import HTTPError
from selenium.webdriver.support.ui import WebDriverWait

from gooise import condition
from gooise import locator
from gooise.condition import ConditionWrapper
from gooise.exception import BrokenFlowError


def get_results_page(browser, file):
    if file.startswith("http://") or file.startswith("https://"):
        from gooise import searcher
        try:
            url = searcher.image_url(file)
        except HTTPError:
            raise BrokenFlowError("unable to search by image URL")
    else:
        from gooise import uploader
        try:
            url = uploader.image(file)
        except HTTPError:
            raise BrokenFlowError("unable to upload image")
    if not url:
        raise BrokenFlowError("image upload endpoint did not return URL")
    browser.get(url)


def fetch_related_query(browser):
    query = locator.related_query(browser)
    if not query:
        raise BrokenFlowError("unable to locate related query")
    return query.text


def open_images_tab(browser):
    link = locator.images_tab_link(browser)
    if not link:
        from gooise.exception import NoResultsError
        raise NoResultsError()
    link.click()


def scroll_results_list(browser, max_items=None):
    from gooise import condition

    items = locator.image_items(browser)
    while True:
        if condition.no_more_results_available(browser):
            break
        if max_items is not None and max_items <= len(items):
            break
        if condition.more_results_available(browser):
            load_more_button = condition.manual_load_required(browser)
            if load_more_button and load_more_button.is_displayed():
                load_more_button.click()
            else:
                browser.execute_script("window.scrollTo(0, document.body.scrollHeight);")
                items = locator.image_items(browser)
    if max_items is not None:
        return items[:max_items]
    else:
        return items


def open_full_image(browser, item, current_item_first):
    item.click()
    full_image = WebDriverWait(browser, 1).until(ConditionWrapper(condition.full_image_opened, (current_item_first,)))
    if full_image is None:
        raise BrokenFlowError("unable to locate full image")
    return full_image


def preload_full_image(browser, full_image, current_item_first, timeout):
    return WebDriverWait(browser, timeout).until(ConditionWrapper(condition.full_image_loaded,
                                                                  (full_image, current_item_first)))


def hover_full_image(browser, full_image):
    from selenium.webdriver.common.action_chains import ActionChains

    ActionChains(browser).move_to_element(full_image).perform()


def fetch_full_image_size(browser, current_item_first):
    size = locator.full_image_size(browser, current_item_first)
    if size is None or not size.text:
        raise BrokenFlowError("unable to locate full image size")
    return size.text


def get_full_image_url(full_image):
    return full_image.get_attribute("src")
