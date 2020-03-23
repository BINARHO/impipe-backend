from tools.tool import Tool


class AddTool(Tool):
    def __init__(self):
        super(AddTool, self).__init__()
        self.inputs = {
            "a": None,
            "b": None,
        }
        self.outputs = {
            "sum": None
        }

    def _compute(self):
        sum = 0
        for input_node in self.inputs.values():
            if input_node["value"]:
                sum += int(input_node["value"])
        self.outputs["sum"] = sum
