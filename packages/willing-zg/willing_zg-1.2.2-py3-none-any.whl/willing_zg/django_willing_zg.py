import logging

from zygoat.components import Component, SettingsComponent
from zygoat.components.backend import settings
from zygoat.constants import Phases
from zygoat.utils.backend import install_dependencies

log = logging.getLogger()


class DjangoWillingZgDependencies(Component):
    def create(self):
        dependencies = [
            "django-willing-zg",
        ]

        log.info("Installing django-willing-zg dependencies")
        install_dependencies(*dependencies)

    def update(self):
        self.call_phase(Phases.CREATE, force_create=True)


class DjangoWillingZgSettings(SettingsComponent):
    def create(self):
        red = self.parse()

        installed_apps = red.find("name", value="INSTALLED_APPS").parent.value
        installed_apps.append('"willing_zg"')

        log.info("Dumping django-willing-zg settings")
        self.dump(red)

    @property
    def installed(self):
        red = self.parse()
        return "willing_zg" in red.find("name", value="INSTALLED_APPS").parent.value


class DjangoWillingZg(Component):
    pass


django_willing_zg = DjangoWillingZg(
    sub_components=[DjangoWillingZgDependencies(), DjangoWillingZgSettings()],
    peer_dependencies=[settings],
)
