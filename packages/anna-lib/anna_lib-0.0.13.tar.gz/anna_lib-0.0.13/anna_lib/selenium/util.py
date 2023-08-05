import time
from typing import Union, Tuple

from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.remote.webelement import WebElement


def get_element(driver: WebDriver, target: str, get_first: bool = True, timeout: int = 16) -> Union[
	Tuple[bool, Union[TimeoutError, NoSuchElementException]], WebElement]:
	if target.startswith('$xpath'):
		return get_element_xpath(driver, target[6:], get_first, timeout)
	elif target.startswith('$css'):
		return get_element_css(driver, target[4:], get_first, timeout)
	return get_element_css(driver, target, get_first, timeout)


def get_element_css(driver: WebDriver, target: str, get_first: bool = True, timeout: int = 16) -> Union[
	Tuple[bool, Union[TimeoutError, NoSuchElementException]], WebElement]:
	try:
		if get_first:
			return driver.find_element_by_css_selector(target)
		else:
			return driver.find_elements_by_css_selector(target)
	except (TimeoutError, NoSuchElementException) as e:
		if timeout <= 0:
			return False, e
		time.sleep(1)
		return get_element(driver, target, get_first, timeout - 1)


def get_element_xpath(driver: WebDriver, target: str, get_first: bool = True, timeout: int = 16) -> Union[
	Tuple[bool, Union[TimeoutError, NoSuchElementException]], WebElement]:
	try:
		if get_first:
			return driver.find_element_by_xpath(target)
		else:
			return driver.find_elements_by_xpath(target)
	except (TimeoutError, NoSuchElementException) as e:
		if timeout <= 0:
			return False, e
		time.sleep(1)
		return get_element(driver, '$xpath' + target, get_first, timeout - 1)
