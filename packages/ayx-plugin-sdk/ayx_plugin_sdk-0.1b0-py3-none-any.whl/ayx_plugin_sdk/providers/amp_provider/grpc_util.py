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
"""Functions demonstrating available port finding for server binding/client connection."""
import socket
from socket import AddressFamily


PORT_MIN = 49152
PORT_MAX = 65535


def can_connect(port: int) -> bool:
    """Check whether a given port number can be connected to, then closes the socket."""
    s = socket.socket()
    try:
        s.connect(("localhost", port))
        return True
    except socket.error:
        return False
    finally:
        s.close()


def can_bind(port: int, proto: AddressFamily = socket.AF_INET) -> bool:
    """Check whether a given port number can be bound to, then closes the socket."""
    s = socket.socket(
        proto, socket.SOCK_STREAM
    )  # use socket.AF_INET(ipv4) for now, allow for AF_INET6 later(?)
    try:
        s.bind(("localhost", port))
        return True
    except socket.error:
        return False
    finally:
        s.close()


def find_port(port_min: int, port_max: int) -> int:
    """Given a range of port numbers, check port numbers until one is available and returns."""
    if port_min >= port_max:
        raise ValueError("Invalid range. Min port must be less than max port")
    if port_min < PORT_MIN or port_max > PORT_MAX:
        raise ValueError(
            "The allowed range for dynamic ports is between 49152 and 65535"
        )
    for p in range(port_min, port_max + 1):
        if can_bind(p):
            return p
    raise RuntimeError("No ports available")
