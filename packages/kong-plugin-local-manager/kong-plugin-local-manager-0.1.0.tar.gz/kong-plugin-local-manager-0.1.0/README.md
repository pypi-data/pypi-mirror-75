# kong-plugin-local-manager

Use python package to manage kong plugin, so that the plugin can be published to private pypi server and used internally. A temporary solution for PYTHONER using kong.

## Install

```shell
pip install kong-plugin-local-manager
```

## Example

**example files**

```
/example/
    /example/__init__.py
    /example/src/
        /example/src/lua/
            /example/src/lua/handler.lua
            /example/src/lua/schema.lua
        /example/src/plugin.rockspec
    /example/manager.py
    /example/setup.py
    /example/requirements.txt
    /example/README.txt
    /example/MANIFEST.in
    /example/LICENSE
```

**content of plugin.rockspec**

```
package = "example"
version = "0.1.0-1"
source = {
    url = "example-0.1.0-1.zip"
}
description = {
    summary = "kong plugin example",
}
dependencies = {
    "lua >= 5.1, < 5.4",
}
build = {
    type = "builtin",
    modules = {
        ["kong.plugins.example.handler"] = "lua/handler.lua",
        ["kong.plugins.example.schema"] = "lua/schema.lua",
    }
}
```

**content of example_manager.py**

```python
import os
from kong_plugin_local_manager import KongPluginLocalManager


application_root = os.path.abspath(os.path.dirname(__file__))
manager = KongPluginLocalManager(application_root).get_manager()

if __name__ == "__main__":
    manager()
```

**content of setup.py**

```
setup(
    ...
    entry_points={
        "console_scripts": [
            "example-manager = example.manager:manager",
        ],
    },
)
```

**usage of example-manager**

```shell
Usage: example-manager [OPTIONS] COMMAND [ARGS]...

Options:
  --help  Show this message and exit.

Commands:
  install  Create a lua package and then install it.
  pack     Create a lua package.
```

## Releases

### v0.1.0 2020/07/30

- First release.