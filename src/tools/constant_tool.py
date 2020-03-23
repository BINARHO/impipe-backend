from tools.tool import Tool


class ConstantTool(Tool):
    def __init__(self):
        super(ConstantTool, self).__init__()
        self.outputs = {"out": None}

    def _compute(self):
        if self.props["value"]:
            self.outputs["out"] = int(self.props["value"])
