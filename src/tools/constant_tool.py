from .tool import Tool


class ConstantTool(Tool):
    def __init__(self, key: str):
        super(ConstantTool, self).__init__(key)
        self._add_output_field("out")
        self._add_prop_field("value")

    def _compute(self):
        if self.props["value"]:
            self.outputs["out"].update_value(int(self.props["value"]))
