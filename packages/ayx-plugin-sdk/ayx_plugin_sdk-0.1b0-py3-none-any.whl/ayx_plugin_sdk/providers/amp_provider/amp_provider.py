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
"""E1 SDK Provider Class."""
from logging import Logger
from typing import Dict, TYPE_CHECKING

from ayx_plugin_sdk.core import ProviderBase
from ayx_plugin_sdk.core.doc_utilities import inherit_docs

if TYPE_CHECKING:
    from ayx_plugin_sdk.providers.amp_provider.amp_environment import AMPEnvironment
    from ayx_plugin_sdk.providers.amp_provider.amp_input_anchor import AMPInputAnchor
    from ayx_plugin_sdk.providers.amp_provider.amp_io import AMPIO
    from ayx_plugin_sdk.providers.amp_provider.amp_output_anchor import AMPOutputAnchor


@inherit_docs
class AMPProvider(ProviderBase):
    """Provides resources generated from AMP Python SDK."""

    @property
    def logger(self) -> "Logger":  # noqa: D102
        raise NotImplementedError

    @property
    def io(self) -> "AMPIO":  # noqa: D102
        raise NotImplementedError

    @property
    def environment(self) -> "AMPEnvironment":  # noqa: D102
        raise NotImplementedError

    def get_input_anchor(self, name: str) -> "AMPInputAnchor":  # noqa: D102
        raise NotImplementedError

    def get_output_anchor(self, name: str) -> "AMPOutputAnchor":  # noqa: D102
        raise NotImplementedError

    @property
    def tool_config(self) -> Dict:  # noqa: D102
        raise NotImplementedError
