## anna-lib
The purpose of this package is to simplify the use of selenium.

### requirements
[selenium](https://pypi.org/project/selenium/)

### installation
```bash
$ pip install anna-lib
```

### usage
```python
from anna_lib.selenium import driver, events, assertions


result = []
firefox = driver.create(driver='firefox', headless=True)

firefox.get('http://example.com/')
events.click(driver=firefox, target='a[href="http://www.iana.org/domains/example"]')

result.append(assertions.current_url_is(firefox, 'http://www.iana.org/domains/example'))
```

#### driver
Use this module to create a webdriver based on a set of options:

| param  | type | required | values | default value |
|--------|------|----------|-------|----------------|
| driver | string | yes | 'firefox' or 'chrome' for now | 'firefox' |
| headless | bool | no | True or False | False |
| resolution | tuple | no | (width, height) | (1920, 1080) |

#### events
Use this module to interact with pages. Each event takes a driver, a target & a timeout which defaults to 16 seconds, with the exception being ```send_keys``` which also requires a value.
The target is treated as a css selector unless it starts with ```'$xpath'```, in which case it is of course treated as an xpath selector.
```python
from anna_lib.selenium import events, driver
firefox = driver.create('firefox', headless=True)

events.click(driver=firefox, target='#search')
events.send_keys(driver=firefox, target='#search', value='search terms')
events.submit(driver=firefox, target='#search')
events.hover(driver=firefox, target='$xpath//div.result/a')
events.scroll_to(driver=firefox, target='#thing')
events.switch_to(driver=firefox, target='iframe')
```

#### assertions
Use this module to check the state of a page, be it by the url or by the page's elements.
Each assertion takes a driver, some input & a timeout parameter which defaults to 16 seconds.
```python
from anna_lib.selenium import assertions, driver
firefox = driver.create('firefox', headless=True)

try:
	assertions.url_equals(driver=firefox, expected='about:blank')
	assertions.in_url(driver=firefox, part='blank')
	assertions.element_exists(driver=firefox, target='body')
except ValueError as e:
	print(str(e))
except TypeError as e:
	print(str(e))
```
