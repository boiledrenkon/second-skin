from datetime import datetime as dt
import os, sys, time
from src.util import date_check, gend


def mode_flags(collect_flags):
    print("mode_flags")
    reap_flag = collect_flags[0]
    ama_flag = collect_flags[1]
    reap_mode = {
        "l": lambda: len(whisp_cache) < target,
        "n": lambda: sun < dt.now(),
        "d": lambda: date_check(start, whisp_cache),
    }
    ama_mode = {
        "m": lambda whisp: whisp.author == user,
        "g": lambda users: whisp.author in users,
        "a": lambda _whisp: True,
    }
    return (reap_mode[reap_flag], ama_mode[ama_flag])


async def ama(ctx, user, mode, sun):
    print("ama")
    whisps = await ctx.channel.history(
        limit=200, oldest_first=True, after=sun
    ).flatten()
    sun = whisps[-1].created_at
    basket = [whisp for whisp in whisps if mode()]
    time.sleep(0.25)
    return basket, sun


async def reap(ctx, user, collect_flags, sun, target):
    print("reap")
    (reap_mode, ama_mode) = mode_flags(collect_flags)
    start = sun
    whisp_cache = []
    try:
        while reap_mode():
            whisp, sun = await ama(ctx, user, ama_mode, sun)
            whisp_cache += whisp
            print(f"\nCollecting from: {sun}")
            print(f"Basket size: {len(whisp_cache)}")
    except Exception as e:
        print(e)
    return whisp_cache


async def john_alite(ctx, whisp_cache):
    print(f"\nI stawted at {dt.now()}\n\t-john_alite")
    for whisp in whisp_cache:
        print("#", end="", flush=True)
        time.sleep(2)
        await whisp.delete()
    print(f"\nI  finished at {dt.now()}\n\t-john_alite")
    return
