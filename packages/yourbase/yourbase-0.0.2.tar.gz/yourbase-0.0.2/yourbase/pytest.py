# This file sets up YourBase pytest integration.
#
# For projects using pytest, the project only needs to add yourbase to its
# requirements file. This file will be run as an entry point (via setup.py) and
# will attach to pytest hooks so that tests do not need to be decorated.
#
# For projects not using pytest, or when running outside of the YourBase CI,
# this file does nothing.

import yourbase


if yourbase.ENABLED:
    try:
        import pytest

        print("[YB] pytest found, attaching")
        from . import skip_when_possible

        @pytest.hookimpl(tryfirst=True)
        def pytest_collection_modifyitems(session, config, items):
            for item in items:
                item.function.function = skip_when_possible(item.function)

    except ModuleNotFoundError:
        print(
            "[YB] YourBase pytest code was initiated, but pytest wasn't found. Is pytest installed oddly?"
        )
