import pkg_resources
try:
    version = pkg_resources.require("damona")[0].version
except:
    version = ">=0.8.3"


