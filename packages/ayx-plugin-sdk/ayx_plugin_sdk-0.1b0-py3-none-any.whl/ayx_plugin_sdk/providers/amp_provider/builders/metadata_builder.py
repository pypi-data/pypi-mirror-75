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
"""Class that implements the serialization/deserialization for Metadata protobuf objects."""
from ayx_plugin_sdk.core.field import FieldType as CoreFieldType
from ayx_plugin_sdk.core.metadata import Metadata as CoreMetadata
from ayx_plugin_sdk.providers.amp_provider.resources.generated.metadata_pb2 import (
    FieldType as ProtobufFieldType,
    Metadata as ProtobufMetadata,
)


class MetadataBuilder:
    """RPC Builder for transforming Metadata into Protobufs and vice versa."""

    @staticmethod
    def to_protobuf(metadata: CoreMetadata) -> ProtobufMetadata:
        """Serialize a Metadata (core.metadata) object into a protobuf."""
        m = ProtobufMetadata()
        for field in metadata.fields:
            f = m.fields.add()
            f.name = field.name
            f.size = field.size
            f.scale = field.scale
            f.source = field.source
            f.description = field.description
            f.type = ProtobufFieldType.Value(f"FT_{field.type.name.upper()}")
        return m

    @staticmethod
    def from_protobuf(message: ProtobufMetadata) -> CoreMetadata:
        """Deserialize a protobuf into a Metadata object (core.metadata)."""
        m = CoreMetadata()
        for field in message.fields:
            name = field.name
            field_type = CoreFieldType(
                ProtobufFieldType.Name(field.type).lower()[len("FT_") :]
            )
            size = field.size or 0
            scale = field.scale or 0
            source = field.source or ""
            description = field.description or ""
            m.add_field(
                name=name,
                field_type=field_type,
                size=size,
                scale=scale,
                source=source,
                description=description,
            )
        return m
