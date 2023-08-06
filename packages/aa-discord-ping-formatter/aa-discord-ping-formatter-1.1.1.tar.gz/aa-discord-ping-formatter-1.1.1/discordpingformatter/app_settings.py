from django.conf import settings
from .utils import clean_setting
import re

# set default panels if none are set in local.py
AA_DISCORDFORMATTER_ADDITIONAL_PING_TARGETS = clean_setting('AA_DISCORDFORMATTER_ADDITIONAL_PING_TARGETS', [])
AA_DISCORDFORMATTER_ADDITIONAL_FLEET_TYPES = clean_setting('AA_DISCORDFORMATTER_ADDITIONAL_FLEET_TYPES', [])
AA_DISCORDFORMATTER_ADDITIONAL_PING_WEBHOOKS = clean_setting('AA_DISCORDFORMATTER_ADDITIONAL_PING_WEBHOOKS', [])
AA_DISCORDFORMATTER_WEBHOOK_EMBED_PING = clean_setting('AA_DISCORDFORMATTER_WEBHOOK_EMBED_PING', False)
AA_DISCORDFORMATTER_FLEET_COMMS = clean_setting('AA_DISCORDFORMATTER_FLEET_COMMS', [])
AA_DISCORDFORMATTER_FLEET_DOCTRINES = clean_setting('AA_DISCORDFORMATTER_FLEET_DOCTRINES', [])
AA_DISCORDFORMATTER_FLEET_FORMUP_LOCATIONS = clean_setting('AA_DISCORDFORMATTER_FLEET_FORMUP_LOCATIONS', [])


def get_site_url():  # regex sso url
    regex = r"^(.+)\/s.+"
    matches = re.finditer(regex, settings.ESI_SSO_CALLBACK_URL, re.MULTILINE)
    url = "http://"

    for m in matches:
        url = m.groups()[0] # first match

    return url


def timezones_installed():
    return 'timezones' in settings.INSTALLED_APPS
