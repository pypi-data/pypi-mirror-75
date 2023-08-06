import logging
import os

from zygoat.components import Component, FileComponent, SettingsComponent
from zygoat.components.backend import settings
from zygoat.constants import Projects

from . import resources

log = logging.getLogger()

"""
    This file contains a few components for setting up basic email capabilities:
    - Takes care of settings for sending email through AWS SES
    - Creates a Mailer class that Zygoat applications can subclass
    - Adds some basic email templates
"""

email_settings = [
    '# production must use SMTP. others will use DJANGO_EMAIL_BACKEND or default to "console"',
    """EMAIL_BACKEND = "django.core.mail.backends.{}.EmailBackend".format(env.str("DJANGO_EMAIL_BACKEND", default="console") if DEBUG else "smtp")""",
    'EMAIL_HOST = "email-smtp.us-east-1.amazonaws.com"',
    "EMAIL_PORT = 587",
    'EMAIL_HOST_USER = prod_required_env("DJANGO_EMAIL_HOST_USER", "")',
    'EMAIL_HOST_PASSWORD = prod_required_env("DJANGO_EMAIL_HOST_PASSWORD", "")',
    "EMAIL_USE_TLS = True",
]

support_settings = [
    'SUPPORT_PHONE_NUMBER = "+1 (855) 943-4177"',
    'SUPPORT_EMAIL_ADDRESS = "clientservice@legalplans.com"',
    'PANEL_EMAIL_ADDRESS = "panel@legalplans.com"',
]


class EmailSettings(SettingsComponent):
    def create(self):
        red = self.parse()
        red.extend(["\n"] + email_settings)
        red.extend(["\n"] + support_settings)

        log.info("Dumping Django email and support settings")
        self.dump(red)

    @property
    def installed(self):
        red = self.parse()
        return red.find("name", value="EMAIL_BACKEND") is not None


class EmailClass(FileComponent):
    resource_pkg = resources
    base_path = os.path.join(Projects.BACKEND, "shared")
    filename = "mailer.py"


class EmailTemplate(FileComponent):
    resource_pkg = resources
    base_path = os.path.join(Projects.BACKEND, "backend", "templates", "email")


class HtmlTemplate(EmailTemplate):
    filename = "mlp_transactional_email.html"


class TextTemplate(EmailTemplate):
    filename = "mlp_transactional_email.txt"


class Email(Component):
    pass


email = Email(
    sub_components=[EmailSettings(), EmailClass(), HtmlTemplate(), TextTemplate()],
    peer_dependencies=[settings],
)
