from textual import on
from textual.widget import Widget
from textual.widgets import Static, Label, Input

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
        yield TopMenuInput(
            "T°",
            self.app.set_temperature,
            value=self.temperature,
            id="top_menu_temperature",
        )
        yield TopMenuInput(
            f"max output tokens", 
            self.app.set_max_tokens,
            value=self.max_tokens,
            id="top_menu_max_tokens"
        )
        yield TopMenuLabel("(🔜input_token_count)", id="top_menu_token_input_label")
        yield TopMenuLabel("(🔜cost)", id="top_menu_cost_label")

    def watch_model(self, model):
        if self.is_mounted:
            model_item: Static = self.query_one("#top_menu_model_label")
            model_item.update(model)

    def watch_temperature(self, temperature):
        if self.is_mounted:
            temperature_item: Input = self.query_one("#top_menu_temperature_input")
            with temperature_item.prevent(Input.Changed):
                temperature_item.value = str(temperature)

    def watch_max_tokens(self, max_tokens):
        if self.is_mounted:
            max_tokens_item: Input = self.query_one("#top_menu_max_tokens_input")
            with max_tokens_item.prevent(Input.Changed):
                max_tokens_item.value = str(max_tokens)


class TopMenuLabel(Static):

    def __init__(self, text, **kwargs):
        super().__init__(text, **kwargs)
        self.styles.content_align = ("center", "middle")
        self.styles.height = "100%"
        self.styles.width = "100%"


class TopMenuInput(Widget):

    def __init__(
        self, label, on_input_submitted_callback: callable, value=None, **kwargs
    ):
        super().__init__(**kwargs)
        self.label = label
        self.value = value
        self.styles.content_align = ("center", "middle")
        self.styles.height = "100%"
        self.styles.width = "100%"
        self.on_input_submitted_callback = on_input_submitted_callback

    def compose(self):
        with self.prevent(Input.Changed):
            yield Label(self.label, id=f"{self.id}_label")
            yield Input(value=str(self.value), type="number", id=f"{self.id}_input")

    def on_mount(self):
        with self.prevent(Input.Changed):
            self.styles.layout = "grid"
            self.styles.grid_size_columns = 2
            self.styles.grid_size_rows = 1
            self.styles.content_align = ("center", "middle")
            self.styles.height = "100%"
            self.styles.width = "100%"

            input_widget = self.query_one(f"#{self.id}_input")
            input_widget.styles.border = None

            label_widget = self.query_one(f"#{self.id}_label")
            label_widget.styles.content_align = ("right", "middle")
            label_widget.styles.height = "100%"
            label_widget.styles.width = "100%"
            self.call_after_refresh(input_widget.action_end)

    @on(Input.Changed)
    def on_input_changed(self, event: Input.Changed):

        if event.validation_result.is_valid:
            self.value = event.value
            self.on_input_submitted_callback(event.value)
