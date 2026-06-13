# Second Skin

A personal Discord **self-bot** for archiving, summarizing, and deleting your own
message history. It logs into your account (not a bot account), scrapes channel
history into JSON/text exports, can bulk-delete your messages from a given date,
and uses OpenAI to summarize channel discussions.

> ⚠️ **Self-bots violate the [Discord Terms of Service](https://discord.com/terms)
> and can get your account banned.** This is a personal research tool. Use it on
> your own account, at your own risk.

## How it works

The bot runs on your account and listens for commands you type in any Discord
channel, prefixed with `¡` (inverted exclamation mark). You point it at a
**channel/server** and optionally a **target user**, then run collection or
deletion commands.

- **Collection (`note`)** — scrape messages from a start date forward and write
  them to disk as JSON.
- **Deletion (`delete`)** — scrape your matching messages and delete them one by
  one.
- **Summaries** — once a target user is set, incoming messages are batched and
  summarized with OpenAI, written to `scrolls/`.

## Requirements

- Python 3.10
- [`discord.py==1.7.3`](https://pypi.org/project/discord.py/1.7.3/) — the last
  release with self-bot support. **Do not upgrade to 2.x** (it removes
  `self_bot=True` / `client.run(token, bot=False)`).
- `aiohttp<3.8` (pinned by discord.py 1.7.3), `openai`, `nltk`, `toml`

```sh
pip install -r requirements.txt
```

## Configuration

Config files live in `src/` as TOML and are **git-ignored** where they hold
secrets.

`src/tokens.toml` — your account token(s) and API keys (never commit):

```toml
[tokens]
me = "your-discord-account-token"

[keys]
opa = "your-openai-api-key"
```

`src/servers.toml` — the channels/servers you operate in:

```toml
[servers.myserver]
id  = 123456789012345678   # guild (server) id
gen = 123456789012345678   # channel id to connect to
```

## Running

```sh
./run <username>
```

`<username>` is a key under `[tokens]` in `tokens.toml` (e.g. `./run me`). On
startup the bot prints `Online`; type commands in Discord from there.

## Commands

All commands are prefixed with `¡`.

| Command | Description |
| --- | --- |
| `¡set_channel <name>` | Connect to a server/channel defined in `servers.toml`. |
| `¡which_channel [l]` | Show current connection (`l` lists configured servers). |
| `¡reset_channel` | Disconnect. |
| `¡set_user <user_id>` | Set the target user to stalk/summarize. |
| `¡which_user` | Show the current target. |
| `¡reset_user` | Clear the target. |
| `¡sendto <text...>` | Send a message to the connected channel. |
| `¡note` / `¡nott <flags> <date> [n]` | Scrape & archive messages (see flags). |
| `¡delete` / `¡delet <flags> <date> [n]` | Scrape & delete matching messages. |
| `¡repeat <text>` | Spam a message in a loop (Ctrl-C to stop). |

`note`/`delete` are zero-arg shortcuts with built-in defaults; `nott`/`delet` are
the explicit forms that take flags, a `MMDDYYYY` start date, and an optional
count.

### Collection flags (`<scope><reap>`)

The first two characters of a collection command select **whose** messages and
**how far** to collect.

**Scope** (whose messages):

| Flag | Meaning |
| --- | --- |
| `m` | your messages only |
| `g` | a group of users *(not ready)* |
| `a` | all users |

**Reap** (when to stop):

| Flag | Meaning |
| --- | --- |
| `k` | until cache reaches the target count |
| `n` | up to today |
| `d` | a single day |

### Form / editor keys

Collection output can be serialized in several shapes. Keys are additive bit
flags (1/2/4/8) — sum them to emit multiple formats at once.

| Key | Output |
| --- | --- |
| `1` | `[msg]` — simple array of message bodies |
| `2` | `[full_msg_obj]` — full message objects |
| `4` | `{user/place/date/msg_id: msg}` |
| `8` | `{user/place/date/msg_id: full_msg_obj}` |

## Examples

```text
¡delete mn 01212024
```
Delete all *my* messages from 21 Jan 2024 up to today.

```text
¡note ad 01212024
```
Starting from 21 Jan 2024, archive *all* users' messages for that day as a
simple list.

## Output locations

- Scraped exports & summaries → `scrolls/` (and `newsdumps/`, git-ignored)
- Secrets → `src/tokens.toml` (git-ignored)

## Working notes / TODO

- Support a list of users in TOML (the `g` scope flag)
- Support operations without an active connection (supply a guild id directly)
- Support form/editor keys from the CLI
