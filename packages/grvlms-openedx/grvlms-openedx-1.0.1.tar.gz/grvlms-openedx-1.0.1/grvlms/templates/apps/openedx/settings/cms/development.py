# -*- coding: utf-8 -*-
import os
from cms.envs.devstack import *
from openedx.core.djangoapps.plugins import constants as plugin_constants

{% include "apps/openedx/settings/partials/common_cms.py" %}

# Setup correct webpack configuration file for development
WEBPACK_CONFIG_PATH = "webpack.dev.config.js"

{{ patch("openedx-cms-development-settings") }}

# This is at the bottom because it is going to load more settings after base settings are loaded

plugin_settings.add_plugins(__name__, plugin_constants.ProjectType.CMS, plugin_constants.SettingsType.DEVSTACK)
