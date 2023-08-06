from typing import Callable, List

from unittrial import _check_and_run


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

