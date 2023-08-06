# -*- coding: utf-8 -*-
import os
from lms.envs.production import *
from openedx.core.djangoapps.plugins import constants as plugin_constants

{% include "apps/openedx/settings/partials/common_lms.py" %}

ALLOWED_HOSTS = [
    ENV_TOKENS.get("LMS_BASE"),
    FEATURES["PREVIEW_LMS_BASE"],
    "lms",
    "127.0.0.1"
]

# Required to display all courses on start page
SEARCH_SKIP_ENROLLMENT_START_DATE_FILTERING = True

{% if OPENEDX_RELEASE_VERSION == "juniper" %}
LMS_CFG=/openedx/config/lms.yml
{% endif %}

{{ patch("openedx-lms-production-settings") }}

# This is at the bottom because it is going to load more settings after base settings are loaded

plugin_settings.add_plugins(__name__, plugin_constants.ProjectType.LMS, plugin_constants.SettingsType.PRODUCTION)
