from io import BytesIO

from teleporter.core import Int, Long

class PeerId(int):
    def __new__(cls) -> int:
        raise NotImplementedError

class lsk(int):
    user_map = 0x00
    draft = 0x01 # data: PeerId peer
    draft_position = 0x02 # data: PeerId peer
    legacy_images = 0x03 # legacy
    locations = 0x04 # no data
    legacy_sticker_images = 0x05 # legacy
    legacy_audios = 0x06 # legacy
    recent_stickers_old = 0x07 # no data
    background_old_old = 0x08 # no data
    settings = 0x09 # no data
    recent_hashtags_and_bots = 0x0A # no data
    stickers_old = 0x0B # no data
    saved_peers_old = 0x0C # no data
    report_spam_statuses_old = 0x0D # no data
    saved_gifs_old = 0x0E # no data
    saved_gifs = 0x0F # no data
    stickers_keys = 0x10 # no data
    trusted_bots = 0x11 # no data
    faved_stickers = 0x12 # no data
    export_settings = 0x13 # no data
    background_old = 0x14 # no data
    self_serialized = 0x15 # serialized self
    masks = 0x16 # no data
    custom_emoji_keys = 0x17, # no data
    search_suggestions = 0x18, # no data
    webview_tokens = 0x19, # data: QByteArray bots, QByteArray other
    round_placeholder = 0x1a, # no data
    inline_bots_downloads = 0x1b, # no data
    media_last_playback_positions = 0x1c, # no data
    bot_storages = 0x1d, # data: PeerId botId

def Map(
    drafts: dict[PeerId, int] = None,
    draft_cursors: dict[PeerId, int] = None,
    drafts_not_read: dict[PeerId, bool] = None,

    locations: int = 0,
    trusted_bots: int = 0,
    installed_stickers: int = 0,
    featured_stickers: int = 0,
    recent_stickers: int = 0,
    faved_stickers: int = 0,
    archived_stickers: int = 0,
    archived_masks: int = 0,
    saved_gifs: int = 0,
    recent_stickers_old: int = 0,
    legacy_background_day: int = 0,
    legacy_background_night: int = 0,

    settings: int = 0,

    recent_hashtags_and_bots: int = 0,
    export_settings: int = 0,
    installed_masks: int = 0,
    recent_masks: int = 0
) -> bytes:
    b = BytesIO()

    if drafts:
        b.write(Int(lsk.draft))
        b.write(Int(len(drafts)))
        for key, value in drafts.items():
            b.write(Long(value))
            b.write(Long(key))

    if draft_cursors:
        b.write(Int(lsk.draft_position))
        b.write(Int(len(draft_cursors)))
        for key, value in draft_cursors.items():
            b.write(Long(value))
            b.write(Long(key))

    if locations:
        b.write(Int(lsk.locations))
        b.write(Long(locations))

    if trusted_bots:
        b.write(Int(lsk.trusted_bots))
        b.write(Long(trusted_bots))

    if recent_stickers_old:
        b.write(Int(lsk.recent_stickers_old))
        b.write(Long(recent_stickers_old))

    if (
        installed_stickers
        or featured_stickers
        or recent_stickers
        or archived_stickers
    ):
        b.write(Int(lsk.stickers_keys))
        b.write(Long(installed_stickers))
        b.write(Long(featured_stickers))
        b.write(Long(recent_stickers))
        b.write(Long(archived_stickers))

    if faved_stickers:
        b.write(Int(lsk.faved_stickers))
        b.write(Long(faved_stickers))

    if saved_gifs:
        b.write(Int(lsk.saved_gifs))
        b.write(Long(saved_gifs))

    if settings:
        b.write(Int(lsk.settings))
        b.write(Long(settings))

    if recent_hashtags_and_bots:
        b.write(Int(lsk.recent_hashtags_and_bots))
        b.write(Long(recent_hashtags_and_bots))

    if export_settings:
        b.write(Int(lsk.export_settings))
        b.write(Long(export_settings))

    if installed_masks or recent_masks or archived_masks:
        b.write(Long(lsk.masks))
        b.write(Long(installed_masks))
        b.write(Long(recent_masks))
        b.write(Long(archived_masks))

    return b.getvalue()
