from tools.tool import Tool


class SubtractTool(Tool):
    def __init__(self, key: str):
        super(SubtractTool, self).__init__(key)
        self.inputs = {
            "a": None,
            "b": None,
        }
        self.outputs = {
            "sub": None
        }

    def _compute(self):
        sub = self.inputs["a"]["value"]
        sub -= self.inputs["b"]["value"]
        self.outputs["sub"] = sub
