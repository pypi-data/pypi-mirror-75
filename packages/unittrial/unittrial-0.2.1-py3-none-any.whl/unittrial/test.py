import asyncio
import inspect

from unittrial.logger import logger
from unittrial.console import Console
from typing import Callable, List, Union, Coroutine, Any


class TestConfig(object):
    class LogConfig:
        format: str = ""

    stopOnFail = False
    logger: LogConfig = LogConfig()


config: TestConfig


class TestCase(object):
    tests: List[Callable] = []

    def setup_class(self):
        pass

    def setup(self):
        pass

    def teardown(self):
        pass

    def teardown_class(self):
        pass

    async def __call__(self, *args, **kwargs):
        await _check_and_run(self.setup_class)

        for test in self.tests:

            await _check_and_run(self.setup)

            await _check_and_run(test)

            await _check_and_run(self.teardown)

        await _check_and_run(self.teardown_class)


def _global_setup_wrapper(global_setup: Union[Callable[..., Any], Callable[..., Coroutine]]) -> Union[Callable[..., Any], Callable[..., Coroutine]]:
    global_setup.__name__ = "_global_setup"
    return global_setup


def _global_teardown_wrapper(global_teardown: Union[Callable[..., Any], Callable[..., Coroutine]]) -> Union[Callable[..., Any], Callable[..., Coroutine]]:
    global_teardown.__name__ = "_global_teardown"
    return global_teardown


async def _check_and_run(test: Union[Callable, TestCase]):
    global config

    if isinstance(test, TestCase):
        Console.writeStatus(f"{test.__class__.__name__}", f"{Console.BrightBlue}{len(test.tests)}")
        Console.indention += 1
        result = await test()
        Console.indention -= 1
        print('')

    else:
        _special_func = False
        if test.__name__ in ["_global_setup", "setup_class", "setup", "teardown", "teardown_class", "_global_teardown"]:
            _special_func = True

        if not _special_func:
            Console.writeStatus(f"{test.__name__}", f"{Console.BrightYellow}Running")

        result = None
        raised_exception = None

        try:
            if inspect.iscoroutinefunction(test):
                result = await test()
            else:
                result = test()

        except Exception as e:
            raised_exception = e

        finally:
            # Something failed in test
            if raised_exception is not None:

                if _special_func:
                    Console.writeStatus(f"{test.__name__}", f"{Console.BrightRed}Fail")
                else:
                    Console.updateStatus(f"{test.__name__}", f"{Console.BrightRed}Fail")

                logger._indent_and_print()

                Console.indention += 1
                Console.writeError(str(raised_exception) if isinstance(raised_exception, AssertionError) else f"{raised_exception.__class__.__name__}: {raised_exception}")
                Console.indention -= 1

            elif logger.hasAnyLog() or not _special_func:
                if _special_func:
                    Console.writeStatus(f"{test.__name__}", f"{Console.BrightGreen}Success")
                else:
                    Console.updateStatus(f"{test.__name__}", f"{Console.BrightGreen}Success")

                logger._indent_and_print()

            if config.stopOnFail:
                raise KeyboardInterrupt()

        return result


def run_tests(
        tests: List[Union[Callable, TestCase]],
        testconfig: TestConfig = TestConfig(),
        global_setup: Union[Callable[..., Any], Callable[..., Coroutine]] = lambda: None,
        global_teardown: Union[Callable[..., Any], Callable[..., Coroutine]] = lambda: None):

    async def async_start():

        await _check_and_run(_global_setup_wrapper(global_setup))

        for test in tests:

            await _check_and_run(test)

        await _check_and_run(_global_teardown_wrapper(global_teardown))

    global config
    config = testconfig

    try:
        asyncio.run(async_start())
    except KeyboardInterrupt:
        pass

