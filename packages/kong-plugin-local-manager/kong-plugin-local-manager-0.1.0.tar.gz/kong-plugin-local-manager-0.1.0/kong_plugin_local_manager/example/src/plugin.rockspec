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