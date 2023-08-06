import inspect
import os


class YourBaseAccelerationConfig(object):
    """A fake config for use in tests."""

    def __init__(self, plugin, options):
        self.plugin = plugin
        self.options = options
        self.asked_for = []

    def get_plugin_options(self, module):
        """Just return the options for `module` if this is the right module."""
        self.asked_for.append(module)
        if module == self.plugin:
            return self.options
        else:
            return {}


CTX = None
ENABLED = False
PLUGIN = None

import yourbase_plugin

if yourbase_plugin.AVAILABLE:
    try:
        ENABLED = True
        from coverage.control import Plugins
        from coverage import Coverage
        from coverage.config import CoverageConfig

        CTX = Coverage()
        cconf = CoverageConfig()
        cconf.data_file = None
        CTX.set_option("run:plugins", ["yourbase_plugin"])
        print("[YB] Acceleration plugin available!")
        config = YourBaseAccelerationConfig("yourbase_plugin", {})
        print("[YB] Loading plugin!")
        plugins = Plugins.load_plugins(["yourbase_plugin"], config)
        print("[YB] Starting Python acceleration engine")
        CTX.start()
        p = CTX._plugins
        PLUGIN = p.get("yourbase_plugin.YourBasePlugin")

    except:
        import traceback

        print("[YB] Problem initializing acceleration subsystem")
        ENABLED = False
        traceback.print_exc()


def shutdown_acceleration(self, *args, **kwargs):
    if CTX and PLUGIN:
        print("[YB] Processing acceleration data")
        PLUGIN.dump_graph()
        CTX.stop()


def skip_when_possible(func):
    def wrapper(*args, **kwargs):
        if PLUGIN is None:
            func(*args, **kwargs)
        else:
            fname = "%s" % (func.__qualname__)
            fpath = os.getcwd() + os.sep + inspect.getfile(func)
            if PLUGIN.can_skip(fpath, fname):
                print("[YB] Skipping %s (@ %s)" % (fname, fpath))
            else:
                PLUGIN.start_test(fpath, fname)
                func(*args, **kwargs)
                PLUGIN.end_test(fpath, fname)

    return wrapper


def accelerate_tests():
    class ClassWrapper:
        def __init__(self, cls):
            self.other_class = cls

        def __call__(self, *cls_ars):
            other = self.other_class(*cls_ars)
            funcs = inspect.getmembers(self.other_class, predicate=inspect.isfunction)
            for fn in funcs:
                f = fn[0]
                if callable(getattr(other, f)):
                    setattr(other, f, skip_when_possible(getattr(other, f)))
            return other

    return ClassWrapper
