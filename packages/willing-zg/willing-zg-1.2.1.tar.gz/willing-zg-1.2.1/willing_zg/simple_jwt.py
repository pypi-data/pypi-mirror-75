import logging

from zygoat.components import Component, SettingsComponent
from zygoat.components.backend import settings
from zygoat.constants import Phases
from zygoat.utils.backend import install_dependencies

log = logging.getLogger()

authentication_classes_string = """"DEFAULT_AUTHENTICATION_CLASSES": (
        "simplejwt_extensions.authentication.JWTAuthentication",
    ),
"""

default_key_string = '''DEFAULT_VERIFYING_KEY = """-----BEGIN PUBLIC KEY-----
MIGfMA0GCSqGSIb3DQEBAQUAA4GNADCBiQKBgQC91RWCawEvxQj+tigRvuHxouO8
jKd35ukUxFBFRAGcI57firbAkFII6zPIiWAENGMqtjX57hk9EjAZ27XvQ4SQACvD
5j7htsJT31bZbVUH7a3JEDpxa02VXpXdfPYSs8umZkdxMxxmiD9uH9VmLN3VS14l
xQlyJdlvbLmNCAf6uwIDAQAB
-----END PUBLIC KEY-----"""
'''

simple_jwt_string = """SIMPLE_JWT = {
    "USER_ID_FIELD": "public_id",
    "ALGORITHM": "RS512",
    "SIGNING_KEY": None,
    "VERIFYING_KEY": prod_required_env("DJANGO_JWT_VERIFYING_KEY", DEFAULT_VERIFYING_KEY),
}
"""


class SimpleJWTSettings(SettingsComponent):
    def create(self):
        red = self.parse()

        rest_framework_settings = red.find("name", value="REST_FRAMEWORK").parent.value
        rest_framework_settings.append(authentication_classes_string)

        red.extend(
            ["\n", default_key_string, "\n", simple_jwt_string,]
        )

        log.info("Dumping Django SimpleJWT settings")
        self.dump(red)

    @property
    def installed(self):
        red = self.parse()
        return red.find("name", value="SIMPLE_JWT") is not None


class SimpleJWTDependencies(Component):
    def create(self):
        dependencies = [
            "djangorestframework-simplejwt",
            "cryptography",
            "simplejwt-extensions",
        ]

        log.info("Installing SimpleJWT dependencies")
        install_dependencies(*dependencies)

    def update(self):
        self.call_phase(Phases.CREATE, force_create=True)


class SimpleJWT(Component):
    pass


simple_jwt = SimpleJWT(
    sub_components=[SimpleJWTSettings(), SimpleJWTDependencies()], peer_dependencies=[settings]
)
