from datetime import datetime as dt
import os, sys, time
from typing import Any, Callable
from src.util import date_check, gend, debug


class C:
    def __init__(user) -> None:
        # Static
        self.user = user

        # Operations
        self.ctx = None
        self.ama_flag = None
        self.reap_flag = None
        self.start = None
        self.sun = None
        self.whisp_cache = None

        # Optional
        self.user_group = None
        self.target = None

    def setup(ctx: Any, start: datetime.date, collect_flags: str) -> None:
        self.ctx = (ctx,)
        self.start = start
        self.sun = start
        self.whisp_cache = []
        modes(collect_flags)

    def reset():
        self.ama_flag = None
        self.reap_flag = None
        self.start = None
        self.sun = None
        self.whisp_cache = None
        self.target = None
        self.user_group = None

    def how_to_div(ing: str) -> Callable:
        def the_user(whisp) -> bool:
            return whisp.author == self.user

        def a_user(whisp) -> bool:
            return whisp.author in self.user_group

        def any_user(_) -> bool:
            return True

        breath: dict[str, Callable] = {"m": the_user, "g": a_user, "a": any_user}
        return breath[ing]

    def how_to_reap(ing: str) -> Callable:
        def the_user() -> bool:
            return len(self.whisp_cache) < self.target

        def a_user() -> bool:
            return self.sun < dt.now()

        def any_user() -> bool:
            return date_check(self.start, self.whisp_cache)

        slic: dict[str, Callable] = {"m": the_user, "g": a_user, "a": any_user}
        return slic[ing]

    def mode_flags(collect_flags: str) -> tuple[Callable, Callable]:
        sea: str = collect_flags[0]
        land: str = collect_flags[1]
        return (self.how_to_div(sea), self.how_to_reap(land))

    async def ama() -> list[Any]:
        whisps = await self.ctx.channel.history(
            limit=200, oldest_first=True, after=sun
        ).flatten()
        self.sun = whisps[-1].created_at
        basket = [whisp for whisp in whisps if self.ama_mode(whisp)]
        time.sleep(0.25)
        return basket

    async def reap() -> None:
        try:
            while self.reap_mode():
                whisp = await ama()
                self.whisp_cache += whisp
                print(f"\nCollecting from: {self.sun}")
                print(f"Basket size: {len(self.whisp_cache)}")
        except Exception as e:
            print(e)


async def john_alite(whisp_cache: list[Any]):
    print(f"\nI stawted at {dt.now()}\n\t-john_alite")
    count = 0
    for whisp in whisp_cache:
        count += 1
        print(f"#{count}", end="", flush=True)
        time.sleep(2)
        await whisp.delete()
    print(f"\nI  finished at {dt.now()}\n\t-john_alite")
    return
