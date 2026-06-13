from datetime import datetime as dt
import os, sys, time
from typing import Optional, Any, Callable
from src.util import date_check, gend, debug


class Intern:
    def __init__(self, user: Any) -> None:
        self.whisp_cache = None

        # Static
        self._user = user

        # Operations
        self._channe = None
        self._ama_cb = None
        self._reap_cb = None
        self._start = None
        self._sun = None

        # Optional
        self._user_group = None  # TODO
        self._target = None

    def setup(
        self, collect_flags: str, channel: Any, start: dt.date, target: int | None
    ) -> None:
        self.whisp_cache = []

        self._channel = channel
        self._start = start
        self._sun = start
        self._set_modes(collect_flags)
        self._target = target

    def reset(self):
        self.whisp_cache = None

        self._ama_cb = None
        self._reap_cb = None
        self._start = None
        self._sun = None
        self._target = None
        self._user_group = None

    def _how_to_div(self, ing: str) -> Callable:
        def the_user(whisp) -> bool:
            return whisp.author == self._user

        def a_user(whisp) -> bool:
            return whisp.author in self._user_group

        def any_user(_) -> bool:
            return True

        breath: dict[str, Callable] = {"m": the_user, "g": a_user, "a": any_user}
        return breath[ing]

    def _how_to_reap(self, ing: str) -> Callable:
        def some() -> bool:
            return len(self.whisp_cache) < self._target

        def alll() -> bool:
            return self._sun < dt.now()

        def day() -> bool:
            return date_check(self._start, self.whisp_cache)

        slic: dict[str, Callable] = {"k": some, "n": alll, "d": day}
        return slic[ing]

    def _set_modes(self, collect_flags: str) -> None:
        sea: str = collect_flags[0]
        land: str = collect_flags[1]
        self._ama_cb = self._how_to_div(sea)
        self._reap_cb = self._how_to_reap(land)

    async def ama(self) -> list[Any]:
        whisps = await self._channel.history(
            limit=200, oldest_first=True, after=self._sun
        ).flatten()
        self._sun = whisps[-1].created_at
        basket = [whisp for whisp in whisps if self._ama_cb(whisp)]
        time.sleep(0.25)
        return basket

    async def reap(self) -> None:
        try:
            while self._reap_cb():
                whisp = await self._ama()
                self.whisp_cache += whisp
                print(f"\nCollecting from: {self._sun}")
                print(f"Basket size: {len(self.whisp_cache)}")
        except Exception as e:
            print(e)

    async def shred(self):
        print(
            f"""
                I  stawted at {dt.now()}
                \t-john_alite
                """
        )
        count = 0
        for whisp in self.whisp_cache:
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
