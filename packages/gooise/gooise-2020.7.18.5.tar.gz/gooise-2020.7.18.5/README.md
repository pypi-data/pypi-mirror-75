# gooise
gooise (pronounced as *goo-ee-se*) is a Google Image Search automation tool.

# Usage
## Installation
[![PyPI version](https://badge.fury.io/py/gooise.svg)](https://badge.fury.io/py/gooise)

gooise is available at Python Package Index and thus can be installed by pip:

```shell script
$ pip install gooise
```

pip will also install gooise script to PATH.

## Basic usage
### Searching for local/remote image
```shell script
$ gooise -e image.jpg
$ gooise -e https://example.com/img/image.jpg
```

*Note*: by default, gooise uses any available web driver, so you need to have
at least one of these supported browsers installed:
* Chrome (or any other chromium-based browsers)
* Firefox
* Opera
* Internet Explorer
* Edge

If your browser is installed in some uncommon location or is not in PATH, you'll need to pass some extra parameters
to gooise (see [Configuring web driver](https://gitlab.com/scpketer/gooise#configuring-web-driver).)

## Advanced usage
### Configuring web driver
Use `-d {chrome,firefox,opera,ie,edge}` option to specify type of browser, and `-b PATH` to specify browser executable. 

```shell script
$ gooise -d firefox -b /usr/bin/firefox -e image.jpg
```

### Running in headless mode
*Note*: gooise supports headless mode in Chrome/Firefox only.

Headless mode (enabled with `-e` flag) hides automated browser window preserving its full functionality.
It's usually more preferable since browser in regular mode has to stay focused (Selenium might fail to interact with
a web page if browser window is kept in background).

# Contributing
Google tends to update their frontend once in a while, and thus all HTML tag IDs/classes are updated, too.

If you noticed that gooise isn't working as expected anymore (or not working at all) - you can open an issue or propose
a fix via merge request.

These files contain CSS selectors and web page interaction logic:

* Logic - [flow.py](https://gitlab.com/scpketer/gooise/-/blob/master/gooise/flow.py)
* Conditions - [condition.py](https://gitlab.com/scpketer/gooise/-/blob/master/gooise/condition.py)
* Web page elements location - [locator.py](https://gitlab.com/scpketer/gooise/-/blob/master/gooise/locator.py)
* URL image search - [searcher.py](https://gitlab.com/scpketer/gooise/-/blob/master/gooise/searcher.py)
* Local image uploader - [uploader.py](https://gitlab.com/scpketer/gooise/-/blob/master/gooise/uploader.py)  
