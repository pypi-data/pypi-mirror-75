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
"""Class that saves/retrieves output record packets."""
from typing import Dict, TYPE_CHECKING

from ayx_plugin_sdk.providers.amp_provider.builders.record_packet_builder import (
    RecordPacketBuilder,
)
from ayx_plugin_sdk.providers.amp_provider.repositories.singleton import Singleton

if TYPE_CHECKING:
    from ayx_plugin_sdk.core.record_packet_base import RecordPacketBase
    from ayx_plugin_sdk.providers.amp_provider.resources.generated.record_packet_pb2 import (
        RecordPacket as ProtobufRecordPacket,
    )


class OutputRecordPacketRepository(metaclass=Singleton):
    """Repository that stores output record packets."""

    _record_packet_builder = RecordPacketBuilder()

    def __init__(self) -> None:
        """Initialize the output record packet repository."""
        self._record_packet_map: Dict[str, "RecordPacketBase"] = {}

    def save_record_packet(
        self, anchor_name: str, record_packet: "RecordPacketBase"
    ) -> None:
        """Save a record packet."""
        self._record_packet_map[anchor_name] = record_packet

    def get_record_packet(self, anchor_name: str) -> "RecordPacketBase":
        """Get a record packet."""
        if anchor_name not in self._record_packet_map:
            raise ValueError(f"Anchor {anchor_name} not found in repository.")

        return self._record_packet_map[anchor_name]

    def get_grpc_record_packet(self, anchor_name: str) -> "ProtobufRecordPacket":
        """Get a record packet in protobuf format."""
        record_packet = self.get_record_packet(anchor_name)

        # TODO: Get sequence and progress correctly
        return self._record_packet_builder.to_protobuf(record_packet, 1, 0)
