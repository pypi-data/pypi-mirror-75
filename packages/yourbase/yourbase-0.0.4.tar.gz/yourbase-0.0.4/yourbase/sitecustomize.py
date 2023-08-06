import yourbase

import atexit
import sys, os

plugin_path = os.environ.get("YB_PYTHON_PLUGIN_PATH", None)

if plugin_path:
    print("[YB] Setting up environment")
    sys.path.append(plugin_path)

atexit.register(yourbase.shutdown_acceleration, None, None)
