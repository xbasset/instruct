from textual.app import App, ComposeResult
from textual.widgets import Markdown, Header, Footer, Static
from textual.binding import Binding
from rich import print

from instruct.gui.widgets.top_menu import TopMenu
from instruct.gui.widgets.result_viewer import ResultViewer
import pyperclip

from instruct.instruct import Instruct
import os

from textual.reactive import reactive

from textual import work


class InstructLayout(App):
    SAVED_FILE_EXT = ".md"

    CSS_PATH = "layout.tcss"

    BINDINGS = [
        Binding(key="q", action="quit", description="Quit the app"),
        Binding(
            key="question_mark",
            action="help",
            description="Show help screen",
            key_display="?",
        ),
        Binding(
            key="c",
            action="copy_result",
            description="Copy content to clipboard",
            show=True,
        ),
        Binding(key="r", action="reload", description="Reload the instruct", show=True),
        Binding(
            key="s", action="save", description="Save result to .md file", show=True
        ),
    ]

    max_tokens = reactive(1000)
    temperature = reactive(0.7)
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

    def compose(self) -> ComposeResult:
        yield Header(show_clock=False)
        yield TopMenu(
            [None, str(self.temperature), str(self.max_tokens)], id="top_menu"
        ).data_bind(InstructLayout.model)

        yield ResultViewer(id="result_viewer").data_bind(InstructLayout.content)
        yield Footer()

    def on_mount(self):
        self.title = "Instruct"
        self.sub_title = "Result Viewer"
        result_viewer = self.query_one("#result_viewer")
        result_viewer.styles.height = "9fr"
        result_viewer.styles.border = ("heavy", "white")
        top_menu = self.query_one("#top_menu")
        top_menu.styles.height = "1fr"
        result_viewer.loading = True
        self.call_after_refresh(self.run_instruct)

    @work
    async def run_instruct(self):
        try:
            instruct = Instruct(
                filepath=self.instruct_file, **self.input if self.input else {}
            )
            self.model = instruct.matching_model.name # TODO: fix the update model name in the top menu
            # self.notify(f"Running with model: {self.model}")

            result = instruct.run(
                temperature=self.temperature, max_tokens=self.max_tokens
            )
            self.content = result
            self.query_one("#result_viewer").loading = False
        except Exception as e:
            self.notify(f"Error running instruct: {e}", severity="error", title="Error")

    def action_help(self):
        self.notify("This is the GUI of `instruct`", severity="information")

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

        saved_file_ext = InstructLayout.SAVED_FILE_EXT
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


# if __name__ == "__main__":
#     app = InstructLayout()
#     app.run()
