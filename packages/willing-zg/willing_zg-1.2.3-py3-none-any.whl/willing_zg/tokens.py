from zygoat.components import FileComponent
from zygoat.constants import FrontendUtils

from . import resources


TOKEN_FILE = "tokens.js"


class TokenFile(FileComponent):
    resource_pkg = resources
    base_path = FrontendUtils
    filename = TOKEN_FILE
    overwrite = True


token_util = TokenFile()
