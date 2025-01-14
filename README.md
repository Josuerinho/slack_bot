# Slack DM Bot

A simple Python bot for sending direct messages to users on Slack.

## Installation

1. Install the required package:
```bash
pip install slack-sdk
```

## Configuration

1. Create a JSON configuration file (e.g., `config.json`) with the following structure:
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
from slack_bot import EnhancedSlackBot

# Initialize the bot with your config file
bot = EnhancedSlackBot('config.json')

# Send a DM using username from config
bot.send_dm(
    user_name="username1",
    message="Hello! This is a test message",
    emoji=":robot_face:"  # Optional, defaults to :robot_face:
)

# Or send a DM using email address
bot.send_dm(
    user_name=None,
    message="Hello! This is a test message",
    emoji=":star:",  # Optional
    email="user@organization.com"
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
