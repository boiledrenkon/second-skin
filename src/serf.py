from datetime import datetime as dt
import os, sys, time
from src.format import form
from src.util import date_check, date_gen, SIZE, runny, hardboiled

async def ama(ctx, user, flag, sun):
    mode = {
        'm': lambda whisp : whisp.author == user,
        'g': lambda users : whisp.author in users,
        'a': lambda _whisp : True,
    }
    whisps = await ctx.channel.history(limit=200, oldest_first=True, after=sun).flatten()
    sun = whisps[-1].created_at
    basket = [whisp for whisp in whisps if mode[flag](whisp)]
    time.sleep(.25)
    return basket, sun


async def reap(ctx, user, collect_flags, sun, target):
    reap_flag = collect_flags[0]
    ama_flag = collect_flags[1]
    start = sun
    whisp_cache = []
    mode = {
        'l': lambda: len(whisp_cache) < target,
        'n': lambda: sun < dt.now(),
        'd': lambda: date_check(start, whisp_cache) 
    }
    try:
        while mode[reap_flag]():
            whisp, sun = await ama(ctx, user, ama_flag, sun)
            whisp_cache += whisp 
            print(f"\nCollecting from: {sun}")
            print(f"Basket size: {len(whisp_cache)}")
    except Exception as e:
        print(e)
    return whisp_cache


async def john_alite(ctx, whisp_cache):
    print(f"\nI stawted at {dt.now()}")
    print("\t-john_alite")
    for whisp in whisp_cache:
        print("#", end="", flush=True)
        time.sleep(2)
        await whisp.delete()
    print(f"\nI  finished at {dt.now()}")
    print("\t-john_alite")
    return


def people(whisp_cache, threshold=0):
    group = {
        whisp.author.name: whisp.author.name.append(whisp) or [whisp]
        for whisp in whisp_cache
    }
    dictionary = {
        author: len(messages)
        for author, messages in group
        if len(messages) > threshold
    }
    print(list(dictionary.keys()))
    return


def editor(whisp_cache, form_key):
    eggs = form(form_key, whisp_cache)
    runny(eggs) if sys.getsizeof(eggs) > SIZE else hardboiled(eggs)
    print("Write complete.")
    return 
