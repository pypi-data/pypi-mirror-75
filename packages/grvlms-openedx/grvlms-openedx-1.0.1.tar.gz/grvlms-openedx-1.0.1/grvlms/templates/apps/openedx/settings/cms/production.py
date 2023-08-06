# -*- coding: utf-8 -*-
import os
from cms.envs.production import *
from openedx.core.djangoapps.plugins import constants as plugin_constants

{% include "apps/openedx/settings/partials/common_cms.py" %}

ALLOWED_HOSTS = [
    ENV_TOKENS.get("CMS_BASE"),
    "cms",
    "127.0.0.1"
]

{{ patch("openedx-cms-production-settings") }}


# This is at the bottom because it is going to load more settings after base settings are loaded

plugin_settings.add_plugins(__name__, plugin_constants.ProjectType.CMS, plugin_constants.SettingsType.PRODUCTION)
