from textual.app import App, ComposeResult
from textual.widgets import Markdown, Header, Footer, Static
from textual.binding import Binding

from instruct.gui.widgets.top_menu import TopMenu
from instruct.gui.widgets.result_viewer import ResultViewer
import pyperclip


class InstructLayout(App):
    CSS_PATH = "layout.tcss"
    

    BINDINGS = [
        Binding(key="q", action="quit", description="Quit the app"),
        Binding(
            key="question_mark",
            action="help",
            description="Show help screen",
            key_display="?",
        ),
        Binding(key="c", action="copy_result", description="Copy content to clipboard", show=True),
        Binding(key="r", action="reload", description="Reload the instruct", show=True),
    ]

    def __init__(self, instruct, content, model, max_tokens:int, temperature:int, **kwargs):
        self.content = content
        self.model = model
        self.max_tokens = max_tokens
        self.temperature = temperature
        self.instruct = instruct


        self.top_menu = TopMenu([self.model, str(self.temperature), str(self.max_tokens)])
        self.top_menu.styles.height = "1fr"

        self.result_viewer = ResultViewer(self.content)
        self.result_viewer.styles.height = "9fr"
        self.result_viewer.styles.border = ("heavy", "white")

        super().__init__(**kwargs)

    def on_mount(self):
        self.title = "Instruct"
        self.sub_title = "Result Viewer"

    def compose(self) -> ComposeResult:





        yield Header( show_clock=False)
        yield self.top_menu

        yield self.result_viewer
        yield Footer()
    
    def action_help(self):
        self.notify("This is the GUI of `instruct`", severity="information")

    def action_copy_result(self):
        try:
            pyperclip.copy(self.content)
            self.notify(f"Copied to clipboard")
        except Exception as e:
            self.notify(f"Error copying to clipboard: {e}", level="error", title="Error")

    def action_reload(self):
        try:
            reloaded = self.instruct.run(temperature=self.temperature, max_tokens=self.max_tokens)
            self.content = reloaded
            self.result_viewer.remove()
            self.result_viewer = ResultViewer(self.content)
            self.result_viewer.styles.height = "9fr"
            self.result_viewer.styles.border = ("heavy", "white")
            self.mount(self.result_viewer)
        except Exception as e:
            self.notify(f"Error reloading instruct: {e}", level="error", title="Error")



# if __name__ == "__main__":
#     app = InstructLayout()
#     app.run()
