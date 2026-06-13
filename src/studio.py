import json
import os
import string
import time
from typing import Any

from nltk.corpus import stopwords
import openai

from src.util import robo_caller
from src.chisel import writer

def toy():
    openai.api_key = robo_caller()["opa"]
    response = openai.Completion.create(model="text-davinci-003", prompt="Say this is a test", temperature=0, max_tokens=7)
    print(response)


def summaries(data: list[Any]) -> None:
    openai.api_key = robo_caller()["opa"]
    queries = package(data)
    print(len(queries))
    desires = []
    for desire in queries:
        print('trying')
        time.sleep(7)
        try:
            op = openai.Completion.create(model=desire['model'], prompt=desire['prompt'], temperature=desire['temperature'], max_tokens=desire['max_tokens'], stop=["{}"])
            desires.append(op)
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
    metangels = ""
    for unfinished in desires:
        if unfinished['choices'][0].get('text'):
            metangels +=  unfinished['choices'][0]['text']
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


def package(data, prompt: str = "summmarize") -> list[dict[str, Any]]:
    data = anon(data)
    lunch_tray = [{
        'model': 'text-davinci-003',
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
# NOTE: this path uses the openai>=1.0 client (OpenAI()), which is incompatible
# with the openai.Completion calls in summaries()/toy() above (those need
# openai<1.0). Imports are kept lazy so this module still loads either way; only
# the function you actually call needs its dependency present.
AUDIO_DIR = "/Users/Shared/programs/second-skin/outputs/audio/UncleJoe"
_audio_count = 0


def _reply_text(user: str, message: str) -> str:
    from openai import OpenAI

    client = OpenAI(api_key=robo_caller()["opa"])
    prompt = (
        f"Pretend you're in a deep conversation with {user}, on an online forum. "
        "You're secretly in love with them and you don't want to say it outloud. "
        "You show that you care by enganging with their interests. "
        f"Respond to their message: {message}" + "{}"
    )
    response = client.chat.completions.create(
        model="gpt-4o",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.8,
        max_tokens=1200,
        stop="{}",
    )
    return response.choices[0].message.content


def _speak(text: str, num: int) -> str:
    from elevenlabs import get_api_key, set_api_key, generate, save

    if get_api_key() is None:
        set_api_key(robo_caller()["eln"])
    audio = generate(
        text=f"{text}. and fuck you by the way!",
        voice="Uncle Joe",
        model="eleven_multilingual_v2",
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
