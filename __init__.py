
_api = None

def _get_option(key, default=None):
    global _api
    if _api and hasattr(_api, "plugin_config"):
        try:
            val = __get_option(key)
            if val is not None:
                return val
        except Exception:
            pass
    if hasattr(config, "setting"):
        try:
            val = config.setting[key]
            if val is not None:
                return val
        except Exception:
            pass
    return default

_api = None
# -*- coding: utf-8 -*-

# Copyright © 2015 Samir Benmendil <me@rmz.io>
# This work is free. You can redistribute it and/or modify it under the
# terms of the Do What The Fuck You Want To Public License, Version 2,
# as published by Sam Hocevar. See http://www.wtfpl.net/ for more details.


from picard.plugin3.api import PluginApi



def soundtrack(tagger, metadata, release):
    if "soundtrack" in metadata["releasetype"]:
        metadata["albumartist"] = "Soundtrack"
        metadata["albumartistsort"] = "Soundtrack"


def enable(api: PluginApi):
    global _api
    _api = api
    """Called when plugin is enabled."""
    api.register_album_metadata_processor(soundtrack)