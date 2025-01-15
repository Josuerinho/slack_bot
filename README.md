# Slack DM Bot

A simple Python bot for sending direct messages to users on Slack.

## Installation

1. Install the required package:
```bash
pip install sims-slack-bot
```

## Configuration

1. Load the config file I'll send to y'all through slack. That config file contains the bot token and also the users ID so you can be found by the bot. The file format is as follows (JSON):
```json
{
    "slack_token": "xoxb-your-bot-token",
    "users": {
        "username1": "U12345678",
        "username2": "U87654321"
    }
}
```

## Usage

```python
from sims_slack_bot import EnhancedSlackBot

# Initialize the bot with your config file
bot = EnhancedSlackBot('config.json')

# Send a DM using username from config
bot.send_dm(
    user_name="username1",
    message="Hello! This is a test message",
    emoji=":robot_face:"  # Optional, defaults to :robot_face:
)
```

## send_dm() Method Details

The `send_dm()` method allows you to send direct messages to Slack users in two ways:

### Parameters

- `user_name` (str): The username as defined in your config file
- `message` (str): The message content to send
- `emoji` (str, optional): Custom emoji to appear before the message. Defaults to ":robot_face:"
- `email` (str, optional): User's Slack email address (alternative to username)

### Features

- Messages are automatically formatted with timestamp and emoji
- Can identify users either by configured username or email address
- Provides error handling for invalid users or failed message delivery
- Prints confirmation when message is successfully sent

### Example Output Format

Your message will be formatted as:
```
🤖 *Bot Message* (2024-01-14 15:30:45)
Your message text here
```

## Error Handling

The method will raise a ValueError if:
- The specified username is not found in the config file
- The provided email doesn't correspond to a valid Slack user

## One-liner usage:

The package can also be run without stable installation. If you have `uv` installed, you can do the following:

```bash

uvx --from sims-slack-bot python -c 'from sims_slack_bot import EnhancedSlackBot;bot = EnhancedSlackBot("/Users/jc5737/config.json");bot.send_dm("user_name", "Hello World!")'

```

This will create a venv on the fly, download the required packages, install them and run the python. Once done, the venv will be deleted. Because all is done in Rust, it takes less than 2 seconds.

