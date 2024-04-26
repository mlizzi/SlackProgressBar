
# slack-progress-bar [![Downloads](https://static.pepy.tech/badge/slack-progress-bar)](https://pepy.tech/project/slack-progress-bar)
A Python library for adding a progress bar to a Slack Bot, updated for Python 3.9+.

![animated-gif](https://imgur.com/WkC70eR.gif)

## Installation
```bash
pip install slack-progress-bar
```

## Overview
- The `SlackProgressBar` enables progress bars to be sent to users of a Slack Workspace. 
- Instantiating or updating a `SlackProgressBar` will send a message to the `user_id` from the bot 
via private message.
- To create another progress bar on Slack, instantiate a new instance of `SlackProgressBar`.
- Make use of the `SlackProgressBar.notify` property to turn on / off message sending as desired.


## Tutorial
1. Create a new Slack app for your workspace with the [Slack Apps API](https://api.slack.com/apps) and clicking `Create New App`. Follow the prompts to create a new app from scratch.
2. Go to `Features -> OAuth & Permissions` and add the following scopes to the `Bot Token Scopes`:  `chat:write`, `channels:manage`, `groups:write`, `im:write`, `mpim:write`.
3. Go to `Settings -> Install App` and press `Install to Workspace`. Press `Allow`.
4. On the same page, copy the generated `Bot User OAuth Token`, and use it for the `token` field of the `SlackProgressBar` class.
5. Head to you Slack Workspace and find your member ID (Found by clicking your profile and clicking `[...] -> Copy Member ID`) and use it for the `user_id` field of the `SlackProgressBar` class.
6. Use the `token` and `user_id` found above to create the progress bar and update it as follows:
```python
import os
import time
from slack_progress_bar import SlackProgressBar

BOT_TOKEN = os.getenv("BOT_TOKEN")
SLACK_MEMBER_ID = os.getenv("SLACK_MEMBER_ID")

# Creates a progress bar on Slack (use `notify=False` to prevent messages)
progress_bar = SlackProgressBar(token=BOT_TOKEN, user_id=SLACK_MEMBER_ID, total=150)

# Update the progress bar as progress is being made
for i in range(150):
    try:
        # Insert work here...
        time.sleep(0.1)
        
        # Update
        progress_bar.update(i+1)
        
    except Exception:
        progress_bar.error()
```