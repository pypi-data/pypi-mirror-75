# Copyright 2019-2020 Cambridge Quantum Computing
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

"""ResultHandle class
"""

from typing import Tuple, Type, Hashable, Union
from ast import literal_eval
from collections.abc import Sequence

_BASIC_HASH_TYPES = (int, float, complex, str, bool, bytes)
# mypy doesn't think you can pass the tuple to Union
_BasicHashType = Union[_BASIC_HASH_TYPES]  # type: ignore
_ResultIdTuple = Tuple[Type[_BasicHashType], ...]


class ResultHandle(Sequence):
    """Object to store multidimensional identifiers for a circuit sent to a backend for
    execution.

    Initialisation arguments must be hashable basic types.

    Note that a `ResultHandle` may be either persistent or transient, depending on the
    backend: consult the :py:attr:`pytket.backends.Backend.persistent_handles` property
    to determine this.
    """

    def __init__(self, *args: _BasicHashType):
        self._identifiers = tuple(args)

    @classmethod
    def from_str(cls, string: str) -> "ResultHandle":
        """Construct ResultHandle from string (output from str())

        :raises ValueError: If string format is invalid
        :return: Instance of ResultHandle
        :rtype: ResultHandle
        """
        input_valid = True
        try:
            evaltuple = literal_eval(string)
        except ValueError:
            input_valid = False
        if input_valid:
            input_valid &= isinstance(evaltuple, tuple)
            if input_valid:
                input_valid &= all(
                    isinstance(arg, _BASIC_HASH_TYPES) for arg in evaltuple
                )
        if not input_valid:
            raise ValueError("ResultHandle string format invalid.")
        return cls(*evaltuple)

    def __hash__(self):
        return hash(self._identifiers)

    def __eq__(self, other):
        return self._identifiers == other._identifiers

    def __str__(self):
        return str(self._identifiers)

    def __repr__(self):
        return "ResultHandle" + repr(self._identifiers)

    def __iter__(self):
        return iter(self._identifiers)

    def __len__(self):
        return len(self._identifiers)

    def __getitem__(self, key):
        return self._identifiers[key]
