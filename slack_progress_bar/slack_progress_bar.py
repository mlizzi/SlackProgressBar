from slack_sdk import WebClient
from slack_sdk.errors import SlackApiError


class SlackProgressBar:

    def __init__(
        self,
        token: str,
        user_id: str,
        total: int,
        value: int = 0,
        bar_width: int = 20,
    ) -> None:
        """A progress bar to use with Slack.

        Parameters
        ----------
        token
            The SlackBot token.
        user_id
            The user id of the Slack account to send messages to.
        total
            The total length of the progress bar.
        value
            The initial value of the progress bar.
        bar_width
            The width of the progress bar as seen on Slack.
        """
        self._client = WebClient(token=token)
        self._total = total
        self._bar_width = bar_width
        self._value = value

        # Get channel id of user conversation (for posting and updating)
        try:
            res = self._client.conversations_open(users=user_id)
            self._channel_id = res["channel"]["id"]
        except SlackApiError:
            ValueError("Enter valid user id (Slack Profile -> Copy member ID")

        res = self._client.chat_postMessage(
            channel=self._channel_id, text=self._as_string()
        )

        self._ts = res["ts"]

    def update(self, value: int) -> None:
        """Update the current progress bar on Slack.

        Parameters
        ----------
        value
            The value to update the progress bar with.
        """
        if value > self._total:
            raise ValueError(
                f"Update value {value} too large for progress bar "
                f"of size {self._total}"
            )

        self._value = value

        message = (
            ":white_check_mark: Loading complete!"
            if self._value == self._total
            else ""
        )

        self._client.chat_update(
            channel=self._channel_id,
            ts=self._ts,
            text=self._as_string(message),
        )

    def error(self) -> None:
        """Set the bar to an error state to indicate loading has stopped."""
        self._client.chat_update(
            channel=self._channel_id,
            ts=self._ts,
            text=self._as_string(message=":warning: ERROR: Loading stopped!"),
        )

    def _as_string(self, message: str = "") -> str:
        """Get the progress bar visualized as a string.

        Parameters
        ----------
        message
            A message to include alongside the progress bar.

        Returns
        -------
        str
            The string representation of the error bar.
        """
        amount_complete = round(self._bar_width * self._value / self._total)
        amount_incomplete = self._bar_width - amount_complete
        bar = amount_complete * chr(9608) + amount_incomplete * chr(9601)

        return (
            f"{bar} {self._value}/{self._total} "
            f"({int(self._value / self._total * 100)}%) "
            f"{message}"
        )
