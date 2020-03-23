from tools.tool import Tool


class MultiplyTool(Tool):
    def __init__(self):
        super(MultiplyTool, self).__init__()
        self.inputs = {
            "a": None,
            "b": None,
        }
        self.outputs = {
            "mul": None
        }

    def _compute(self):
        mul = 1
        for input_node in self.inputs.values():
            if input_node["value"]:
                mul *= int(input_node["value"])
        self.outputs["mul"] = mul
