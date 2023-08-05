from typing import Union

from selenium.webdriver import ActionChains
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException, NoSuchElementException

from . import util


def send_keys(driver: WebDriver, target: str, value: str, timeout: int = 16) -> Union[bool, None]:
	if wait(driver, target, timeout):
		element = util.get_element(driver=driver, target=target, timeout=timeout)
		try:
			element.send_keys(value.encode('ascii', 'ignore').decode("utf-8"))
		except NoSuchElementException:
			return False
	else:
		return False


def submit(driver: WebDriver, target: str, timeout: int = 16) -> Union[bool, None]:
	if wait(driver, target, timeout):
		element = util.get_element(driver=driver, target=target, timeout=timeout)
		try:
			element.submit()
		except NoSuchElementException:
			return False
	else:
		return False


def click(driver: WebDriver, target: str, timeout: int = 16) -> Union[bool, None]:
	if wait(driver, target, timeout, True):
		element = util.get_element(driver=driver, target=target, timeout=timeout)
		if isinstance(element, tuple) and len(element) > 0 and element[0] == False:
			return False
		if element.tag_name == 'option':
			element.click()
		else:
			action = ActionChains(driver)
			action.move_to_element(element)
			action.click(element)
			action.perform()
	else:
		return False


def hover(driver: WebDriver, target: str, timeout: int = 16) -> Union[bool, None]:
	if wait(driver, target, timeout):
		element = util.get_element(driver=driver, target=target, timeout=timeout)
		driver.execute_script("var event = new MouseEvent('mouseover', {'view': window, 'bubbles': true, 'cancelable': true});arguments[0].dispatchEvent(event);", element)
		action = ActionChains(driver)
		action.move_to_element(element)
		action.perform()
	else:
		return False


def wait(driver: WebDriver, target: str, timeout: int = 16, clickable: bool = False) -> bool:
	try:
		if not target.startswith('$css') and not target.startswith('$xpath'):
			target = '$css' + target
		if clickable:
			if target.startswith('$xpath'):
				WebDriverWait(driver=driver, timeout=timeout).until(ec.element_to_be_clickable((By.XPATH, target[6:])))
			else:
				WebDriverWait(driver=driver, timeout=timeout).until(
					ec.element_to_be_clickable((By.CSS_SELECTOR, target[4:])))
		else:
			if target.startswith('$xpath'):
				WebDriverWait(driver=driver, timeout=timeout).until(
					ec.presence_of_element_located((By.XPATH, target[6:])))
			else:
				WebDriverWait(driver=driver, timeout=timeout).until(
					ec.presence_of_element_located((By.CSS_SELECTOR, target[4:])))
	except TimeoutException:
		return False
	return True


def switch_to(driver: WebDriver, target: str, timeout: int = 16) -> Union[bool, None]:
	if wait(driver=driver, target=target, timeout=timeout):
		element = util.get_element(driver=driver, target=target, timeout=timeout)
		driver.switch_to.frame(element)
	else:
		return False


def scroll_to(driver: WebDriver, target: str, timeout: int = 16) -> Union[bool, None]:
	if wait(driver=driver, target=target, timeout=timeout):
		element = util.get_element(driver=driver, target=target, timeout=timeout)
		driver.execute_script('arguments[0].scrollIntoView(true);', element)
	else:
		return False
