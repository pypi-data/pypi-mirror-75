# Copyright (C) 2020 Alteryx, Inc. All rights reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
"""Class that saves input connection information given the associated anchor."""
from typing import Dict, List, TYPE_CHECKING

from ayx_plugin_sdk.providers.amp_provider.builders.input_connection_builder import (
    InputConnectionBuilder,
)
from ayx_plugin_sdk.providers.amp_provider.repositories.singleton import Singleton

if TYPE_CHECKING:
    from ayx_plugin_sdk.providers.amp_provider.amp_input_anchor import AMPInputAnchor
    from ayx_plugin_sdk.providers.amp_provider.amp_input_connection import (
        AMPInputConnection,
    )
    from ayx_plugin_sdk.providers.amp_provider.resources.generated.incoming_anchor_pb2 import (
        IncomingConnection as ProtobufInputConnection,
    )


class InputConnectionRepository(metaclass=Singleton):
    """Repository that stores input connection information."""

    _input_connection_builder = InputConnectionBuilder()

    def __init__(self) -> None:
        """Initialize the input connection repository."""
        self._anchor_connection_map: Dict[str, List["AMPInputConnection"]] = {}

    def save_connection(
        self, anchor_name: str, connection: "AMPInputConnection"
    ) -> None:
        """Save input connection information for the assoiciated anchor name."""
        self._anchor_connection_map.setdefault(anchor_name, [])
        self._anchor_connection_map[anchor_name].append(connection)

    def save_grpc_connection(
        self, anchor: "AMPInputAnchor", connection: "ProtobufInputConnection"
    ) -> None:
        """Save input connection information for the associated anchor name given a Protobuf incoming connection message."""
        amp_connection, _ = self._input_connection_builder.from_protobuf(
            connection, anchor
        )
        self.save_connection(anchor.name, amp_connection)

    def get_all_connections(self, anchor_name: str) -> List["AMPInputConnection"]:
        """Get the connections associated with the given anchor name."""
        connections = self._anchor_connection_map.get(anchor_name)
        if not connections:
            raise ValueError(f"Anchor {anchor_name} not found.")

        return connections

    def get_connection(
        self, anchor_name: str, connection_name: str
    ) -> "AMPInputConnection":
        """Get the connection associated with the given anchor name and connection name."""
        connections = self.get_all_connections(anchor_name)
        for connection in connections:
            if connection.name == connection_name:
                return connection

        raise ValueError(
            f"Input connection {connection_name} not found for anchor {anchor_name}."
        )

    def delete_connection(self, anchor_name: str, connection_name: str) -> None:
        """Delete the connection associated with the given anchor name and connection name."""
        connections = self.get_all_connections(anchor_name)
        for idx, connection in enumerate(connections):
            if connection.name == connection_name:
                connections.pop(idx)
                return

        raise ValueError(
            f"Input connection {connection_name} not found for anchor {anchor_name}."
        )
