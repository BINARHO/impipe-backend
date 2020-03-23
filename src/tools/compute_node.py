from tools.tool import Tool


class ComputeNode(Tool):
    def __init__(self):
        super(ComputeNode, self).__init__()
        self.inputs = {"in": None}
        self.value = None

    def _compute(self):
        if self.inputs["in"]:
            self.value = self.inputs["in"]["value"]
