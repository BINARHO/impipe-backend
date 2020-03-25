import logging

from typing import Dict

from tools.tool import Tool
from tools.compute_node import ComputeNode

from tools.add_tool import AddTool
from tools.subtract_tool import SubtractTool
from tools.multiply_tool import MultiplyTool
from tools.constant_tool import ConstantTool

_JSON_TYPE = Dict[str, str]


class Event(object):
    INSERTED_NODE_KEYS = "insertedNodeKeys"
    MODIFIED_NODE_DATA = "modifiedNodeData"
    REMOVED_NODE_KEYS = "removedNodeKeys"
    INSERTED_LINK_KEYS = "insertedLinkKeys"
    MODIFIED_LINK_DATA = "modifiedLinkData"
    REMOVED_LINK_KEYS = "removedLinkKeys"
    MODEL_DATA = "modelData"


class Graph(object):
    AVAILABLE_TOOLS = {
        "AddTool": AddTool,
        "SubtractTool": SubtractTool,
        "MultiplyTool": MultiplyTool,
        "ConstantTool": ConstantTool,
        "ComputeNode": ComputeNode,
    }

    def __init__(self):
        super(Graph, self).__init__()
        self.nodes: Dict[str, Tool] = {}
        self.links: Dict[str, _JSON_TYPE] = {}
        self.logger = logging.getLogger(__name__)
        self.logger.setLevel(logging.DEBUG)

    def _get_node(self, node_key: str) -> Tool:
        if node_key not in self.nodes:
            msg = f"Couldn't find node with unknown key {node_key}"
            self.logger.error(msg)
            raise RuntimeError(msg)
        return self.nodes[node_key]

    def _add_node(self, node: _JSON_TYPE) -> None:
        node_type = node["type"]
        node_key = node["key"]

        if node_type not in self.AVAILABLE_TOOLS:
            msg = f"Couldn't add new node with key {node_key} of unknown type {node_type}"
            self.logger.error(msg)
            raise IOError(msg)

        if node_key in self.nodes:
            msg = f"Couldn't add new node with key {node_key} as it already exists"
            self.logger.error(msg)
            raise RuntimeError(msg)

        self.logger.debug(f"Adding new node of type {node_type} with key {node_key}")

        new_node = self.AVAILABLE_TOOLS[node_type](node_key)
        if self.AVAILABLE_TOOLS[node_type] is ComputeNode:
            self.logger.debug(f"Setting new compute node with ket {node_key}")
        self.nodes[node_key] = new_node

    def _update_node(self, key: str, props: _JSON_TYPE) -> None:
        node = self._get_node(key)
        self.logger.debug(f"Updating node props with key {key}")
        node.update_props(props)

    def _add_link(self, link: _JSON_TYPE) -> None:
        link_key = link["key"]

        if link_key in self.links:
            raise RuntimeError()

        from_key, from_port, to_key, to_port = link["from"], link["fromPort"], link["to"], link["toPort"]
        from_node, to_node = self._get_node(from_key), self._get_node(to_key)
        self.logger.info(f"from: {from_node.key}/{from_key}")
        self.logger.info(f"to: {to_node.key}/{to_key}")

        if from_port not in from_node.outputs:
            msg = f"Couldn't link from unknown port {from_port} on node with key {from_key}"
            self.logger.error(msg)
            raise RuntimeError(msg)

        if to_port not in to_node.inputs:
            msg = f"Couldn't link to unknown port {to_port} on node with key {to_key}"
            self.logger.error(msg)
            raise RuntimeError(msg)

        self.logger.debug(f"Adding link {link_key} = {from_key}:{from_port}->{to_key}:{to_port}")

        new_output = {from_port: (to_node, to_port)}
        from_node.add_outputs(new_output)

        new_input = {to_port: (from_node, from_port)}
        to_node.update_inputs(new_input)

        self.links[link_key] = link

    def _update_link(self, link: _JSON_TYPE) -> None:
        link_key = link["key"]

        if link_key not in self.links:
            raise RuntimeError()

        # remove link and redefine it
        self._remove_link(link_key)
        self._add_link(link)

    def _remove_link(self, link_key: str) -> None:
        if link_key not in self.links:
            raise RuntimeError()

        link = self.links[link_key]
        from_key, from_port, to_key, to_port = link["from"], link["fromPort"], link["to"], link["toPort"]
        from_node, to_node = self._get_node(from_key), self._get_node(to_key)

        if from_port not in from_node.outputs:
            msg = f"Couldn't remove link from unknown port {from_port} on node with key {from_key}"
            self.logger.error(msg)
            raise RuntimeError(msg)

        if to_port not in to_node.inputs:
            msg = f"Couldn't remove link to unknown port {to_port} on node with key {to_key}"
            self.logger.error(msg)
            raise RuntimeError(msg)

        self.logger.debug(f"Removing link {link_key} = {from_key}:{from_port}->{to_key}:{to_port}")

        removed_node = {from_port: (to_key, to_port)}
        from_node.remove_outputs(removed_node)

        to_node.remove_inputs([to_port])

        del self.links[link_key]

    def _remove_node(self, key):
        # assumption: all link connected to the remove node were already removed

        _ = self._get_node(key)

        del self.nodes[key]

    def update(self, events):
        self.logger.debug(f"Got update request: {events}")

        new_nodes = []
        new_links = []

        # note new nodes
        if Event.INSERTED_NODE_KEYS in events:
            for new_key in events[Event.INSERTED_NODE_KEYS]:
                new_nodes.append(new_key)
            self.logger.debug(f"New nodes with keys: {new_nodes}")

        # handle modified nodes, if new node - create it, else - update it
        if Event.MODIFIED_NODE_DATA in events:
            for node in events[Event.MODIFIED_NODE_DATA]:
                if node["key"] in new_nodes:
                    self._add_node(node)
                self._update_node(node["key"], node["props"])

        # no need to handle new links differently - as we don't save state on links
        if Event.INSERTED_LINK_KEYS in events:
            for new_key in events[Event.INSERTED_LINK_KEYS]:
                new_links.append(new_key)
            self.logger.debug(f"New links with keys: {new_links}")

        # handle modified links and update node inputs/outputs accordingly
        if Event.MODIFIED_LINK_DATA in events:
            for link in events[Event.MODIFIED_LINK_DATA]:
                if link["key"] in new_links:
                    self._add_link(link)
                else:
                    self._update_link(link)

        # handle model change
        if Event.MODEL_DATA in events:
            self.logger.warning(f"Got model data change: {events[Event.MODEL_DATA]}")

        # handle removed links, do it before handling removed nodes
        if Event.REMOVED_LINK_KEYS in events:
            for link_key in events[Event.REMOVED_LINK_KEYS]:
                self._remove_link(link_key)

        # handle removed nodes, do it last so removed links were updated
        if Event.REMOVED_NODE_KEYS in events:
            for node in events[Event.REMOVED_NODE_KEYS]:
                self._remove_node(node["key"])

        return "updated successfully"

    def _compute_node(self, key, node: Tool):
        for name in node.inputs:
            key = node.inputs[name].connected_node.key
            port = node.inputs[name].connected_port
            if (key is None) or (port is None):
                raise RuntimeError(f"Incomplete input data for node with key {key}")
            self._compute_node(key, self.nodes[key])
            node.inputs[name].update_value(self.nodes[key].outputs[port].value)
        node.compute()

    def compute(self, event):
        compute_node_key = event["selectedData"]

        compute_node = self._get_node(compute_node_key)
        if not isinstance(compute_node, ComputeNode):
            raise IOError(f'node with key {compute_node_key} is not a compute node')

        self.logger.debug(f"Computing compute-node with key {compute_node_key}")
        self._compute_node(compute_node_key, compute_node)

        self.logger.debug(f"Computed value: {compute_node.value}")
        return compute_node.value

    def __repr__(self):
        return repr(self.nodes.keys())
