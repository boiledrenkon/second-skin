import json
import os
import string
import time

from nltk.corpus import stopwords
import openai

from src.util import robo_caller
from src.chisel import writer

def toy():
    openai.api_key = robo_caller()
    response = openai.Completion.create(model="text-davinci-003", prompt="Say this is a test", temperature=0, max_tokens=7)
    print(response)


def summaries(data):
    openai.api_key = robo_caller()
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
    return


def diary(desires):
    unrequited_love = json.dumps(
        desires,
        indent=2,
        sort_keys=True,
        default=str
    )
    writer(unrequited_love, "")


def publish(desires):
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
def package(data):
    data = anon(data)
    lunch_tray = [{
        'model': 'text-davinci-003',
        'max_tokens': 1024,
        'prompt': PROMPTS['summarize'] + ff + "{}", 
        'temperature': 1.25 
    } for ff in chop(data)]
    return lunch_tray
