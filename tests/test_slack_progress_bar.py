from unittest.mock import patch

import pytest
from slack_sdk.errors import SlackApiError

from slack_progress_bar import SlackProgressBar


@patch("slack_progress_bar.slack_progress_bar.WebClient")
def test_slack_progress_bar(MockClient):

    # Adjust params for the mock web client to test
    mock_web_client = MockClient.return_value
    mock_web_client.conversations_open.return_value = {"channel": {"id": "10"}}
    mock_web_client.chat_postMessage.return_value = {"ts": "0001"}
    mock_web_client.chat_update.return_value = {"ok": True}

    # Test initialization
    pb = SlackProgressBar("FAKE_TOKEN", "FAKE_USER", 100)
    assert pb._ts == "0001"
    assert pb._channel_id == "10"

    # Test update
    pb.update(10)
    assert pb._value == 10
    pb._client.chat_update.assert_called_with(
        channel=pb._channel_id,
        ts=pb._ts,
        text=pb._as_string(),
    )

    # Test notify off during initialization
    pb = SlackProgressBar("FAKE_TOKEN", "FAKE_USER", 100, notify=False)
    assert pb._ts is None

    # Test turning notify on after initialization
    pb.notify = True
    assert pb._ts is None
    pb.update(10)
    assert pb._ts == "0001"

    # Test too large of a update value
    with pytest.raises(ValueError):
        pb.update(101)

    # Test bar is complete
    pb.update(100)
    pb._client.chat_update.assert_called_with(
        channel=pb._channel_id,
        ts=pb._ts,
        text=pb._as_string() + " :white_check_mark: Loading complete!",
    )

    # Test error method
    pb.error()
    pb._client.chat_update.assert_called_with(
        channel=pb._channel_id,
        ts=pb._ts,
        text=pb._as_string() + " :warning: ERROR: Loading stopped!",
    )

    # Test invalid user_id
    data = {
        "ok": False,
        "error": "invalid_auth",
    }
    mock_web_client.conversations_open.return_value = data
    mock_web_client.conversations_open.side_effect = SlackApiError(
        "The request to the Slack API failed. (url: https://www.slack.com/api/conversations.open)",
        data,
    )
    with pytest.raises(ValueError):
        pb = SlackProgressBar("FAKE_TOKEN", "FAKE_USER", 100)
