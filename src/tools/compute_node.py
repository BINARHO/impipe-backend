from tools.tool import Tool


class ComputeNode(Tool):
    def __init__(self, key: str):
        super(ComputeNode, self).__init__(key)
        self._add_input_field('in')
        self.value = None

    def _compute(self):
        if self.inputs["in"]:
            self.value = self.inputs["in"].value
