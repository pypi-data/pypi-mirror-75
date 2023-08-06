import asyncio
import inspect
from asyncio import Future
from asyncio.exceptions import InvalidStateError
from typing import Any, Callable, Coroutine, List, Union

from unittrial.console import Console
from unittrial.logger import logger
from unittrial.testcase import TestCase
from unittrial.testconfig import TestConfig

config: TestConfig


async def _check_and_run(test: Union[Callable, TestCase]):
    global config

    if isinstance(test, TestCase):
        Console.writeStatus(f"{test.__class__.__name__}", f"{Console.BrightBlue}{len(test.tests)}")
        Console.indention += 1
        result = await run_blocking(test())
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
                result = await run_blocking(test())
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

                if config.stop_on_fail:
                    raise KeyboardInterrupt()

            elif logger.hasAnyLog() or not _special_func:
                if _special_func:
                    Console.writeStatus(f"{test.__name__}", f"{Console.BrightGreen}Success")
                else:
                    Console.updateStatus(f"{test.__name__}", f"{Console.BrightGreen}Success")

                logger._indent_and_print()

        return result


def _global_setup_wrapper(global_setup: Union[Callable[..., Any], Callable[..., Coroutine]]) -> Union[Callable[..., Any], Callable[..., Coroutine]]:
    global_setup.__name__ = "_global_setup"
    return global_setup


def _global_teardown_wrapper(global_teardown: Union[Callable[..., Any], Callable[..., Coroutine]]) -> Union[Callable[..., Any], Callable[..., Coroutine]]:
    global_teardown.__name__ = "_global_teardown"
    return global_teardown


async def run_blocking(call: Union[Coroutine, Future]):
    loop = asyncio.get_event_loop()
    fut = loop.create_future()

    async def _blocking():
        try:
            fut.set_result(await call)
        except Exception as e:
            fut.set_result(e)

    loop.create_task(_blocking())

    while True:
        try:
            result = fut.result()
            if isinstance(result, Exception):
                raise result
            else:
                return result
        except InvalidStateError:
            await asyncio.sleep(0.1)


def run_tests(
        tests: List[Union[Callable, TestCase]],
        testconfig: TestConfig = TestConfig(),
        global_setup: Union[Callable[..., Any], Coroutine] = lambda: None,
        global_teardown: Union[Callable[..., Any], Coroutine] = lambda: None,
        ):

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

