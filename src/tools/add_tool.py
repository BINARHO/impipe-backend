from .tool import Tool


class AddTool(Tool):
    def __init__(self, key: str):
        super(AddTool, self).__init__(key)
        self._add_input_field("a")
        self._add_input_field("b")
        self._add_output_field("sum")

    def _compute(self):
        sum = 0
        for input_node in self.inputs.values():
            if input_node.value:
                sum += int(input_node.value)
        self.outputs["sum"].update_value(sum)
