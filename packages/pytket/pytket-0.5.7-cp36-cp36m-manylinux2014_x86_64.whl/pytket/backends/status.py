# Copyright 2020 Cambridge Quantum Computing
#
# Licensed under a Non-Commercial Use Software Licence (the "Licence");
# you may not use this file except in compliance with the Licence.
# You may obtain a copy of the Licence in the LICENCE file accompanying
# these documents or at:
#
#     https://cqcl.github.io/pytket/build/html/licence.html
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the Licence is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the Licence for the specific language governing permissions and
# limitations under the Licence, but note it is strictly for non-commercial use.

"""Status classes for circuits submitted to backends.
"""
from typing import NamedTuple
from enum import Enum


class StatusEnum(Enum):
    """Enumeration for the possible status of a circuit submitted to a backend.
    """

    COMPLETED = "Circuit has completed. Results are ready."
    QUEUED = "Circuit is queued."
    SUBMITTED = "Circuit has been submitted."
    RUNNING = "Circuit is running."
    ERROR = "Circuit has errored. Check CircuitStatus.message for error message."


class CircuitStatus(NamedTuple):
    """The status of a circuit along with optional long description, \
for example an error message."""

    status: StatusEnum
    message: str = ""


WAITING_STATUS = {StatusEnum.QUEUED, StatusEnum.SUBMITTED, StatusEnum.RUNNING}
