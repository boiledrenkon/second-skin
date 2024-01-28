# Eris Cyborg

## Ama flags:
- m: user
- g: in users (not ready)
- a: all

## Reap flags:
- k: cache < target
- n: up to today
- d: one day

## Editor keys:
- 1: [msg]
- 2: [full_msg_obj]
- 4: {'user/place/date/msg_id: msg}
- 8: {'user/place/date/msg_id: full_msg_obj}

## Examples:
™delete mn 01212024<br>
delete all my messages from 21 Jan 2024 til no

™note ad 01212024<br>
starting from 21 Jan 2024 write all users messages in simple list

### Working Notes:
- Support list of users in toml
- Support operations without context (supplying guild id)
- Support use of editor keys on cli
