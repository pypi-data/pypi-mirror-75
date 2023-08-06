import inspect


def assert_equals(a, b):
    if a != b:
        raise AssertionError(f"Expected: {b} | Got: {a}")


def assert_false(a):
    if a:
        raise AssertionError(f"Expected: False | Got: {a}")


def assert_greater(a, b):
    if a <= b:
        raise AssertionError(f"Expected: Greater than {b} | Got: {a}")


def assert_greater_or_equal(a, b):
    if a < b:
        raise AssertionError(f"Expected: Greater than or equal {b} | Got: {a}")


def assert_is_instance(a, t):
    if a.__class__ == type:
        raise AssertionError(f"Type of {a} was passed but an instance is required.")

    if not isinstance(a, t):
        raise AssertionError(f"Expected: Instance of {t} | Got: {a} Type: {type(a)}")


def assert_is_none(a):
    if a is not None:
        raise AssertionError(f"Expected: None | Got: {a} Type: {type(a)}")


def assert_is_not_none(a):
    if a is None:
        raise AssertionError(f"Expected: Any | Got: None")


def assert_lesser(a, b):
    if a >= b:
        raise AssertionError(f"Expected: Lesser than {b} | Got: {a}")


def assert_lesser_or_equal(a, b):
    if a > b:
        raise AssertionError(f"Expected: Lesser than or equal {b} | Got: {a}")


def assert_true(a):
    if not a:
        raise AssertionError(f"Expected: True | Got: {a}")


def expect_failure(exception=Exception):
    def inner(test):
        async def wrapper(self=None):
            raised = None
            try:
                if inspect.iscoroutinefunction(test):
                    await test(self)
                else:
                    test(self)
            except Exception as e:
                raised = e
                if isinstance(e, exception):
                    return
            raise AssertionError(f"Expected a '{exception.__name__}' but '{type(raised).__name__}' was raised.")
        wrapper.__name__ = test.__name__
        return wrapper
    return inner
