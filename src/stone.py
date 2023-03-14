import json
from src.format import form
from src.util import SIZE, runny, hardboiled

def editor(whisp_cache, form_key):
    eggs = form(form_key, whisp_cache)
    runny(eggs, writer) if sys.getsizeof(eggs) > SIZE else hardboiled(eggs, writer)
    print("Write complete.")
    return 


def writer(tons, form_id):
    with open(f"./newsdumps/{date_gen()}-{form_id}.json", "a") as f:
        f.write(tons)
    return
