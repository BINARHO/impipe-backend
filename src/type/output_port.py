from typing import Dict, Tuple, TYPE_CHECKING

if TYPE_CHECKING:
    from tools import Tool

from .port import Port


class OutputPort(Port):
    def __init__(self, value=None, value_type=None):
        super(OutputPort, self).__init__(value, value_type)
        self._connected_nodes: Dict[Tuple[str, str], 'Tool'] = {}

    def _update_connected_nodes(self):
        for node in self._connected_nodes.values():
            node.recompute()

    def update_value(self, new_value):
        super(OutputPort, self).update_value(new_value)
        self._update_connected_nodes()

    def add_connected_node(self, node: 'Tool', port: str):
        if not all([port, node, node.key]):
            raise ValueError('all given values should not be None')

        if (node.key, port) in self._connected_nodes:
            raise ValueError(f'node with key {node.key} and port {port} is already connected to this port')

        if port not in node.inputs:
            raise ValueError(f'node with key {node.key} does not have input port {port}')

        self._connected_nodes[(node.key, port)] = node
        self._connected_nodes[(node.key, port)].recompute()

    def remove_connected_node(self, key, port):
        if (key, port) not in self._connected_nodes:
            raise ValueError(f'node with key {key} and port {port} is not connected to this port')

        node = self._connected_nodes[(key, port)]

        del self._connected_nodes[(key, port)]

        node.recompute()
