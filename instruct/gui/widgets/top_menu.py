from textual.widget import Widget
from textual.widgets import Static

from textual.reactive import reactive

class MenuItem(Widget):
    def __init__(self, value, **kwargs):
        self.value = value
        super().__init__(**kwargs)

    def compose(self):
        content = Static(self.value)
        content.styles.content_align = ("center", "middle")
        content.styles.height = "100%"
        content.styles.height = "1fr"

        yield content

class TopMenu(Widget):
    """A top menu widget that displays a list of menu items."""

    model = reactive("")

    def __init__(self, items: list[str], **kwargs) -> None:
        """Initialize the top menu widget.

        Args:
            items: A list of menu items to display.
        """
        super().__init__(**kwargs)
        self.items = items
        items[0] = self.model

    def compose(self):
        for item in self.items:
            menu_idem = MenuItem(item)
            menu_idem.styles.background = "royalblue"
            menu_idem.styles.margin = 1
            menu_idem.styles.height = "100%"
            yield menu_idem
    
    def watch_model(self, model):
        if self.is_mounted:
            self.items[0] = model
            self.refresh()
            