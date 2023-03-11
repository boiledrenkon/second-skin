from src.util import resolve_key

def form(key, ee_cache): 
    forms = {
        1: simple_array,
        2: full_array,
        4: simple_map,
        8: full_map
    }
    specs = resolve_key(key)
    return [ forms[spec](ee_cache) for spec in specs ]


def simple_array(ee_cache):
    for ee in ee_cache:
        yield {
            "content": ee.content,
            "name": ee.author.name,
            "created_at": ee.created_at,
            "edited_at": ee.edited_at,
            "reactions": ee.reactions,
            "message_id": ee.id
        } 


def full_array(ee_cache):
    for ee in ee_cache:
        yield {
            "content": ee.content,
            "name": ee.author.name,
            "created_at": ee.created_at,
            "edited_at": ee.edited_at,
            "message_id": ee.id,
            "reactions": ee.reactions,
            "activity": ee.activity,
            "application": ee.application,
            "attachments": ee.attachments,
            "channel": ee.channel,
            "channel_mentions": ee.channel_mentions, 
            "clean_content": ee.clean_content,
            "embeds": ee.embeds,
            "flags": ee.flags,
            "guild": ee.guild,
            "jump_url": ee.jump_url,
            "mention_everyone": ee.mention_everyone,
            "mentions": ee.mentions,
            "nonce": ee.nonce,
            "pinned": ee.pinned,
            "raw_channel_mentions": ee.raw_channel_mentions,
            "raw_mentions": ee.raw_mentions,
            "raw_role_mentions": ee.raw_role_mentions,
            "reference": ee.reference,
            "role_mentions": ee.role_mentions,
            "stickers": ee.stickers,
            "system_content": ee.system_content,
            "tts": ee.tts,
            "type": ee.type,
            "webhook_id": ee.webhook_id,
        } 


def simple_map(ee_cache):
    for ee in ee_cache:
        yield {
            f"{ee.created_at}###{ee.author.name}###{ee.id}": {
                "content": ee.content,
                "name": ee.author.name,
                "created_at": ee.created_at,
                "edited_at": ee.edited_at,
                "reactions": ee.reactions,
                "message_id": ee.id
            }
        }


def full_map(ee_cache):
    for ee in ee_cache:
        yield { 
               f"{ee.created_at}###{ee.author.name}###{ee.id}": {
                   "content": ee.content,
                   "name": ee.author.name,
                   "created_at": ee.created_at,
                   "edited_at": ee.edited_at,
                   "message_id": ee.id,
                   "reactions": ee.reactions,
                   "activity": ee.activity,
                   "application": ee.application,
                   "attachments": ee.attachments,
                   "channel": ee.channel,
                   "channel_mentions": ee.channel_mentions, 
                   "clean_content": ee.clean_content,
                   "embeds": ee.embeds,
                   "flags": ee.flags,
                   "guild": ee.guild,
                   "jump_url": ee.jump_url,
                   "mention_everyone": ee.mention_everyone,
                   "mentions": ee.mentions,
                   "nonce": ee.nonce,
                   "pinned": ee.pinned,
                   "raw_channel_mentions": ee.raw_channel_mentions,
                   "raw_mentions": ee.raw_mentions,
                   "raw_role_mentions": ee.raw_role_mentions,
                   "reference": ee.reference,
                   "role_mentions": ee.role_mentions,
                   "stickers": ee.stickers,
                   "system_content": ee.system_content,
                   "tts": ee.tts,
                   "type": ee.type,
                   "webhook_id": ee.webhook_id,
        }
    }
