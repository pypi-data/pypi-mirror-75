import unittrial

from typing import Callable, List


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
        await unittrial._check_and_run(self.setup_class)

        for test in self.tests:

            await unittrial._check_and_run(self.setup)

            await unittrial._check_and_run(test)

            await unittrial._check_and_run(self.teardown)

        await unittrial._check_and_run(self.teardown_class)

