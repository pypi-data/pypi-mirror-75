import abc

from anna_lib.selenium import assertions
from anna_lib.selenium.event_executor import EventExecutor


class AbstractTask(EventExecutor):
    def __init__(self, driver):
        super().__init__(driver)
        self.result = []
        self.passed = False
        self.timeout = 16

    def execute(self) -> None:
        self.before_execute()
        self.__execute__()
        self.after_execute()
        self.passed = all(r['passed'] is True for r in self.result)

    @abc.abstractmethod
    def before_execute(self) -> None:
        pass

    @abc.abstractmethod
    def __execute__(self) -> None:
        pass

    @abc.abstractmethod
    def after_execute(self) -> None:
        pass

    def _assert(self, assertion: str, param: str) -> None:
        try:
            method = getattr(assertions, assertion)
            self.result.append(
                {'assertion': assertion, 'passed': method(self.driver, param, timeout=self.timeout) is True})
        except TypeError as e:
            self.result.append(
                {
                    'assertion': assertion,
                    'passed': False,
                    'log': str(e)
                })
