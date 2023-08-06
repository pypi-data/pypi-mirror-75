import logging
import os

from zygoat.components import Component, FileComponent
from zygoat.constants import Projects

from . import resources

log = logging.getLogger()

"""
    This file contains a chat component and settings.
"""

class ChatSettings(FileComponent):
    resource_pkg = resources
    base_path = os.path.join(Projects.FRONTEND, "utils", "constants")
    filename = "chat.js"
    overwrite = False


class ChatWidget(FileComponent):
    resource_pkg = resources
    base_path = os.path.join(Projects.FRONTEND, "components")
    filename = "ChatWidget.js"


class Chat(Component):
    pass


chat = Chat(sub_components=[ChatSettings(), ChatWidget()])
