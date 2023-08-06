import os
from kong_plugin_local_manager import KongPluginLocalManager


application_root = os.path.abspath(os.path.dirname(__file__))
manager = KongPluginLocalManager(application_root).get_manager()

if __name__ == "__main__":
    manager()