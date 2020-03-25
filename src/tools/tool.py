from __future__ import annotations  # for self reference in type annotation

import logging

from typing import Dict, Tuple, List, Any

from type import InputPort, OutputPort


class Tool(object):
    def __init__(self, key: str):
        super(Tool, self).__init__()
        self.key: str = key
        self.inputs: Dict[str, InputPort] = {}
        self.outputs: Dict[str, OutputPort] = {}
        self.props: Dict[str, Any] = {}
        self._should_recompute: bool = True
        self._logger = logging.getLogger(__name__)

    def _add_input_field(self, input_name, input_type=None):
        self.inputs[input_name] = InputPort(value_type=input_type)

    def _add_output_field(self, output_name, output_type=None):
        self.outputs[output_name] = OutputPort(value_type=output_type)

    def _add_prop_field(self, prop_name):
        self.props[prop_name] = None

    def _validate_keys_input(self, ref_keys, in_keys, msg):
        if not set(ref_keys).issuperset(set(in_keys)):
            undefined_props = set(in_keys).difference(set(ref_keys))
            raise IOError(f'{msg}: {undefined_props}')

    def update_props(self, props: Dict[str, Any]):
        # validate all props defined by this tool
        self._validate_keys_input(ref_keys=self.props.keys(), in_keys=props.keys(),
                                  msg='not all given prop are defined for this tool')

        # after validation, update props
        self.props.update(props)

        self._should_recompute = True

    def update_inputs(self, changed_inputs: Dict[str, Tuple[Tool, str]]):
        # validate all props defined by this tool
        self._validate_keys_input(ref_keys=self.inputs.keys(), in_keys=changed_inputs.keys(),
                                  msg='not all given inputs are defined for this tool')

        for port_name, (node_connected, port_connected) in changed_inputs.items():
            self.inputs[port_name].update_connected_node(node_connected, port_connected)

        self._should_recompute = True

    def remove_inputs(self, removed_inputs: List[str]):
        # validate all props defined by this tool
        self._validate_keys_input(ref_keys=self.inputs.keys(), in_keys=removed_inputs,
                                  msg='not all given inputs are defined for this tool')

        for port_name in removed_inputs:
            self.inputs[port_name].remove_connected_node()

        self._should_recompute = True

    def add_outputs(self, added_outputs: Dict[str, Tuple[Tool, str]]):
        # validate all props defined by this tool
        self._validate_keys_input(ref_keys=self.outputs.keys(), in_keys=added_outputs.keys(),
                                  msg='not all given outputs are defined for this tool')

        for port_name, (node_connected, port_connected) in added_outputs.items():
            self.outputs[port_name].add_connected_node(node_connected, port_connected)

        self._should_recompute = True

    def remove_outputs(self, removed_outputs: Dict[str, Tuple[str, str]]):
        # validate all props defined by this tool
        self._validate_keys_input(ref_keys=self.outputs.keys(), in_keys=removed_outputs.keys(),
                                  msg='not all given outputs are defined for this tool')

        for port_name, (key_connected, port_connected) in removed_outputs.items():
            self.outputs[port_name].remove_connected_node(key_connected, port_connected)

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

    def recompute(self):
        self._should_recompute = True
        self.compute()

    def __repr__(self):
        tool_dict = {
            "name": self.__class__.__name__,
            "inputs": self.inputs.keys(),
            "outputs": self.outputs,
            "props": self.props
        }
        return repr(tool_dict)
