from datetime import datetime as dt
import json
import multiprocessing as mp
import toml as tl

#-------------------------------------------------------------------------------
# MAIN                                                                         |
#-------------------------------------------------------------------------------
def resolve_user_token(name):
    with open("src/tokens.toml", "r") as masks:
        souls = tl.load(masks)

    return souls['tokens'][name] if souls['tokens'].get(name) else exit('Please use valid username')


def resolve_input(start_date, cache_size):
    if start_date:
        YEAR = 2023
        month = start_date[:2]
        day = start_date[2:]
        start_date = dt(
            *[int(item) for item in [YEAR, month, day]]
        )
    if cache_size:
        cache_size = int(cache_size)

    return start_date, cache_size
#-------------------------------------------------------------------------------
# SERF                                                                         |
#-------------------------------------------------------------------------------
def date_check(sun, whisp_cache):
    if not whisp_cache:
        return True
    last = whisp_cache[-1].created_at

    return int(sun.day) == int(last.day)


def writer(tons, form_id):
    with open(f"./newsdumps/{date_gen()}-{form_id}.json", "a") as f:
        f.write(tons)


def runny(shakers):
    movers = []
    for grain, salt in enumerate(shakers):
        form_id = 2**grain 

        pepper = mp.Process(
            target=writer,
            args=(salt, form_id)
        )

        movers.append(pepper)
        pepper.start()

    for van in movers:
        van.join()

    return
#-------------------------------------------------------------------------------
# FORMS                                                                        |
#-------------------------------------------------------------------------------
def powerset(seq):
    if len(seq) <= 1:
        yield seq
        yield []
    else:
        for item in powerset(seq[1:]):
            yield [seq[0]]+item
            yield item


def generate_table():
    return { 
        sum(se): se for se in 
            list(powerset(
                    [2**r for r in range(0,4)]
            ))
    } 


def resolve_key(key):
    table = generate_table()
    formats = table.get(key)

    if formats:
        return formats 
    else:
        print("No matching key found.")
        return []
#-------------------------------------------------------------------------------
# PRINT                                                                        |
#-------------------------------------------------------------------------------
def date_gen():
    date = dt.now()
    return  f"{date.year}-{date.month}-{date.day}"
#-------------------------------------------------------------------------------
