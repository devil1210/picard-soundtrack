# -*- coding: utf-8 -*-

from picard.plugin3.api import PluginApi

_api = None

def process_soundtrack(*args, **kwargs):
    obj = None
    metadata = None
    release = None
    for a in args:
        if hasattr(a, 'getall') or (isinstance(a, dict) and ('title' in a or 'releasetype' in a)):
            metadata = a
        elif isinstance(a, dict) and 'release-group' in a:
            release = a
        elif hasattr(a, 'album') or hasattr(a, 'tracks'):
            obj = a

    if not metadata:
        return

    rel_types = []
    if hasattr(metadata, 'getall'):
        rt = metadata.getall('releasetype')
    else:
        rt = metadata.get('releasetype', [])

    if isinstance(rt, (list, tuple)):
        rel_types.extend([str(x).lower() for x in rt])
    elif rt:
        rel_types.extend([str(x).lower() for x in str(rt).split('/')])

    if obj and hasattr(obj, 'album') and obj.album and hasattr(obj.album, 'metadata'):
        a_rt = obj.album.metadata.getall('releasetype') if hasattr(obj.album.metadata, 'getall') else obj.album.metadata.get('releasetype', [])
        if isinstance(a_rt, (list, tuple)):
            rel_types.extend([str(x).lower() for x in a_rt])
        elif a_rt:
            rel_types.extend([str(x).lower() for x in str(a_rt).split('/')])

    if release and isinstance(release, dict):
        rg = release.get('release-group', {})
        sec_types = rg.get('secondary-types', [])
        prim_type = rg.get('primary-type', '')
        rel_types.extend([str(x).lower() for x in sec_types])
        if prim_type:
            rel_types.append(str(prim_type).lower())

    path_is_soundtrack = False
    if obj and hasattr(obj, 'filename') and obj.filename and 'soundtrack' in str(obj.filename).lower():
        path_is_soundtrack = True

    is_soundtrack = any('soundtrack' in t or 'ost' in t or 'score' in t for t in rel_types) or path_is_soundtrack

    if is_soundtrack:
        metadata["albumartist"] = "Soundtrack"
        metadata["albumartistsort"] = "Soundtrack"


def enable(api: PluginApi):
    global _api
    _api = api
    api.register_album_metadata_processor(process_soundtrack)
    api.register_track_metadata_processor(process_soundtrack)
