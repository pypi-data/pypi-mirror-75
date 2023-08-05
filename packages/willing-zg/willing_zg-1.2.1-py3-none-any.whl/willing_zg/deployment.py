import json
import logging


from zygoat.components import Component, FileComponent
from zygoat.constants import Projects
from zygoat.utils.files import use_dir

from . import resources

log = logging.getLogger()

zappa_settings = "zappa_settings.json"
script = "deploy.py"
dockerfile = "Dockerfile"


class ScriptRequirements(FileComponent):
    resource_pkg = resources
    filename = "requirements.deploy.txt"
    overwrite = False


class Script(FileComponent):
    resource_pkg = resources
    filename = "deploy.py"
    overwrite = False
    executable = True


class ZappaSettingsFile(FileComponent):
    resource_pkg = resources
    base_path = Projects.BACKEND
    filename = zappa_settings
    overwrite = False


class ZappaSettingsUpdates(Component):
    def create(self):
        with use_dir(Projects.BACKEND):
            data = {}

            with open(zappa_settings) as f:
                data = json.load(f)

            log.info("Tweaking zappa settings to be specific to this app")

            data["base"]["project_name"] = f"{self.config.name}-backend"
            data["base"]["s3_bucket"] = f"com.willing.{self.config.name}-deployments"
            data["base"]["certificate_arn"] = "REPLACE THIS TO DEPLOY"

            log.info("Writting out zappa settings")
            with open(zappa_settings, "w") as f:
                json.dump(data, f)

    @property
    def installed(self):
        with use_dir(Projects.BACKEND):
            data = {}
            with open(zappa_settings) as f:
                data = json.load(f)

            return data["base"].get("project_name", None) is not None


class FrontendProductionDockerFile(FileComponent):
    resource_pkg = resources
    base_path = Projects.FRONTEND
    filename = dockerfile
    overwrite = False


class Deployment(Component):
    pass


deployment = Deployment(
    sub_components=[
        ZappaSettingsFile(sub_components=[ZappaSettingsUpdates()]),
        Script(sub_components=[ScriptRequirements()]),
        FrontendProductionDockerFile(),
    ]
)
