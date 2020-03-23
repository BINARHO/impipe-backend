import logging


class Tool(object):
    def __init__(self):
        super(Tool, self).__init__()
        self.inputs = {}
        self.outputs = {}
        self.props = {}
        self._should_recompute = True
        self._logger = logging.getLogger(__name__)

    def update(self, inputs, props):
        self.inputs.update(inputs)
        self.props.update(props)

        # if update ended successfully, invalidate cache
        self._should_recompute = True

    def _compute(self):
        raise NotImplementedError()

    def compute(self):
        # if no need to recompute, return cached result
        if not self._should_recompute:
            self._logger.debug("No need to recompute")
            return

        self._logger.debug("Computing")
        self._compute()

        # if computation ended successfully, cache result
        self._should_recompute = False

    def __repr__(self):
        tool_dict = {
            "name": self.__class__.__name__,
            "inputs": self.inputs.keys(),
            "outputs": self.outputs,
            "props": self.props
        }
        return repr(tool_dict)
