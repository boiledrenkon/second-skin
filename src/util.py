from datetime import datetime as dt
from inspect import iscoroutinefunction
from functools import wraps
import multiprocessing as mp
import toml as tl


# -------------------------------------------------------------------------------
# GENERAL                                                                      |
# -------------------------------------------------------------------------------
def open_toml():
    with open("src/tokens.toml", "r") as masks:
        souls = tl.load(masks)
    return souls


# -------------------------------------------------------------------------------
# MAIN                                                                         |
# -------------------------------------------------------------------------------
def resolve_user_token(name):
    souls = open_toml()
    return (
        souls["tokens"][name]
        if souls["tokens"].get(name)
        else exit("Please use valid username")
    )


def resolve_input(start_date, cache_size):
    if start_date:
        month = start_date[:2]
        day = start_date[2:4]
        year = start_date[4:]
        date = [year, month, day]

        start_date = dt(*[int(item) for item in date])
    if cache_size:
        cache_size = int(cache_size)
    return start_date, cache_size


# -------------------------------------------------------------------------------
# SERF/STONE                                                                   |
# -------------------------------------------------------------------------------
SIZE = 2097152


def date_check(sun, whisp_cache):
    if not whisp_cache:
        return True
    last = whisp_cache[-1].created_at
    print(sun)
    print(last)
    return int(sun.day) == int(last.day)


def runny(shakers, pan):
    movers = []
    for grain, salt in enumerate(shakers):
        form_id = 2**grain
        pepper = mp.Process(target=pan, args=(salt, form_id))
        movers.append(pepper)
        pepper.start()
    for van in movers:
        van.join()
    return


def hardboiled(shakers, pan):
    for grain, salt in enumerate(shakers):
        form_id = 2**grain
        pan(salt, form_id)
    return


# -------------------------------------------------------------------------------
# FORMS                                                                        |
# -------------------------------------------------------------------------------
def powerset(seq):
    if len(seq) <= 1:
        yield seq
        yield []
    else:
        for item in powerset(seq[1:]):
            yield [seq[0]] + item
            yield item


def generate_table():
    return {sum(se): se for se in list(powerset([2**r for r in range(0, 4)]))}


def resolve_key(key):
    table = generate_table()
    formats = table.get(key)
    if formats:
        return formats
    else:
        print("No matching key found.")
        return []


# -------------------------------------------------------------------------------
# PRINT                                                                        |
# -------------------------------------------------------------------------------
def gend():
    date = dt.now()
    return f"{date.day}-{date.month}-{date.year}"


def debug(func):
    @wraps(func)
    def ray(*args, **kwargs):
        print(f"Calling {func.__name__} with {args}, {kwargs}")
        result = func(*args, **kwargs)
        print(f"exiting {func.__name__}")
        return result

    @wraps(func)
    async def peat(*args, **kwargs):
        print(f"Calling {func.__name__} with {args}, {kwargs}")
        result = await func(*args, **kwargs)
        print(f"exiting {func.__name__}")
        return result

    return peat if iscoroutinefunction(func) else ray


# -------------------------------------------------------------------------------
# BROADCAST                                                                    |
# -------------------------------------------------------------------------------
def robo_caller():
    souls = open_toml()
    return souls["keys"]["opa"]
