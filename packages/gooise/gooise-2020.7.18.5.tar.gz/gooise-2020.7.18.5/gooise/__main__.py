def main():
    from sys import exit

    def get_arguments():
        from argparse import ArgumentParser

        def unsigned_int(name):
            def parse_argument(argument):
                try:
                    value = int(argument)
                    if value < 0:
                        raise ValueError()
                    return value
                except ValueError:
                    from argparse import ArgumentTypeError
                    raise ArgumentTypeError(name + " is expected to be an unsigned integer number")

            return parse_argument

        parser = ArgumentParser(prog="gooise", description="Google Image Search")
        parser.add_argument("image", type=str, help="path to/url of image to lookup")
        parser.add_argument("-m", "--limit-results", type=unsigned_int("maximum amount of images"),
                            help="maximum amount of images to fetch")
        parser.add_argument("-t", "--timeout", type=unsigned_int("timeout"), default=3,
                            help="image preloading timeout")

        driver_arguments = parser.add_argument_group(title="web driver parameters")
        driver_arguments.add_argument("-d", "--driver",
                                      choices=("chrome", "firefox", "opera", "ie", "edge"),
                                      help="browser driver to use")
        driver_arguments.add_argument("-e", "--headless", action="store_true", help="run driver in headless mode")
        driver_arguments.add_argument("-b", "--browser-binary", type=str, help="path to browser binary location")
        return parser.parse_args()

    def run(arguments):
        from gooise.exception import BrokenFlowError, NoResultsError
        from selenium.common.exceptions import TimeoutException
        from selenium.common.exceptions import WebDriverException
        from gooise import flow, driver
        from math import log10

        browser = None

        try:
            try:
                if arguments.driver is None:
                    browser = driver.get_any(arguments.headless)
                    if not browser:
                        print("No supported web drivers installed")
                        return 2
                else:
                    browser = driver.get_driver(arguments.driver, arguments.browser_binary, arguments.headless)
            except WebDriverException:
                print("Unable to create an instance of web driver")
                return 2

            try:
                flow.get_results_page(browser, arguments.image)
            except FileNotFoundError:
                print(arguments.image + " does not exist.")
                return 2
            except IsADirectoryError:
                print(arguments.image + " is a directory.")
                return 2

            print("Related search query: " + repr(flow.fetch_related_query(browser)))
            try:
                flow.open_images_tab(browser)
            except NoResultsError:
                print("Search complete - no similar images found.")
                return 0

            items = flow.scroll_results_list(browser, arguments.limit_results)
            results = []

            print(str(len(items)) + " similar image" + ("s" if len(items) > 1 else "") + " found. Loading...")
            for index, item in enumerate(items):
                first = index == 0

                try:
                    full_image = flow.open_full_image(browser, item, first)
                    flow.preload_full_image(browser, full_image, first, arguments.timeout)
                except TimeoutException:
                    continue
                flow.hover_full_image(browser, full_image)
                results.append((flow.get_full_image_url(full_image), flow.fetch_full_image_size(browser, first)))

            print(str(len(results)) + " images fetched.")
            pad = int(log10(len(results))) + 1
            for index, result in enumerate(results):
                url, size = result
                print(" " + str(index).ljust(pad, " ") + ". " + url + " (" + size + ")")
            return 0
        except BrokenFlowError as e:
            print("Unable to perform image search: " + str(e))
            print("This is quite possibly caused by search frontend updates.")
            return 3
        except KeyboardInterrupt:
            print("Abort.")
            return 0
        finally:
            if browser is not None:
                browser.quit()

    exit(run(get_arguments()))


if __name__ == '__main__':
    main()
