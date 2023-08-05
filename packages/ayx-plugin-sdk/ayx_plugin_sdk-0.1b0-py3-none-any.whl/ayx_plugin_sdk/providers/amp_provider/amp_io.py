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
"""Proxy Class for SDK IO, AMP."""
from pathlib import Path
from typing import Any

from ayx_plugin_sdk.core import IoBase
from ayx_plugin_sdk.core.doc_utilities import inherit_docs


@inherit_docs
class AMPIO(IoBase):
    """Class that wraps all IO with Designer."""

    def error(self, error_msg: str) -> None:  # noqa: D102
        raise NotImplementedError

    def warn(self, warn_msg: str) -> None:  # noqa: D102
        raise NotImplementedError

    def info(self, info_msg: str) -> None:  # noqa: D102
        raise NotImplementedError

    def translate_msg(self, msg: str, *args: Any) -> str:  # noqa: D102
        raise NotImplementedError

    def update_progress(self, percent: float) -> None:  # noqa: D102
        raise NotImplementedError

    def create_temp_file(
        self, extension: str = "tmp", options: int = 0
    ) -> "Path":  # noqa: D102
        raise NotImplementedError
