from __future__ import annotations
import discord
import discord.abc
from discord.ext import commands
from datetime import datetime, timedelta
from typing import Type
from enum import Enum, auto

class PomodoroState(Enum):
    WORK = auto()
    BREAK = auto()
    LONG_BREAK = auto()
    STANDBY = auto()

Context = commands.Context[commands.Bot]
Author =  discord.Member | discord.User

class PomodoroHandler:
    def __init__(self, pomodoro: Type[Pomodoro], timer: Type[Timer]) -> None:
        self._timers: dict[Author, Pomodoro] = {}
        self._user_channels: dict[Author, discord.abc.Messageable] = {}
        self._pomodoro: Type[Pomodoro] = pomodoro
        self._timer: Type[Timer] = timer

    def validate(self, ctx: Context):
        return ctx.author in self._timers

    def set_pomodoro(self, ctx: Context) -> None:
        author: Author = ctx.author
        self._timers[author] = Pomodoro(self._timer)
        self._user_channels[author] = ctx.channel
    
    def check_time_is_up(self) -> list[discord.abc.Messageable]:
        users: list[discord.abc.Messageable] = []
        for k in self._timers.keys():
            if self._timers[k].time_is_up:
                users.append(self._user_channels[k])
        return users

    def start(self, ctx: Context) -> None:
        state: PomodoroState = self._timers[ctx.author].state_next
        if state is PomodoroState.BREAK:
            self._timers[ctx.author].start_break()
        else:
            self._timers[ctx.author].start_work()
    
    def state(self, ctx: Context) -> PomodoroState:
        return self._timers[ctx.author].state

    def get_time_left(self, ctx: Context) -> str:
        return self._timers[ctx.author].time_left
    
    def skip(self, ctx: Context) -> None:
        self._timers[ctx.author].skip()

    def end(self, ctx: Context) -> None:
        self._timers.pop(ctx.author)
    

class Pomodoro:
    def __init__(self, timer_obj: Type[Timer]) -> None:
        self._state: PomodoroState = PomodoroState.WORK
        self._state_next: PomodoroState = PomodoroState.BREAK
        self._work_counter: int = 1
        self._timer_obj: Type[Timer] = timer_obj
        self._timer: Timer = self._timer_obj(25)

    def start_work(self) -> None:
        if self._state != PomodoroState.STANDBY:
            return
        self._state_next = PomodoroState.BREAK
        self._state = PomodoroState.WORK
        self._timer = self._timer_obj(25)
        self._work_counter += 1
    
    def start_break(self) -> None:
        if self._state != PomodoroState.STANDBY:
            return
        self._state_next = PomodoroState.WORK
        if self._work_counter % 4 == 0:
            self._timer = self._timer_obj(15)
            self._state = PomodoroState.LONG_BREAK
        else:
            self._timer = self._timer_obj(5)
            self._state = PomodoroState.BREAK
    
    def skip(self) -> None:
        self._timer = Timer(1)
        self._state = PomodoroState.STANDBY

    @property
    def state(self) -> PomodoroState:
        return self._state

    @property
    def state_next(self) -> PomodoroState:
        return self._state_next

    @property
    def time_left(self) -> str:
        if self._state == PomodoroState.STANDBY:
            return "No pomodoro set"
        else:
            return  self._timer.time

    @property
    def time(self) -> str:
        if self._state == PomodoroState.STANDBY:
            return "No pomodoro set"
        else:
            return  self._timer.time

    @property
    def time_is_up(self) -> bool:
        if self._timer.time_is_up:
            self._state = PomodoroState.STANDBY
            self._timer = Timer(1)
            return True
        return False


class Timer:
    def __init__(self, mins: int) -> None:
        self._time = datetime.now() + timedelta(minutes= mins)
    
    @property
    def time_left(self) -> str:
        time: timedelta = self._time - datetime.now()
        return f"{time} left"
    
    @property
    def time_is_up(self) -> bool:
        return datetime.now() >= self._time

    @property
    def time(self) -> str:
        return f"Pomodoro will alarm in {self._time.hour}:{self._time.minute}:{self._time.second}"
    
