from textual.app import App, ComposeResult
from textual.widgets import Markdown, Header, Footer, Static, RichLog
from textual.binding import Binding
from rich import print

from instruct.gui.widgets.top_menu import TopMenu
from instruct.gui.widgets.result_viewer import ResultViewer
import pyperclip

from instruct.instruct import Instruct
import os

from textual.reactive import reactive

from textual import work

import time

import logging

logging.basicConfig(level=logging.ERROR)


class InstructApp(App):
    SAVED_FILE_EXT = ".md"

    CSS_PATH = "instruct_app.tcss"

    BINDINGS = [
        Binding(key="q", action="quit", description="Quit", show=True),
        Binding(
            key="c",
            action="copy_result",
            description="Copy to clipboard",
            show=True,
        ),
        Binding(key="r", action="reload", description="Reload", show=True),
        Binding(key="s", action="save", description="Save to file", show=True),
        Binding(
            key="l", action="toggle_log_view", description="Show/hide logs", show=True
        ),
    ]

    max_tokens = reactive(0)
    temperature = reactive(0)
    model = reactive("")

    content = reactive("")

    def __init__(
        self,
        instruct_file: Instruct,
        input,
        max_tokens: int,
        temperature: int,
        forced_model: str = None,
        **kwargs,
    ):
        super().__init__(**kwargs)
        self.instruct_file = instruct_file
        self.input = input
        self.max_tokens = max_tokens
        self.temperature = temperature
        self.forced_model = forced_model  # TODO implement this in instruct call

        self.first_token_reiceved = False
        self.instruct = Instruct(
            filepath=self.instruct_file, **self.input if self.input else {}
        )
        self.model = self.instruct.matching_model.name

    def compose(self) -> ComposeResult:
        yield TopMenu(
            id="top_menu",
        ).data_bind(InstructApp.model, InstructApp.max_tokens, InstructApp.temperature)

        yield RichLog(id="log")
        yield ResultViewer(id="result_viewer").data_bind(InstructApp.content)
        yield Footer()

    async def on_mount(self):
        self.title = "Instruct"
        self.sub_title = "Result Viewer"
        self.model = self.instruct.matching_model.name
        result_viewer = self.query_one("#result_viewer")
        result_viewer.styles.height = "9fr"
        result_viewer.styles.border = ("heavy", "white")
        rich_log = self.query_one("#log")
        rich_log.styles.height = "0fr"
        rich_log.styles.visibility = "hidden"

        await self.run_instruct()

    # @work(thread=True)
    async def run_instruct(self):
        try:
            self._write_to_log(
                f"Running instruct with model: {self.instruct.matching_model.model}"
            )
            self.call_run_instruct()
        except Exception as e:
            self.notify(f"Error running instruct: {e}", severity="error", title="Error")

    @work(thread=True)
    def call_run_instruct(self):
        self.query_one("#log").write("Running instruct...")
        self.query_one("#result_viewer").loading = True
        self.instruct.run(
            temperature=self.temperature,
            max_tokens=self.max_tokens,
            stream=True,
            stream_callback=lambda token: self.app.call_from_thread(
                self._token_received, token
            ),
        )

    def _token_received(self, token):
        try:
            self.content = token
            if self.content != "":
                self.query_one("#result_viewer").loading = False
            self.refresh(layout=True)
        except Exception as e:
            self.notify(f"Error updating content: {e}", severity="error", title="Error")

    def _write_to_log(self, message):
        self.query_one("#log").write(message)

    def action_copy_result(self):
        try:
            pyperclip.copy(self.content)
            self.notify(f"Copied to clipboard")
        except Exception as e:
            self.notify(
                f"Error copying to clipboard: {e}", severity="error", title="Error"
            )

    def action_reload(self):
        try:

            # Reload the instruct file from disk and re-run it
            self.instruct = Instruct(
                filepath=self.instruct_file, **self.input if self.input else {}
            )

            self.model = self.instruct.matching_model.name

            # clear log
            self.query_one("#log").clear()

            self.query_one("#result_viewer").loading = True
            self.call_after_refresh(self.run_instruct)
        except Exception as e:
            self.notify(
                f"Error reloading instruct: {e}", severity="error", title="Error"
            )

    def action_save(self):
        try:
            saved_file_path = self._get_saved_file_name(self.instruct_file)

            with open(saved_file_path, "w") as f:
                f.write(self.content)
            self.notify(f"File saved: [{saved_file_path}]({saved_file_path})")

        except Exception as e:
            self.notify(f"Error saving to file: {e}", severity="error", title="Error")

    def _get_saved_file_name(self, file_path):
        directory, base_name = os.path.split(file_path)
        base, _ = os.path.splitext(base_name)

        saved_file_ext = InstructApp.SAVED_FILE_EXT
        file_path = os.path.join(directory, base + saved_file_ext)

        if not os.path.exists(file_path):
            return file_path

        for version in range(
            1, 1_000_000
        ):  # Arbitrary large number to avoid infinite loop
            new_file_path = os.path.join(directory, f"{base}-{version}{saved_file_ext}")
            if not os.path.exists(new_file_path):
                return new_file_path

        raise RuntimeError(
            "Unable to find a non-existent file name after many attempts."
        )

    def action_toggle_log_view(self):
        rich_log = self.query_one("#log")
        current_visibility = rich_log.styles.visibility
        if current_visibility == "hidden":
            rich_log.styles.visibility = "visible"
            rich_log.styles.height = "1fr"
        else:
            rich_log.styles.visibility = "hidden"
            rich_log.styles.height = "0fr"


if __name__ == "__main__":
    app = InstructApp()
    app.run()
