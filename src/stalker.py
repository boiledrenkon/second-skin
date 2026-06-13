from typing import Any, Generator

MESSAGE_MIN = 6
SUMMARY_COUNT = 50


class Guild:
    def __init__(self, guild_id):
        self.guild_id: str = guild_id
        self.messages: list[dict[str, Any]] = []

    @property
    def messages_len(self) -> int:
        return len(self.messages)

    def _is_valid_message(self, content: str) -> bool:
        return len(content.split(" ")) >= MESSAGE_MIN

    def add_message(self, content: str, author: str) -> bool:
        if self._is_valid_message(content):
            self.messages.append({"content": content, "name": author})
            return True
        return False

    def empty_messages(self) -> None:
        self.messages = []


class Stalker:
    def __init__(self, user):
        self.user = user
        self.username = user.name
        self.guilds: dict[str, Guild] = {}

    def _get_guild(self, guild_id: str) -> Guild:
        guild: Guild
        if guild_id in self.guilds:
            guild = self.guilds.get(guild_id)
        else:
            guild = Guild(guild_id)
            self.guilds[guild_id] = guild
        return guild

    def _add_message(
        self, guild: Guild, content: str, author: str
    ) -> list[dict[str, Any]]:
        added = guild.add_message(content, author)
        batch: list[dict[str, Any]] = []
        if added and guild.messages_len >= SUMMARY_COUNT:
            batch = list(guild.messages)
            guild.empty_messages()
        return batch

    def on_message(self, message: Any) -> list[dict[str, Any]]:
        # Collect only the stalked user's own messages, and only inside a guild.
        # Returns a batch of {content, name} dicts once SUMMARY_COUNT pile up,
        # otherwise an empty list.
        if self.user != message.author or message.guild is None:
            return []
        guild = self._get_guild(message.guild.id)
        return self._add_message(guild, message.content, message.author.name)

    def on_react(self, reaction, user) -> str:
        message = reaction.message
        if self.user == user:
            return f"{self.username} thought something was {reaction.emoji} in {message.guild}"

    async def on_raw_react(self, raw_reaction: Any, client: Any) -> str | None:
        if raw_reaction.event_type != "REACTION_ADD":
            return None
        channel = await client.fetch_channel(raw_reaction.channel_id)
        user = await client.fetch_user(raw_reaction.user_id)
        if self.user == user:
            return f"{self.username} thought something was {raw_reaction.emoji} in {channel.guild}"
        return None
