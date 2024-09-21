from textual.app import App, ComposeResult
from textual.widgets import Markdown, Header, Footer, Static
from textual.binding import Binding

from instruct.gui.widgets.top_menu import TopMenu
from instruct.gui.widgets.result_viewer import ResultViewer



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
        Binding(key="j", action="down", description="Scroll down", show=False),
    ]

    def __init__(self, content, model, max_tokens, temperature, **kwargs):
        self.content = content
        self.model = model
        self.max_tokens = max_tokens
        self.temperature = temperature
        super().__init__(**kwargs)

    def on_mount(self):
        self.title = "Instruct"
        self.sub_title = "Result Viewer"

    def compose(self) -> ComposeResult:
        top_menu = TopMenu([self.model, self.temperature, self.max_tokens])
        top_menu.styles.height = "1fr"

        result_viewer = ResultViewer(self.content)
        result_viewer.styles.height = "9fr"
        result_viewer.styles.border = ("heavy", "white")


        yield Header( show_clock=False)
        yield top_menu

        yield result_viewer
        yield Footer()
    
    def action_help(self):
        self.notify("This is the GUI of `instruct`", severity="information")


# if __name__ == "__main__":
#     app = InstructLayout()
#     app.run()
