# -*- coding: utf-8 -*-

import re
from picard.plugin3.api import PluginApi

_api = None

SOUNDTRACK_KEYWORDS = (
    'soundtrack', 'ost', 'original motion picture', 'original score',
    'motion picture soundtrack', 'music from', 'music inspired by',
    'game soundtrack', 'original soundtrack', 'tvアニメ', 'サントラ',
    'オリジナル・サウンドトラック', 'オリジナルサウンドトラック', '劇中歌', 'bgm'
)

def process_soundtrack(*args, **kwargs):
    obj = None
    metadata = None
    release = None

    for a in args:
        if hasattr(a, 'getall'):
            metadata = a
        elif isinstance(a, dict):
            release = a
        elif hasattr(a, 'album') or hasattr(a, 'tracks') or hasattr(a, 'filename'):
            obj = a

    if not metadata:
        return

    is_soundtrack = False

    # 1. Check release types in metadata
    rel_types = []
    for tag in ('releasetype', 'musicbrainz_releasetype'):
        rt = metadata.getall(tag) if hasattr(metadata, 'getall') else metadata.get(tag, [])
        if isinstance(rt, (list, tuple)):
            rel_types.extend([str(x).lower() for x in rt])
        elif rt:
            rel_types.extend([str(x).lower() for x in str(rt).split('/')])

    if any(k in t for t in rel_types for k in ('soundtrack', 'ost', 'score')):
        is_soundtrack = True

    # 2. Check release group from MB release dict
    if not is_soundtrack and release and isinstance(release, dict):
        rg = release.get('release-group', {})
        sec_types = rg.get('secondary-types', [])
        prim_type = rg.get('primary-type', '')
        all_types = [str(x).lower() for x in sec_types] + ([str(prim_type).lower()] if prim_type else [])
        if any(k in t for t in all_types for k in ('soundtrack', 'ost', 'score')):
            is_soundtrack = True

    # 3. Check album title, originalalbum, or track title
    if not is_soundtrack:
        for key in ('album', 'originalalbum', 'title'):
            val = metadata.get(key, '')
            if isinstance(val, list) and val:
                val = val[0]
            val_lower = str(val).lower()
            if any(kw in val_lower for kw in SOUNDTRACK_KEYWORDS):
                is_soundtrack = True
                break

    # 4. Check genre
    if not is_soundtrack:
        genres = metadata.getall('genre') if hasattr(metadata, 'getall') else metadata.get('genre', [])
        if isinstance(genres, str):
            genres = [genres]
        if any(k in str(g).lower() for g in genres for k in ('soundtrack', 'ost', 'score')):
            is_soundtrack = True

    # 5. Check filename / file path
    if not is_soundtrack and obj:
        fn = getattr(obj, 'filename', '') or (getattr(obj, 'file', None) and getattr(obj.file, 'filename', ''))
        if fn and any(k in str(fn).lower() for k in ('soundtrack', 'ost', 'score')):
            is_soundtrack = True

    if is_soundtrack:
        metadata["albumartist"] = "Soundtrack"
        metadata["albumartistsort"] = "Soundtrack"


def enable(api: PluginApi):
    global _api
    _api = api
    api.register_album_metadata_processor(process_soundtrack)
    api.register_track_metadata_processor(process_soundtrack)
