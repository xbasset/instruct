from textual.widget import Widget
from textual.widgets import Markdown
from textual.containers import ScrollableContainer

class ResultViewer(Widget):
    def __init__(self, content, **kwargs):
        self.content = content
        super().__init__(**kwargs)

    def compose(self):
        yield ScrollableContainer(Markdown(self.content))