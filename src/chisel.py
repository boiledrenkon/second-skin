import inspect
import os
import json
from random import random
import sys

from src.stone import form
from src.util import SIZE, gend, hardboiled, runny

def editor(whisp_cache, form_key):
    eggs = form(form_key, whisp_cache)
    runny(eggs, writer) if sys.getsizeof(eggs) > SIZE else hardboiled(eggs, writer)
    print("Write complete.")
    return eggs


PATH = "/Users/Shared/programs/cyborg/newsdumps/"
def writer(tons, form_id):
    json = ".json"
    txt = ".txt"
    mode = {
        "summaries": ("", json),
        "logs": (f"{form_id}", json),
        "publish": ("full", txt) 
    }
    gentleman = inspect.stack()[1][3]
    match mode[gentleman]:
        case "summaries":
            caller = "summaries"
        case "publish":
            caller = "publish"
        case _:
            caller = "logs"
    PATH =+ caller 
    path = os.path.join(PATH, space)
    with open(f"/{path}/{gend()}-{mode[caller][0]}-{random()[:8]}.{mode[caller][1}", "a") as f:
        f.write(tons)
    return
