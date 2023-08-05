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
"""Alteryx plugin output anchor definition, AMP."""
from typing import Optional, TYPE_CHECKING

from ayx_plugin_sdk.core import Metadata, OutputAnchorBase, RecordPacketBase
from ayx_plugin_sdk.core.doc_utilities import inherit_docs
from ayx_plugin_sdk.providers.amp_provider.repositories.output_record_packet_repository import (
    OutputRecordPacketRepository,
)

if TYPE_CHECKING:
    import pandas as pd  # noqa: F401


@inherit_docs
class AMPOutputAnchor(OutputAnchorBase):
    """Output anchor definition, AMP."""

    def __init__(
        self,
        name: str,
        allow_multiple: bool = False,
        optional: bool = False,
        metadata: Optional[Metadata] = None,
    ) -> None:
        self.__name: str = name
        self.__allow_multiple: bool = allow_multiple
        self.__optional: bool = optional
        self.__metadata: Optional[Metadata] = metadata
        self.__num_connections: int = 0
        self.written_dataframe: Optional["pd.Dataframe"] = None

    @property
    def name(self) -> str:  # noqa: D102
        return self.__name

    @property
    def allow_multiple(self) -> bool:  # noqa: D102
        return self.__allow_multiple

    @property
    def optional(self) -> bool:  # noqa: D102
        return self.__optional

    @property
    def num_connections(self) -> int:  # noqa: D102
        return self.__num_connections

    @property
    def is_open(self) -> bool:  # noqa: D102
        return isinstance(self.__metadata, Metadata)

    @property
    def metadata(self) -> Optional["Metadata"]:  # noqa: D102
        return self.__metadata

    def open(self, metadata: "Metadata") -> None:  # noqa: D102
        self.__metadata = metadata

    def write(self, record_packet: "RecordPacketBase") -> None:  # noqa: D102
        if self.metadata is None:
            raise RuntimeError("Output anchor is not open.")

        if record_packet.metadata != self.__metadata:
            raise RuntimeError(
                "Output anchor's metadata does not match incoming record packet."
            )

        OutputRecordPacketRepository().save_record_packet(self.name, record_packet)

    def flush(self) -> None:  # noqa: D102
        raise NotImplementedError

    def close(self) -> None:  # noqa: D102
        self.__metadata = None

    def update_progress(self, percentage: float) -> None:  # noqa: D102
        raise NotImplementedError
