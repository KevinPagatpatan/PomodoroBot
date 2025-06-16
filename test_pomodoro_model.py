from pomodoro_model import PomodoroHandler, Pomodoro, PomodoroState, Timer, Context, HandlerFeedback
from unittest.mock import MagicMock
import discord

def make_mock_ctx() -> Context:
    mock_ctx = MagicMock()
    mock_ctx.author = MagicMock(spec=discord.User)
    mock_ctx.channel = MagicMock(spec=discord.abc.Messageable)
    return mock_ctx

def test_set_pomodoro():
    user = make_mock_ctx()
    test_handler = PomodoroHandler(Pomodoro, Timer)

    assert test_handler.set_pomodoro(user) is HandlerFeedback.PASS
    assert test_handler.state(user) is PomodoroState.WORK
    assert test_handler.check_time_is_up() == []
    assert test_handler.check_inactive() == []

def test_not_validated():
    user1 = make_mock_ctx()
    user2 = make_mock_ctx()

    test_handler = PomodoroHandler(Pomodoro, Timer)

    test_handler.set_pomodoro(user1)
    assert test_handler.start(user1) is not HandlerFeedback.ERROR_UNKNOWN_USER
    assert test_handler.start(user2) is HandlerFeedback.ERROR_UNKNOWN_USER

    assert test_handler.state(user1) is not HandlerFeedback.ERROR_UNKNOWN_USER
    assert test_handler.state(user2) is HandlerFeedback.ERROR_UNKNOWN_USER

    assert test_handler.get_time_left(user1) is not HandlerFeedback.ERROR_UNKNOWN_USER
    assert test_handler.get_time_left(user2) is HandlerFeedback.ERROR_UNKNOWN_USER

    assert test_handler.skip(user1) is not HandlerFeedback.ERROR_UNKNOWN_USER
    assert test_handler.skip(user2) is HandlerFeedback.ERROR_UNKNOWN_USER

    assert test_handler.end(user1) is not HandlerFeedback.ERROR_UNKNOWN_USER
    assert test_handler.end(user2) is HandlerFeedback.ERROR_UNKNOWN_USER

def test_invalid_input():
    user = make_mock_ctx()
    test_handler = PomodoroHandler(Pomodoro, Timer)

    assert test_handler.set_pomodoro(user) is HandlerFeedback.PASS
    assert test_handler.set_pomodoro(user) is HandlerFeedback.ERROR_INVALID_INPUT

    assert test_handler.skip(user) is HandlerFeedback.PASS
    assert test_handler.skip(user) is HandlerFeedback.ERROR_INVALID_INPUT

    assert test_handler.start(user) is HandlerFeedback.PASS
    assert test_handler.start(user) is HandlerFeedback.ERROR_INVALID_INPUT

def test_states():
    user = make_mock_ctx()
    test_handler = PomodoroHandler(Pomodoro, Timer)

    test_handler.set_pomodoro(user)
    assert test_handler.state(user) is PomodoroState.WORK
    test_handler.skip(user)
    assert test_handler.state(user) is PomodoroState.STANDBY

    test_handler.start(user)
    assert test_handler.state(user) is PomodoroState.BREAK
    test_handler.skip(user)
    assert test_handler.state(user) is PomodoroState.STANDBY

    test_handler.start(user)
    assert test_handler.state(user) is PomodoroState.WORK
    test_handler.skip(user)
    assert test_handler.state(user) is PomodoroState.STANDBY

    test_handler.start(user)
    assert test_handler.state(user) is PomodoroState.BREAK
    test_handler.skip(user)
    assert test_handler.state(user) is PomodoroState.STANDBY

    test_handler.start(user)
    assert test_handler.state(user) is PomodoroState.WORK
    test_handler.skip(user)
    assert test_handler.state(user) is PomodoroState.STANDBY

    test_handler.start(user)
    assert test_handler.state(user) is PomodoroState.BREAK
    test_handler.skip(user)
    assert test_handler.state(user) is PomodoroState.STANDBY

    test_handler.start(user)
    assert test_handler.state(user) is PomodoroState.WORK
    test_handler.skip(user)
    assert test_handler.state(user) is PomodoroState.STANDBY

    test_handler.start(user)
    assert test_handler.state(user) is PomodoroState.LONG_BREAK
    test_handler.skip(user)
    assert test_handler.state(user) is PomodoroState.STANDBY


