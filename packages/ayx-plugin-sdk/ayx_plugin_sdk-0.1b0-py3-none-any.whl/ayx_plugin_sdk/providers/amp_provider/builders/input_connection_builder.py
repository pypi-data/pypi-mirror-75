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
"""Class that implements the serialization/deserialization for input connection protobuf objects."""
from typing import TYPE_CHECKING, Tuple

from ayx_plugin_sdk.providers.amp_provider.amp_input_connection import (
    AMPInputConnection,
)
from ayx_plugin_sdk.providers.amp_provider.builders.metadata_builder import (
    MetadataBuilder,
)
from ayx_plugin_sdk.providers.amp_provider.resources.generated.incoming_anchor_pb2 import (
    IncomingConnection,
)


if TYPE_CHECKING:
    from ayx_plugin_sdk.providers.amp_provider.amp_input_anchor import AMPInputAnchor


class InputConnectionBuilder:
    """RPC Builder for transforming InputConnection into Protobuf messages and vice versa."""

    metadata_builder = MetadataBuilder()

    @classmethod
    def to_protobuf(
        cls, input_connection: AMPInputConnection, tool_id: int
    ) -> IncomingConnection:
        """Serialize an AMPInputConnection object (amp_provider.amp_input_connection) object into a Protobuf object."""
        name = input_connection.name
        if input_connection.metadata is None:
            raise RuntimeError(
                "Input connection must be open in order to convert it to a Protobuf message."
            )

        metadata = cls.metadata_builder.to_protobuf(input_connection.metadata)
        return IncomingConnection(name=name, tool_id=tool_id, metadata=metadata)

    @classmethod
    def from_protobuf(
        cls, message: IncomingConnection, input_anchor: "AMPInputAnchor"
    ) -> Tuple[AMPInputConnection, int]:
        """Deserialize a Protobuf object into an AMPInputConnection object (amp_provider.amp_input_connection)."""
        name = message.name
        metadata = cls.metadata_builder.from_protobuf(message.metadata)
        return AMPInputConnection(name, metadata, input_anchor), message.tool_id
