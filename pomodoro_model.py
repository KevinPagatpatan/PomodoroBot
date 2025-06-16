from __future__ import annotations
import discord
from discord.ext import commands
from datetime import datetime, timedelta
from typing import Type
from enum import Enum, auto

class PomodoroState(Enum):
    WORK = auto()
    BREAK = auto()
    LONG_BREAK = auto()
    STANDBY = auto()

class HandlerFeedback(Enum):
    PASS = auto()
    ERROR_UNKNOWN_USER = auto()
    ERROR_INVALID_INPUT= auto()


Context = commands.Context[commands.Bot]
Author =  discord.Member | discord.User

class PomodoroHandler:
    def __init__(self, pomodoro: Type[Pomodoro], timer: Type[Timer]) -> None:
        self._timers: dict[Author, Pomodoro] = {}
        self._user_context: dict[Author, Context] = {}
        self._pomodoro: Type[Pomodoro] = pomodoro
        self._timer: Type[Timer] = timer

    def check_inactive(self) -> list[Context]:
        users: list[Context] = []
        keys = list(self._timers.keys())
        for k in keys[:]:
            if self._timers[k].inactive:
                users.append(self._user_context[k])
                self._timers.pop(k)
        return users

    def check_time_is_up(self) -> list[Context]:
        """Check if user's time is up"""
        users: list[Context] = []
        for k in self._timers.keys():
            if self._timers[k].time_is_up:
                users.append(self._user_context[k])
        return users

    def set_pomodoro(self, ctx: Context) -> HandlerFeedback:
        """Set a pomodoro for a user"""
        if self._validate(ctx):
            return HandlerFeedback.ERROR_INVALID_INPUT
        author: Author = ctx.author
        self._timers[author] = Pomodoro(self._timer)
        self._user_context[author] = ctx
        return HandlerFeedback.PASS

    def start(self, ctx: Context) -> HandlerFeedback:
        """Start a break or work"""
        if self._validate(ctx) is False:
            return HandlerFeedback.ERROR_UNKNOWN_USER
        elif self._timers[ctx.author].state is not PomodoroState.STANDBY:
            return HandlerFeedback.ERROR_INVALID_INPUT
        state: PomodoroState = self._timers[ctx.author].state_next
        if state is PomodoroState.BREAK:
            self._timers[ctx.author].start_break()
        else:
            self._timers[ctx.author].start_work()
        return HandlerFeedback.PASS
    
    def state(self, ctx: Context) -> PomodoroState | HandlerFeedback:
        """Return the user's pomodoro state"""
        if self._validate(ctx) is False:
            return HandlerFeedback.ERROR_UNKNOWN_USER
        return self._timers[ctx.author].state

    def get_time_left(self, ctx: Context) -> str | HandlerFeedback:
        """Return the user's remaining time"""
        if self._validate(ctx) is False:
            return HandlerFeedback.ERROR_UNKNOWN_USER
        return self._timers[ctx.author].time_left
        
    def skip(self, ctx: Context) -> HandlerFeedback:
        """Skip the user's current time"""
        if self._validate(ctx) is False:
            return HandlerFeedback.ERROR_UNKNOWN_USER
        elif self._timers[ctx.author].state is PomodoroState.STANDBY:
            return HandlerFeedback.ERROR_INVALID_INPUT
        self._timers[ctx.author].skip()
        return HandlerFeedback.PASS

    def end(self, ctx: Context) -> HandlerFeedback:
        """Remove user's pomodoro"""
        if self._validate(ctx) is False:
            return HandlerFeedback.ERROR_UNKNOWN_USER
        self._timers.pop(ctx.author)
        return HandlerFeedback.PASS

    def _validate(self, ctx: Context):
        """Check if user has a pomodoro"""
        return ctx.author in self._timers
    
    @property
    def len_timers(self) -> int:
        return len(self._timers)

class Pomodoro:
    def __init__(self, timer_obj: Type[Timer]) -> None:
        self._state: PomodoroState = PomodoroState.WORK
        self._state_next: PomodoroState = PomodoroState.BREAK
        self._work_counter: int = 1
        self._timer_obj: Type[Timer] = timer_obj
        self._timer: Timer = self._timer_obj(25)
        self._ping_counter: int = 0

    def start_work(self) -> None:
        self._ping_counter = 0
        if self._state != PomodoroState.STANDBY:
            return
        self._state_next = PomodoroState.BREAK
        self._state = PomodoroState.WORK
        self._timer = self._timer_obj(25)
        self._work_counter += 1
    
    def start_break(self) -> None:
        self._ping_counter = 0
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
            return "No pomodoro set (type !start to proceed with your pomodoro)"
        else:
            return  self._timer.time_left

    @property
    def time_is_up(self) -> bool:
        if self._timer.time_is_up:
            self._state = PomodoroState.STANDBY
            self._timer = Timer(1)
            self._ping_counter += 1
            return True
        return False
    
    @property
    def inactive(self) -> bool:
        return self._ping_counter >= 5


class Timer:
    def __init__(self, mins: int) -> None:
        now = datetime.now()
        self._time = now + timedelta(minutes= mins)
    
    @property
    def time_left(self) -> str:
        time: timedelta = self._time - datetime.now()
        secs: int = time.seconds
        return f"{secs//60} minutes and {secs%60} seconds left"
    
    @property
    def time_is_up(self) -> bool:
        return datetime.now() >= self._time

