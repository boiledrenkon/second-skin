import json
from src.util import resolve_key


def form(key, whisp_cache):
    forms = {1: simple_array, 2: full_array, 4: simple_map, 8: full_map}
    specs = resolve_key(key)
    return [
        json.dumps(forms[spec](whisp_cache), indent=2, sort_keys=True, default=str)
        for spec in specs
    ]


def simple_array(whisp_cache):
    return [
        {
            "content": whisp.content,
            "name": whisp.author.name,
            "created_at": whisp.created_at,
            "edited_at": whisp.edited_at,
            "reactions": whisp.reactions,
            "message_id": whisp.id,
        }
        for whisp in whisp_cache
    ]


def full_array(whisp_cache):
    return [
        {
            "content": whisp.content,
            "name": whisp.author.name,
            "created_at": whisp.created_at,
            "edited_at": whisp.edited_at,
            "message_id": whisp.id,
            "reactions": whisp.reactions,
            "activity": whisp.activity,
            "application": whisp.application,
            "attachments": whisp.attachments,
            "channel": whisp.channel,
            "channel_mentions": whisp.channel_mentions,
            "clean_content": whisp.clean_content,
            "embeds": whisp.embeds,
            "guild": whisp.guild,
            "jump_url": whisp.jump_url,
            "mention_everyone": whisp.mention_everyone,
            "mentions": whisp.mentions,
            "nonce": whisp.nonce,
            "pinned": whisp.pinned,
            "raw_channel_mentions": whisp.raw_channel_mentions,
            "raw_mentions": whisp.raw_mentions,
            "raw_role_mentions": whisp.raw_role_mentions,
            "reference": whisp.reference,
            "role_mentions": whisp.role_mentions,
            "stickers": whisp.stickers,
            "system_content": whisp.system_content,
            "tts": whisp.tts,
            "type": whisp.type,
            "webhook_id": whisp.webhook_id,
        }
        for whisp in whisp_cache
    ]


def simple_map(whisp_cache):
    return {
        f"{whisp.created_at}###{whisp.author.name}###{whisp.id}": {
            "content": whisp.content,
            "name": whisp.author.name,
            "created_at": whisp.created_at,
            "edited_at": whisp.edited_at,
            "reactions": whisp.reactions,
            "message_id": whisp.id,
        }
        for whisp in whisp_cache
    }


def full_map(whisp_cache):
    return {
        f"{whisp.created_at}###{whisp.author.name}###{whisp.id}": {
            "content": whisp.content,
            "name": whisp.author.name,
            "created_at": whisp.created_at,
            "edited_at": whisp.edited_at,
            "message_id": whisp.id,
            "reactions": whisp.reactions,
            "activity": whisp.activity,
            "application": whisp.application,
            "attachments": whisp.attachments,
            "channel": whisp.channel,
            "channel_mentions": whisp.channel_mentions,
            "clean_content": whisp.clean_content,
            "embeds": whisp.embeds,
            "guild": whisp.guild,
            "jump_url": whisp.jump_url,
            "mention_everyone": whisp.mention_everyone,
            "mentions": whisp.mentions,
            "nonce": whisp.nonce,
            "pinned": whisp.pinned,
            "raw_channel_mentions": whisp.raw_channel_mentions,
            "raw_mentions": whisp.raw_mentions,
            "raw_role_mentions": whisp.raw_role_mentions,
            "reference": whisp.reference,
            "role_mentions": whisp.role_mentions,
            "stickers": whisp.stickers,
            "system_content": whisp.system_content,
            "tts": whisp.tts,
            "type": whisp.type,
            "webhook_id": whisp.webhook_id,
        }
        for whisp in whisp_cache
    }
