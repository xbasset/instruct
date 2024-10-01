from textual.widget import Widget
from textual.widgets import Static

from textual.reactive import reactive


class TopMenu(Widget):
    """A top menu widget that displays a list of menu items."""

    model = reactive("")
    temperature = reactive(0)
    max_tokens = reactive(0)

    def __init__(self, **kwargs) -> None:
        super().__init__(**kwargs)

    def compose(self):

        model_label = TopMenuLabel(f"{self.model}", id="top_menu_model_label")
        model_label.styles.color = "lime"
        yield model_label
        yield TopMenuLabel(f"T°: {self.temperature}", id="top_menu_temperature_label")
        yield TopMenuLabel(
            f"Max Output Tokens: {self.max_tokens}", id="top_menu_max_tokens_label"
        )
        yield TopMenuLabel("Input Tokens Count", id="top_menu_token_input_label")
        yield TopMenuLabel("Cost", id="top_menu_cost_label")

    def watch_model(self, model):
        if self.is_mounted:
            model_item:Static = self.query_one("#top_menu_model_label")
            model_item.update(model)

    def watch_temperature(self, temperature):
        if self.is_mounted:
            temperature_item:Static = self.query_one("#top_menu_temperature_label")
            temperature_item.update(f"T°: {temperature}")
    
    def watch_max_tokens(self, max_tokens):
        if self.is_mounted:
            max_tokens_item:Static = self.query_one("#top_menu_max_tokens_label")
            max_tokens_item.update(f"Max Output Tokens: {max_tokens}")

class TopMenuLabel(Static):

    def __init__(self, text, **kwargs):
        super().__init__(text, **kwargs)
        self.styles.content_align = ("center", "middle")
        self.styles.height = "100%"
        self.styles.width = "100%"