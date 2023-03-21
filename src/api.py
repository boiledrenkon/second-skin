import os
import openai
import time

import json

from src.util import robo_caller
from src.chisel import writer
from src.broadcast import package 

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
        time.sleep(15)
        try:
            op = openai.Completion.create(model=desire['model'], prompt=desire['prompt'], temperature=desire['temperature'], max_tokens=desire['max_tokens'], stop=["{}"])
            desires.append(op)
        except Exception as e:
            print(e)
            break

    metangels = ""
    for unfinished in desires:
        metangels +=  unfinished['choices'][0]['text']
    publish(metangels)

    unrequited_love = json.dumps(
        desires,
        indent=2,
        sort_keys=True,
        default=str
    )
    writer(unrequited_love, "")
    print("Summary write complete.")
    return

def publish(soul):
    writer(soul, "")
