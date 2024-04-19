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
        notify: bool = True,
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
        notify
            If the progress bar will send a message on Slack. Can be used
            to disable or enable message sending.
        """
        self._client = WebClient(token=token)
        self._total = total
        self._value = value
        self._bar_width = bar_width
        self._ts = None

        self.notify = notify

        # Get channel id of user conversation (for posting and updating)
        try:
            res = self._client.conversations_open(users=user_id)
            self._channel_id = res["channel"]["id"]
        except SlackApiError:
            raise ValueError(
                "Enter valid user_id (Slack Profile -> Copy member ID) or check token!"
            )

        if self.notify:
            self._chat_update()

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

        self._chat_update(
            message=(
                ":white_check_mark: Loading complete!"
                if self._value == self._total
                else ""
            )
        )

    def error(self) -> None:
        """Set the bar to an error state to indicate loading has stopped."""
        self._chat_update(message=":warning: ERROR: Loading stopped!")

    def _chat_update(self, message: str = "") -> None:
        """Send the progress bar with a message to Slack if notify is True.

        Parameters
        ----------
        message
            A message to include alongside the progress bar.
        """
        if self.notify:

            if message:
                text = self._as_string() + f" {message}"
            else:
                text = self._as_string()

            if not self._ts:
                res = self._client.chat_postMessage(
                    channel=self._channel_id, text=text
                )
                self._ts = res["ts"]
            else:
                self._client.chat_update(
                    channel=self._channel_id,
                    ts=self._ts,
                    text=text,
                )

    def _as_string(self) -> str:
        """Get the progress bar visualized as a string.

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
            f"({int(self._value / self._total * 100)}%)"
        )
