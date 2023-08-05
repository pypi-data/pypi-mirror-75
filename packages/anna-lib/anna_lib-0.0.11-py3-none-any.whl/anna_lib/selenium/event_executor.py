from typing import Union

from anna_lib.selenium import events
from selenium.webdriver.remote.webdriver import WebDriver


class EventExecutor:
    driver: WebDriver

    def __init__(self, driver: WebDriver):
        self.driver = driver

    def send_keys(self, target: str, value: str, timeout: int = 16) -> Union[bool, None]:
        return events.send_keys(self.driver, target, value, timeout)

    def submit(self, target: str, timeout: int = 16) -> Union[bool, None]:
        return events.submit(self.driver, target, timeout)

    def click(self, target: str, timeout: int = 16) -> Union[bool, None]:
        return events.click(self.driver, target, timeout)

    def hover(self, target: str, timeout: int = 16) -> Union[bool, None]:
        return events.hover(self.driver, target, timeout)

    def wait(self, target: str, timeout: int = 16, clickable: bool = False) -> bool:
        return events.wait(self.driver, target, timeout, clickable)

    def switch_to(self, target: str, timeout: int = 16) -> Union[bool, None]:
        return events.switch_to(self.driver, target, timeout)

    def scroll_to(self, target: str, timeout: int = 16) -> Union[bool, None]:
        return events.scroll_to(self.driver, target, timeout)
