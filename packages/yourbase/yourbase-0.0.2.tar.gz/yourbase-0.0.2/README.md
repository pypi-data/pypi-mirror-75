# YourBase Python Skipper

## What is this?

This is a Python package you can use in conjunction with [YourBase](https://yourbase.io).

## What does it do?

YourBase has a unique test acceleration that records the execution of your
tests and builds a dependency graph that it can use to bypass tests that do not
need to be run based on the changes in a commit. This helps to make those
commands much finer-grained enabling more acceleration. 

To achieve this, when running in the YourBase CI, this package will load a
lighweight wrapper for Python that will determine if a test needs to run based
on the YourBase runtime dependency graph. 

## How do I use this?

Simply run
```python
pip install yourbase
pip freeze > requirements.txt
```

If you use [pytest][pytest] for testing, you're done! YourBase will attach to
pytest hooks on its own. If you're using a different testing framework, you
will need to decorate your tests with `@accelerate_tests()`:
```python
from yourbase import accelerate_tests

# ...

@accelerate_tests()
class TestApplication:
    # ...
```

In both situations, when you run your tests locally it will have no impact at
all other than printing that it won't accelerate your tests. When you run
your tests in the YourBase CI, they will be accelerated where possible.

[pytest]: https://pytest.org

## Local development
This open source package is a lightweight wrapper for your code that plugs it
into the more complex proprietary systems powering YourBase CI servers. We
welcome contributions to this wrapper, but at this time we have not built
shims or mocks to allow it to be tested front to back outside our systems.

### Code style
We use [Black][black] for code formatting, which is similar in personality to
`gofmt` -- ruthless consistency, no configuration. Your build **will not pass
CI** if the Black run doesn't come back clean, so we recommend you have your
editor automatically run it on save. You can run it manually with

```sh
black .
```

[black]: https://pypi.org/project/black/