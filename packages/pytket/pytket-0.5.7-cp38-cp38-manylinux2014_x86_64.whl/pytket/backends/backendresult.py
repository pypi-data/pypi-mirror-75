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

"""`BackendResult` class and associated methods."""
from typing import (
    Optional,
    Any,
    Sequence,
    Iterable,
    List,
    Dict,
    Counter,
    NamedTuple,
    Collection,
    TypeVar,
)
import operator
from functools import reduce
import numpy as np

from pytket.circuit import Bit, Qubit, UnitID
from pytket.utils.results import (
    probs_from_state,
    get_n_qb_from_statevector,
    permute_statearray_qb_labels,
)
from pytket.utils.outcomearray import OutcomeArray

from .backend_exceptions import InvalidResultType


class StoredResult(NamedTuple):
    """NamedTuple with optional fields for all result types."""

    counts: Optional[Counter[OutcomeArray]] = None
    shots: Optional[OutcomeArray] = None
    state: Optional[np.ndarray] = None
    unitary: Optional[np.ndarray] = None


class BackendResult:
    """ Encapsulate generic results from pytket Backend instances.

    Results can either be measured (shots or counts), or ideal simulations in
    the form of statevector or unitary arrays. For measured results, a map of
    Bit identifiers to its stored outcome index is also stored (e.g.
    {Bit(1):2} tells us Qubit(1) corresponds to the 1 reading in the bitstring
    0010). Likewise, for state results a map of Qubit identifiers to qubit
    location in basis vector labelling is stored (e.g. statevector index 3
    corresponds to bitwise encoding 011, and a mapping {Qubit(2): 0} tells us
    the 0 in the bitwise encoding corresponds to Qubit(2)).
    """

    def __init__(
        self,
        *,
        q_bits: Iterable[Qubit] = None,
        c_bits: Iterable[Bit] = None,
        counts: Counter[OutcomeArray] = None,
        shots: OutcomeArray = None,
        state: Any = None,
        unitary: Any = None,
    ):
        self._counts = counts
        self._shots = shots
        self.measured_results = (self._counts is not None) or (self._shots is not None)

        self._state = state
        self._unitary = unitary
        self.state_results = (self._state is not None) or (self._unitary is not None)

        self.c_bits: Dict[Bit, int] = {}
        self.q_bits: Dict[Qubit, int] = {}

        def _process_unitids(var, attr, lent, uid):
            if var is not None:
                setattr(self, attr, dict(reversed(pair) for pair in enumerate(var)))
                if lent != len(var):
                    raise ValueError(
                        (
                            f"Length of {attr} ({len(var)}) does not"
                            " match input data dimensions ({lent})."
                        )
                    )
            else:
                setattr(self, attr, dict((uid(i), i) for i in range(lent)))

        if self.measured_results:
            _bitlength = 0
            if self._counts is not None:
                if shots is not None:
                    raise ValueError(
                        "Provide either counts or shots, both is not valid."
                    )
                _bitlength = next(self._counts.elements()).width

            if self._shots is not None:
                _bitlength = self._shots.width

            _process_unitids(c_bits, "c_bits", _bitlength, Bit)

        if self.state_results:
            _n_qubits = 0
            if self._unitary is not None:
                _n_qubits = int(np.log2(self._unitary.shape[-1]))
            elif self._state is not None:
                _n_qubits = get_n_qb_from_statevector(self._state)

            _process_unitids(q_bits, "q_bits", _n_qubits, Qubit)

    def get_bitlist(self) -> List[Bit]:
        """Return sorted list of Bits.

        :raises AttributeError: No Bits in BackendResult.
        :return: Sorted list of Bits.
        :rtype: List[Bit]
        """
        if self.c_bits:
            return _sort_keys_by_val(self.c_bits)
        raise AttributeError

    def get_qbitlist(self) -> List[Qubit]:
        """Return sorted list of Qubits.

        :raises AttributeError: No Qubits in BackendResult.
        :return: Sorted list of Qubits.
        :rtype: List[Qubit]
        """

        if self.q_bits:
            return _sort_keys_by_val(self.q_bits)
        raise AttributeError

    def get_result(
        self, request_ids: Optional[Sequence[UnitID]] = None
    ) -> StoredResult:
        """Retrieve all results, optionally according to a specified UnitID ordering or subset.

        :param request_ids: Ordered set of UnitIDs (Qubit, Bit) for which to
            retrieve results, defaults to None
        :type request_ids: Optional[Sequence[UnitID]], optional
        :raises RuntimeError: Classical bits not set.
        :raises ValueError: Requested (Qu)Bit not in result.
        :raises RuntimeError: "Qubits not set."
        :raises ValueError: For state/unitary results only a permutation of all
            qubits can be requested.
        :return: All stored results corresponding to requested IDs.
        :rtype: StoredResult
        """
        if request_ids is None:
            return StoredResult(self._counts, self._shots, self._state, self._unitary)

        vals: Dict[str, Any] = {}

        if self.measured_results:
            if not self.c_bits:
                raise RuntimeError("Classical bits not set.")
            try:
                chosen_readouts = [self.c_bits[bit] for bit in request_ids]
            except KeyError:
                # if qubits have been specified instead of bits
                if isinstance(request_ids[0], Qubit):
                    chosen_readouts = list(range(len(self.c_bits)))
                else:
                    raise ValueError("Requested (Qu)Bit not in result.")
            if self._counts is not None:
                allcounts = self._counts
                vals["counts"] = reduce(
                    operator.add,
                    (
                        Counter({outcome.choose_indices(chosen_readouts): count})
                        for outcome, count in allcounts.items()
                    ),
                )
            if self._shots is not None:
                vals["shots"] = self._shots.choose_indices(chosen_readouts)

        if self.state_results:
            if not self.q_bits:
                raise RuntimeError("Qubits not set.")
            if not isinstance(request_ids[0], Qubit):
                request_ids = self.get_qbitlist()

            if not _check_permuted_sequence(request_ids, self.q_bits):
                raise ValueError(
                    "For state/unitary results only a permutation of all qubits can be requested."
                )
            qb_mapping = {
                selfqb: request_ids[index] for selfqb, index in self.q_bits.items()
            }
            if self._state is not None:
                vals["state"] = permute_statearray_qb_labels(
                    self._state, self.get_qbitlist(), qb_mapping
                )
            if self._unitary is not None:
                vals["unitary"] = permute_statearray_qb_labels(
                    self._unitary, self.get_qbitlist(), qb_mapping
                )

        return StoredResult(**vals)

    def get_shots(self, cbits: Optional[Sequence[Bit]] = None) -> OutcomeArray:
        """Return shots in an OutcomeArray if available.

        :param cbits: ordered subset of Bits, returns all results by default, defaults to None
        :type cbits: Optional[Sequence[Bit]], optional
        :raises InvalidResultType: Shot results are not available
        :return: OutcomeArray of shots
        :rtype: OutcomeArray
        """
        res = self.get_result(cbits)
        if res.shots is not None:
            return res.shots
        raise InvalidResultType("shots")

    def get_counts(
        self, cbits: Optional[Sequence[Bit]] = None
    ) -> Counter[OutcomeArray]:
        """Return counts of outcomes if available.

        :param cbits: ordered subset of Bits, returns all results by default, defaults to None
        :type cbits: Optional[Sequence[Bit]], optional
        :raises InvalidResultType: Counts are not available
        :return: Counts of outcomes
        :rtype: Counter[OutcomeArray]
        """

        res = self.get_result(cbits)
        if res.counts is not None:
            return res.counts
        if res.shots is not None:
            return res.shots.counts()
        raise InvalidResultType("counts")

    def get_state(self, qbits: Optional[Sequence[Qubit]] = None) -> np.ndarray:
        """Return statevector if available.

        :param qbits: permutation of Qubits, defaults to None
        :type qbits: Optional[Sequence[Qubit]], optional
        :raises InvalidResultType: Statevector not available
        :return: Statevector, (complex 1-D numpy array)
        :rtype: np.ndarray
        """

        res = self.get_result(qbits)
        if res.state is not None:
            return res.state
        if res.unitary is not None:
            return res.unitary[:, 0]
        raise InvalidResultType("state")

    def get_unitary(self, qbits: Optional[Sequence[Qubit]] = None) -> np.ndarray:
        """Return unitary if available.

        :param qbits: permutation of Qubits, defaults to None
        :type qbits: Optional[Sequence[Qubit]], optional
        :raises InvalidResultType: Statevector not available
        :return: Unitary, (complex 2-D numpy array)
        :rtype: np.ndarray
        """

        res = self.get_result(qbits)
        if res.unitary is not None:
            return res.unitary
        raise InvalidResultType("unitary")

    def get_distribution(
        self, units: Optional[Sequence[UnitID]] = None
    ) -> Dict[OutcomeArray, float]:
        """ Calculate an exact or approximate probability distribution over outcomes.

        If the exact statevector is known, the exact probability distribution is
        returned. Otherwise, if measured results are available the distribution
        is estimated from these results.
        """
        try:
            state = self.get_state(units)
            return probs_from_state(state)
        except InvalidResultType:
            counts = self.get_counts(units)
            total = sum(counts.values())
            dist = {outcome: count / total for outcome, count in counts.items()}
            return dist


T = TypeVar("T")


def _sort_keys_by_val(dic: Dict[T, int]) -> List[T]:
    vals, _ = zip(*sorted(dic.items(), key=lambda x: x[1]))
    return list(vals)


def _check_permuted_sequence(first: Collection[Any], second: Collection[Any]) -> bool:
    return len(first) == len(second) and set(first) == set(second)
