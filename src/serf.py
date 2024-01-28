from datetime import datetime as dt
import os, sys, time
from typing import Any, Callable
from src.util import date_check, gend, debug


class Intern:
    def __init__(self, user: Any) -> None:
        # Static
        self.user = user

        # Operations
        self.ctx = None
        self.ama_mode = None
        self.reap_mode = None
        self.start = None
        self.sun = None
        self.whisp_cache = None

        # Optional
        self.user_group = None
        self.target = None

    def setup(
        self, ctx: Any, collect_flags: str, start: dt.date, target: int | None
    ) -> None:
        self.ctx = ctx
        self.start = start
        self.sun = start
        self.whisp_cache = []
        (a, r) = self.modes(collect_flags)
        self.ama_mode = a
        self.reap_mode = r

        self.target = target

    def reset(self):
        self.ama_mode = None
        self.reap_mode = None
        self.start = None
        self.sun = None
        self.whisp_cache = None
        self.target = None
        self.user_group = None

    def how_to_div(self, ing: str) -> Callable:
        def the_user(whisp) -> bool:
            return whisp.author == self.user

        def a_user(whisp) -> bool:
            return whisp.author in self.user_group

        def any_user(_) -> bool:
            return True

        breath: dict[str, Callable] = {"m": the_user, "g": a_user, "a": any_user}
        return breath[ing]

    def how_to_reap(self, ing: str) -> Callable:
        def some() -> bool:
            return len(self.whisp_cache) < self.target

        def alll() -> bool:
            return self.sun < dt.now()

        def day() -> bool:
            return date_check(self.start, self.whisp_cache)

        slic: dict[str, Callable] = {"k": some, "n": alll, "d": day}
        return slic[ing]

    def modes(self, collect_flags: str) -> tuple[Callable, Callable]:
        sea: str = collect_flags[0]
        land: str = collect_flags[1]
        return (self.how_to_div(sea), self.how_to_reap(land))

    async def ama(self) -> list[Any]:
        whisps = await self.ctx.channel.history(
            limit=200, oldest_first=True, after=self.sun
        ).flatten()
        self.sun = whisps[-1].created_at
        basket = [whisp for whisp in whisps if self.ama_mode(whisp)]
        time.sleep(0.25)
        return basket

    async def reap(self) -> None:
        try:
            while self.reap_mode():
                whisp = await self.ama()
                self.whisp_cache += whisp
                print(f"\nCollecting from: {self.sun}")
                print(f"Basket size: {len(self.whisp_cache)}")
        except Exception as e:
            print(e)


async def john_alite(whisp_cache: list[Any]):
    print(
        f"""
            I  stawted at {dt.now()}
            \t-john_alite
            """
    )
    count = 0
    for whisp in whisp_cache:
        count += 1
        print(f"#{count}", end="", flush=True)
        time.sleep(2)
        await whisp.delete()
    print(
        f"""\n
            I  finished at {dt.now()}
            \t-john_alite
            """
    )
    return
