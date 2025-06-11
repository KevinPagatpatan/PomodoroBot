from pomodoro_model import PomodoroHandler, Pomodoro, PomodoroState, Timer, Context
from unittest.mock import MagicMock
import discord




def make_mock_ctx() -> Context:
    mock_ctx = MagicMock()
    mock_ctx.author = MagicMock(spec=discord.User)
    mock_ctx.channel = MagicMock(spec=discord.abc.Messageable)
    return mock_ctx

mock_user = make_mock_ctx()
print(mock_user.author)

test_handler = PomodoroHandler(Pomodoro, Timer)
test_pomodoro = Pomodoro(Timer)

def test_skip():
    assert test_pomodoro.state == PomodoroState.WORK
    test_pomodoro.skip()
    assert test_pomodoro.state == PomodoroState.STANDBY
    test_pomodoro.start_break