from textual.widget import Widget
from textual.widgets import Markdown
from textual.containers import ScrollableContainer

from textual.reactive import reactive

class ResultViewer(Widget):
    
    content = reactive("")

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def compose(self):
        yield ScrollableContainer(Markdown(self.content, id="content"))

    def watch_content(self, content):
        if self.is_mounted:
            markdown : Markdown = self.query_one("#content")
            markdown.update(content)