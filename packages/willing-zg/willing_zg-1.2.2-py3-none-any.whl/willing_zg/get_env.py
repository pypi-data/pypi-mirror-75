from zygoat.components import FileComponent
from zygoat.constants import FrontendUtils

from . import resources


GET_ENV_FILE = "getEnv.js"


class GetEnvFile(FileComponent):
    resource_pkg = resources
    base_path = FrontendUtils
    filename = GET_ENV_FILE
    overwrite = True


get_env_util = GetEnvFile()
