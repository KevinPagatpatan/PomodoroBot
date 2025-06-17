
# PomodoroBot

Pomodoro bot for Discord

**PomodoroBot** is a Discord bot that helps you to stay productive by using the Pomodoro technique. This bot lets users create a Pomodoro session within a discord server. Whether you're studying or working, PomodoroBot keeps track of your work and break intervals directly within the server, helping work more organized and collaborative without ever leaving the server.


## Features
- Individual timers for each user
- Automatic pinging when timers are up
- Easy to set-up and start

## Commands

| Command        | Description                            |
|----------------|----------------------------------------|
| `!pomodoro`    | Initializes a Pomodoro session         |
| `!start`       | Starts the work or break timer         |
| `!skip`        | Skips the current timer                |
| `!tl`             | Displays remaining time                |
| `!finish`         | Ends the current Pomodoro session      |


## Installation

1. Clone the repository  
   ```bash
   git clone https://github.com/KevinPagatpatan/PomodoroBot.git
   cd pomodoro-bot

2. Install the necesary dependencies
    ```bash
    pip install -r requirements.txt
3. Make and install the Discord bot in your server ([link](https://discord.com/developers/docs/intro))
###### If you need help with this one you can follow this guide made by [TechWithTim](https://youtu.be/YD_N6Ffoojw?t=338)

4. Create a .env file
    ```ini
    DISCORD_TOKEN = [Your bot token here]
5. Run it 
    ```bash
    python main.py

## Running Tests

Make sure pytest is installed by running:

```bash
pip install pytest
```
Then run
```bash
pytest
```
## Feedback
Contributions and suggestions are **extremely** welcome! This is my first non-academic project and I would love to listen to all suggestions on how to improve :D


## FAQ

#### Can't I just install the bot in my server?
Sadly no, I have no way to have the bot running 24/7.

#### Can I copy paste the code and host the bot myself?

Yes I don't mind.

