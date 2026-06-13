import json
import os
import string
import time
from typing import Any

from nltk.corpus import stopwords

from src.util import BASE_DIR, robo_caller
from src.llm import complete
from src.chisel import writer

def toy():
    print(complete(prompt="Say this is a test", role="summarize", max_tokens=8))


def summaries(data: list[Any]) -> None:
    queries = package(data)
    print(len(queries))
    desires = []
    for desire in queries:
        print('trying')
        time.sleep(7)
        try:
            text = complete(
                prompt=desire['prompt'],
                role="summarize",
                temperature=desire['temperature'],
                max_tokens=desire['max_tokens'],
                stop=["{}"],
            )
            desires.append(text)
        except Exception as e:
            print(e)
            break
    diary(desires)
    publish(desires)
    print("Summary write complete.")


def diary(desires) -> None:
    inactions = json.dumps(
        desires,
        indent=2,
        sort_keys=True,
        default=str
    )
    writer(inactions, "")


def publish(desires) -> None:
    metangels = "\n\n".join(text for text in desires if text)
    writer(metangels.strip(), "")
#-------------------------------------------------------------------------------
# 
#-------------------------------------------------------------------------------
MSG_OVER = 800
MSG_UNDER = 30
ROBO_LIMIT = 8400
STOP_WORDS = stopwords.words('english')

def anon(data):
    if type(data) == dict:
        data = data.values()
    return data


def sift(node):
    area = node['content']
    squatter = node['name']
    side = len(area)
    if side < MSG_UNDER or side > MSG_OVER or 'http' in area:
        return None
    area = "".join([block for block in area if block not in string.punctuation and block not in "0123456789"])
    area = " ".join([a for a in area.split(" ") if a not in STOP_WORDS])
    biscuit = f"{squatter}@{area}"
    return biscuit


def chop(ginger):
    counter = 0
    loads = []
    mainload = ""
    print(ginger)
    for node in ginger:
        valid = sift(node)
        if not valid:
            continue
        if counter >= ROBO_LIMIT:
            loads.append(mainload)
            mainload = valid
            counter = len(mainload)
        else:
            mainload = mainload + ". " + valid
            counter = len(mainload)
    mainload = mainload[:MSG_OVER]
    loads.append(mainload)
    return loads


PROMPTS = {
    'summarize': 'Given the following  sequence of messages with usernames delimited by an @ symbol,  summarize the discussion and add some context to any popular topics: ',
    'story': 'Given the following sequence of messages, write a short story about the themes and actions discussed in the style of Ryunosuke Akutagawa: ',
}


def package(data, prompt: str = "summarize") -> list[dict[str, Any]]:
    data = anon(data)
    lunch_tray = [{
        'max_tokens': 1024,
        'prompt': PROMPTS[prompt] + ff + "{}",
        'temperature': 1.25
    } for ff in chop(data)]
    return lunch_tray


# -------------------------------------------------------------------------------
# AUDIO REPLY  (GPT-4o text -> ElevenLabs TTS)
# -------------------------------------------------------------------------------
# Triggered when you react 👴 to a message: compose a reply with GPT-4o, speak it
# in the "Uncle Joe" voice, and return the path to the saved mp3.
#
# The text reply goes through the shared complete() wrapper (role "reply"), so
# the model/provider is set in models.toml. The TTS step below is a separate
# concern (audio, not an LLM) and keeps its own voice/model settings.
AUDIO_DIR = os.path.join(BASE_DIR, "outputs", "audio", "UncleJoe")
TTS_VOICE = "Uncle Joe"
TTS_MODEL = "eleven_multilingual_v2"
_audio_count = 0


def _reply_text(user: str, message: str) -> str:
    prompt = (
        f"Pretend you're in a deep conversation with {user}, on an online forum. "
        "You're secretly in love with them and you don't want to say it outloud. "
        "You show that you care by enganging with their interests. "
        f"Respond to their message: {message}" + "{}"
    )
    return complete(
        prompt=prompt,
        role="reply",
        temperature=0.8,
        max_tokens=1200,
        stop="{}",
    )


def _speak(text: str, num: int) -> str:
    from elevenlabs import get_api_key, set_api_key, generate, save

    if get_api_key() is None:
        set_api_key(robo_caller()["eln"])
    audio = generate(
        text=f"{text}. and fuck you by the way!",
        voice=TTS_VOICE,
        model=TTS_MODEL,
    )
    os.makedirs(AUDIO_DIR, exist_ok=True)
    path = f"{AUDIO_DIR}/{num}.mp3"
    save(audio, path)
    return path


def go(user: str, message: str) -> str:
    global _audio_count
    text = _reply_text(user, message)
    path = _speak(text, _audio_count)
    _audio_count += 1
    return path
