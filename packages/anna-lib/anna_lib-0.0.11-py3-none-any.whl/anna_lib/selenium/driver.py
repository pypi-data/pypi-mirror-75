import re

from selenium import webdriver
from selenium.webdriver.remote.webdriver import WebDriver


def create(driver: str = 'firefox', headless: bool = True, resolution: tuple = (1920, 1080)) -> WebDriver:
	if driver not in ('firefox', 'chrome'):
		raise TypeError

	if driver == 'chrome':
		options = webdriver.ChromeOptions()
	elif driver == 'firefox':
		options = webdriver.FirefoxOptions()

	options.headless = headless

	if driver == 'chrome':
		d = webdriver.Chrome(options=options)
	elif driver == 'firefox':
		d = webdriver.Firefox(options=options)

	if not re.match(r"^[1-9]\d*,[1-9]\d*", ','.join(str(axis) for axis in resolution)):
		raise TypeError('specify a valid resolution')
	d.set_window_size(int(resolution[0]), int(resolution[1]))
	return d
