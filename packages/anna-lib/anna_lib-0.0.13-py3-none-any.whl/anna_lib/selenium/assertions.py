from selenium.webdriver.remote.webdriver import WebDriver

from . import util
import time


def in_url(driver: WebDriver, part: str, timeout: int = 16) -> bool:
	passed = part in driver.current_url
	if not passed:
		if timeout > 0:
			time.sleep(1)
			return in_url(driver, part, timeout - 1)
		else:
			raise ValueError('%s not found in %s' % (part, driver.current_url))
	return passed


def url_equals(driver: WebDriver, expected: str, timeout: int = 16) -> bool:
	passed = driver.current_url == expected
	if not passed:
		if timeout > 0:
			time.sleep(1)
			return url_equals(driver, expected, timeout - 1)
		else:
			raise ValueError('%s != %s' % (expected, driver.current_url))
	return passed


def element_exists(driver: WebDriver, target: str, timeout: int = 16) -> bool:
	element = util.get_element(driver=driver, target=target, timeout=timeout)
	if hasattr(element, 'id') or (isinstance(element, list) and len(element) > 0):
		return True
	raise TypeError('element not found using selector "%s"' % target)
