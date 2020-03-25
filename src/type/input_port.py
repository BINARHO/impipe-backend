from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from tools import Tool

from .port import Port


class InputPort(Port):
    def __init__(self, value=None, value_type=None):
        super(InputPort, self).__init__(value, value_type)
        self._connected_node: 'Tool' = None
        self._connected_port: str = None

    @property
    def connected_node(self):
        return self._connected_node

    @property
    def connected_port(self):
        return self._connected_port

    def _recompute_connected_port(self):
        if self._connected_node is not None:
            self._connected_node.recompute()

    def update_value(self, new_value):
        super(InputPort, self).update_value(new_value)
        self._recompute_connected_port()

    def update_connected_node(self, node: 'Tool', port: str):
        if self._connected_node is not None:
            raise ValueError('input port is already connected')

        if port not in node.outputs:
            raise ValueError(f'node with key {node.key} does not have input port {port}')

        self._connected_node = node
        self._connected_port = port

    def remove_connected_node(self):
        if self._connected_node is None:
            raise ValueError('input port is already not connected')

        self._connected_node = None
        self._connected_port = None

    def __repr__(self):
        return f'connected to {self.connected_node.key}:{self.connected_port}'
