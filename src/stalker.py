from typing import Any, Generator

MESSAGE_MIN = 6
SUMMARY_COUNT = 50


class Guild:
    def __init__(self, guild_id):
        self.guild_id: str = guild_id
        self.messages: list[Any] = []
        self.messages_len: int = 0

    def _is_valid_message(self, message) -> bool:
        tokens: list[str] = message.split(" ")
        return False if len(tokens) < MESSAGE_MIN else True

    def add_message(self, message) -> bool:
        if self._is_valid_message(message):
            self.messages += message
            self.messages_len += 1
            return True
        return False

    def empty_messages(self) -> None:
        self.messages = []
        self.messages_len = 0


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

    def _add_message(self, guild, message):
        added: bool = guild.add_messsage(message)
        count: int = guild.messages_len

        messages: str = ""
        if added and count == SUMMARY_COUNT:
            messages: str = " ".join(guild.messages)
            guild.empty_messages()
        return messages

    def on_message(self, message) -> tuple[bool, list[Any], Guild | None]:
        if not self.user == message.author:
            return

        guild_id: str = message.guild.id
        guild: Guild = self._get_guild(guild_id)
        messages = self._add_message(guild, message)

    def on_react(self, reaction, user) -> str:
        message = reaction.message
        if self.user == user:
            return f"{self.username} thought something was {reaction.emoji} in {message.guild}"

    async def on_raw_react(self, raw_reaction: Any, client: Any) -> str | None:
        if raw_reaction.event_type == "REACTION_ADD":
            channel = await client.fetch_channel(raw_reaction.channel_id)
            user = await client.fetch_user(raw_reaction.user_id)
        if self.user == user:
            return f"{self.username} thought something was {raw_reaction.emoji} in {channel.guild}"
        else:
            return None
