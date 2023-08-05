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
"""Utility classes for converting between byte representations."""
import struct
from abc import ABC, abstractmethod
from typing import Any, Tuple


class _Packer(ABC):
    def pack(self, element: Any) -> bytes:
        return struct.pack(self._format_code, element)

    def unpack(self, raw_bytes: bytes, start_idx: int) -> Tuple[Any, int]:
        element_bytes = raw_bytes[start_idx : start_idx + self._element_size]
        [parsed_element] = struct.unpack(self._format_code, element_bytes)

        return parsed_element, self._element_size

    @property
    @abstractmethod
    def _format_code(self) -> str:
        """Get the format code for struct package."""
        raise NotImplementedError()

    @property
    @abstractmethod
    def _element_size(self) -> int:
        """Get the element size in bytes of the packer."""
        raise NotImplementedError()

    @staticmethod
    def _unpack_sized_blob(blob: bytes, start_idx: int) -> Tuple[bytes, int]:
        element_size, integer_size = _UnsignedIntegerPacker().unpack(blob, start_idx)
        return (
            blob[start_idx + integer_size : start_idx + integer_size + element_size],
            element_size + integer_size,
        )


class _BoolPacker(_Packer):
    _element_size = 1
    _format_code = "?"


class _IntegerPacker(_Packer):
    _element_size = 4
    _format_code = "i"


class _UnsignedIntegerPacker(_Packer):
    _element_size = 4
    _format_code = "I"


class _LongIntegerPacker(_Packer):
    _element_size = 8
    _format_code = "Q"


class _FloatPacker(_Packer):
    _element_size = 4
    _format_code = "f"


class _DoublePacker(_Packer):
    _element_size = 8
    _format_code = "d"


class _StringPacker(_Packer):
    @classmethod
    def pack(cls, string: str) -> bytes:
        string_bytes = string.encode("utf-8")
        string_size = len(string_bytes)
        return _UnsignedIntegerPacker().pack(string_size) + string_bytes

    @classmethod
    def unpack(cls, raw_bytes: bytes, start_idx: int) -> Tuple[str, int]:
        blob, element_size = cls._unpack_sized_blob(raw_bytes, start_idx)
        return blob.decode("utf-8"), element_size

    @property
    def _format_code(self) -> str:
        """Get the format code for struct package."""
        raise NotImplementedError()

    @property
    def _element_size(self) -> int:
        """Get the element size in bytes of the packer."""
        raise NotImplementedError()


class _BlobPacker(_Packer):
    @classmethod
    def pack(cls, blob: bytes) -> bytes:
        return _UnsignedIntegerPacker().pack(len(blob)) + blob

    @classmethod
    def unpack(cls, raw_bytes: bytes, start_idx: int) -> Tuple[bytes, int]:
        return cls._unpack_sized_blob(raw_bytes, start_idx)

    @property
    def _format_code(self) -> str:
        """Get the format code for struct package."""
        raise NotImplementedError()

    @property
    def _element_size(self) -> int:
        """Get the element size in bytes of the packer."""
        raise NotImplementedError()


class _IndirectStringPacker(_Packer):
    @classmethod
    def pack(cls, string: str) -> bytes:
        return bytes()

    @classmethod
    def unpack(cls, raw_bytes: bytes, start_idx: int) -> Tuple[str, int]:
        return "", 0

    @property
    def _format_code(self) -> str:
        """Get the format code for struct package."""
        raise NotImplementedError()

    @property
    def _element_size(self) -> int:
        """Get the element size in bytes of the packer."""
        raise NotImplementedError()


class _IndirectBlobPacker(_Packer):
    @classmethod
    def pack(cls, blob: bytes) -> bytes:
        return bytes()

    @classmethod
    def unpack(cls, raw_bytes: bytes, start_idx: int) -> Tuple[bytes, int]:
        return bytes(), 0

    @property
    def _format_code(self) -> str:
        """Get the format code for struct package."""
        raise NotImplementedError()

    @property
    def _element_size(self) -> int:
        """Get the element size in bytes of the packer."""
        raise NotImplementedError()


class _BoolTruePacker(_Packer):
    @classmethod
    def pack(cls, element: bool) -> bytes:
        return bytes()

    @classmethod
    def unpack(cls, raw_bytes: bytes, start_idx: int) -> Tuple[bool, int]:
        return True, 0

    @property
    def _format_code(self) -> str:
        """Get the format code for struct package."""
        raise NotImplementedError()

    @property
    def _element_size(self) -> int:
        """Get the element size in bytes of the packer."""
        raise NotImplementedError()


class _BoolFalsePacker(_Packer):
    @classmethod
    def pack(cls, element: bool) -> bytes:
        return bytes()

    @classmethod
    def unpack(cls, raw_bytes: bytes, start_idx: int) -> Tuple[bool, int]:
        return False, 0

    @property
    def _format_code(self) -> str:
        """Get the format code for struct package."""
        raise NotImplementedError()

    @property
    def _element_size(self) -> int:
        """Get the element size in bytes of the packer."""
        raise NotImplementedError()


class _EmptyStringPacker(_Packer):
    @classmethod
    def pack(cls, element: str) -> bytes:
        return bytes()

    @classmethod
    def unpack(cls, raw_bytes: bytes, start_idx: int) -> Tuple[str, int]:
        return "", 0

    @property
    def _format_code(self) -> str:
        """Get the format code for struct package."""
        raise NotImplementedError()

    @property
    def _element_size(self) -> int:
        """Get the element size in bytes of the packer."""
        raise NotImplementedError()


class _NullPacker(_Packer):
    @classmethod
    def pack(cls, element: str) -> bytes:
        return bytes()

    @classmethod
    def unpack(cls, raw_bytes: bytes, start_idx: int) -> Tuple[None, int]:
        return None, 0

    @property
    def _format_code(self) -> str:
        """Get the format code for struct package."""
        raise NotImplementedError()

    @property
    def _element_size(self) -> int:
        """Get the element size in bytes of the packer."""
        raise NotImplementedError()


class _Int0Packer(_Packer):
    @classmethod
    def pack(cls, element: str) -> bytes:
        return bytes()

    @classmethod
    def unpack(cls, raw_bytes: bytes, start_idx: int) -> Tuple[int, int]:
        return 0, 0

    @property
    def _format_code(self) -> str:
        """Get the format code for struct package."""
        raise NotImplementedError()

    @property
    def _element_size(self) -> int:
        """Get the element size in bytes of the packer."""
        raise NotImplementedError()
