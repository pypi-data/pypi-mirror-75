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
import math
from typing import (
    TYPE_CHECKING,
    Any,
    Counter,
    Dict,
    List,
    Optional,
    Sequence,
    Tuple,
    Union,
)

import numpy as np
from pytket.circuit import BasisOrder
from pytket.utils.outcomearray import OutcomeArray

if TYPE_CHECKING:
    from pytket.circuit import Circuit, Qubit

StateTuple = Tuple[int, ...]
CountsDict = Dict[StateTuple, int]
KwargTypes = Union[int, float, None]
ResultCache = Dict[str, Any]


class BitPermuter:
    """Class for permuting the bits in an integer

    Enables inverse permuation and uses caching to speed up common uses.

    """

    def __init__(self, permutation: Tuple[int, ...]):
        """Constructor

        :param permutation: Map from current bit index (big-endian) to its new position, encoded as a list.
        :type permutation: Tuple[int, ...]
        :raises ValueError: Input permutation is not valid complete permutation
        of all bits
        """
        if sorted(permutation) != list(range(len(permutation))):
            raise ValueError("Permutation is not a valid complete permutation.")
        self.perm = tuple(permutation)
        self.n_bits = len(self.perm)
        self.int_maps: Tuple[Dict[int, int], Dict[int, int]] = ({}, {})

    def permute(self, val: int, inverse: bool = False) -> int:
        """Return input with bit values permuted.

        :param val: input integer
        :type val: int
        :param inverse: whether to use the inverse permutation, defaults to False
        :type inverse: bool, optional
        :return: permuted integer
        :rtype: int
        """
        perm_map, other_map = self.int_maps[:: (-1) ** inverse]
        if val in perm_map:
            return perm_map[val]

        res = 0
        for source_index, target_index in enumerate(self.perm):
            if inverse:
                target_index, source_index = source_index, target_index
            # if source bit set
            if val & (1 << (self.n_bits - 1 - source_index)):
                # set target bit
                res |= 1 << (self.n_bits - 1 - target_index)

        perm_map[val] = res
        other_map[res] = val
        return res

    def permute_all(self) -> List:
        """Permute all integers within bit-width specified by permutation.

        :return: List of permuted outputs.
        :rtype: List
        """
        return list(map(self.permute, range(1 << self.n_bits)))


def change_basis_of_permutation(permutation: Tuple[int, ...]) -> Tuple[int, ...]:
    """Given permutation of indices under one BasisOrder (ilo/dlo), gives the
    same functional permutation with respect to the indices of the other (dlo/
    ilo), e.g. mapping [1, 0, 2] to [0, 2, 1].

    :param permutation: Permutation of indices
    :type permutation: Tuple[int, ...]
    :return: The same permutation, but with respect to the other BasisOrder
    :rtype: Tuple[int, ...]
    """
    return tuple(len(permutation) - 1 - index for index in permutation[::-1])


def counts_from_shot_table(shot_table: np.ndarray) -> Dict[Tuple[int, ...], int]:
    """Summarises a shot table into a dictionary of counts for each observed outcome.

    :param shot_table: Table of shots from a pytket backend.
    :type shot_table: np.ndarray
    :return: Dictionary mapping observed readouts to the number of times observed.
    :rtype: Dict[Tuple[int, ...], int]
    """
    shot_values, counts = np.unique(shot_table, axis=0, return_counts=True)
    return {tuple(s): c for s, c in zip(shot_values, counts)}


def shots_from_counter(counts: Counter[OutcomeArray]) -> OutcomeArray:
    """Generate artificial shot table from counter of outcomes"""

    unroll_counts = list(counts.elements())
    return OutcomeArray(unroll_counts, unroll_counts[0].width)


def probs_from_counts(
    counts: Dict[Tuple[int, ...], int]
) -> Dict[Tuple[int, ...], float]:
    """Converts raw counts of observed outcomes into the observed probability distribution.

    :param counts: Dictionary mapping observed readouts to the number of times observed.
    :type counts: Dict[Tuple[int, ...], int]
    :return: Probability distribution over observed readouts.
    :rtype: Dict[Tuple[int, ...], float]
    """
    total = np.sum([c for _, c in counts.items()])
    return {outcome: c / total for outcome, c in counts.items()}


def _index_to_outcome(
    index: int, width: int, basis: BasisOrder = BasisOrder.ilo
) -> OutcomeArray:
    return OutcomeArray.from_readouts(
        [
            list(
                (index >> i) & 1
                for i in range(width)[:: (-1) ** (basis == BasisOrder.ilo)]
            )
        ]
    )


def _reverse_bits_of_index(index: int, width: int) -> int:
    """Reverse bits of a readout/statevector index to change :py:class:`BasisOrder`.
    Values in tket are ILO-BE (2 means [bit0, bit1] == [1, 0]).
    Values in qiskit are DLO-BE (2 means [bit1, bit0] == [1, 0]).
    Note: Since ILO-BE (DLO-BE) is indistinguishable from DLO-LE (ILO-LE), this can also be seen as changing the endianness of the value.
    
    :param n: Value to reverse
    :type n: int
    :param width: Number of bits in bitstring
    :type width: int
    :return: Integer value of reverse bitstring
    :rtype: int
    """
    permuter = BitPermuter(tuple(range(width - 1, -1, -1)))
    return permuter.permute(index)


def probs_from_state(state: np.ndarray) -> Dict[OutcomeArray, float]:
    """
    Converts statevector to the probability distribution over readouts in the
    computational basis. Ignores probabilities lower than 1e-10.

    :param state: Full statevector with big-endian encoding.
    :type state: np.ndarray
    :return: Probability distribution over readouts.
    :rtype: Dict[OutcomeArray, float]
    """
    width = get_n_qb_from_statevector(state)
    state /= np.sqrt(state.conjugate().dot(state))
    probs = {
        _index_to_outcome(i, width): abs(coeff) ** 2
        for i, coeff in enumerate(state)
        if abs(coeff) ** 2 >= 1e-10
    }
    if not math.isclose(np.sum([p for _, p in probs.items()]), 1.0):
        raise ValueError("Statevector is not normalised")
    return probs


def sample_from_state(
    state: np.ndarray, n_shots: int, seed: Optional[int] = None
) -> OutcomeArray:
    """Converts statevector to artificial shots by sampling.

    :param state: Complex Statevector
    :type state: np.ndarray
    :param n_shots: Number of shots to sample
    :type n_shots: int
    :return: Artificial shots OutcomeArray
    :rtype: OutcomeArray
    """
    choices, probs = zip(*probs_from_state(state).items())
    width = choices[0].width
    np.random.seed(seed)
    sample_indices = np.random.choice(len(choices), p=probs, size=n_shots)
    return OutcomeArray(np.vstack([choices[i] for i in sample_indices]), width)


def get_n_qb_from_statevector(state: np.ndarray) -> int:
    """Given a statevector, returns the number of qubits described

    :param state: Statevector to inspect
    :type state: np.ndarray
    :raises ValueError: If the dimension of the statevector is not a power of 2
    :return: `n` such that `len(state) == 2 ** n`
    :rtype: int
    """
    n_qb = int(np.log2(state.shape[0]))
    if 2 ** n_qb != state.shape[0]:
        raise ValueError("Size is not a power of 2")
    return n_qb


def _assert_compatible_state_permutation(
    state: np.ndarray, permutation: Tuple[int, ...]
):
    """Asserts that a statevector and a permutation list both refer to the same number of qubits

    :param state: Statevector
    :type state: np.ndarray
    :param permutation: Permutation of qubit indices, encoded as a list.
    :type permutation: Tuple[int, ...]
    :raises ValueError: [description]
    """
    n_qb = len(permutation)
    if 2 ** n_qb != state.shape[0]:
        raise ValueError("Invalid permutation: length does not match number of qubits")


def permute_qubits_in_statevector(
    state: np.ndarray, permutation: Tuple[int, ...]
) -> np.ndarray:
    """Rearranges a statevector according to a permutation of the qubit indices.

    :param state: Original statevector.
    :type state: np.ndarray
    :param permutation: Map from current qubit index (big-endian) to its new position, encoded as a list.
    :type permutation: Tuple[int, ...]
    :return: Updated statevector.
    :rtype: np.ndarray
    """
    _assert_compatible_state_permutation(state, permutation)
    permuter = BitPermuter(permutation)
    return state[permuter.permute_all()]


def permute_basis_indexing(
    matrix: np.ndarray, permutation: Tuple[int, ...]
) -> np.ndarray:
    """Rearranges the first dimensions of an array (statevector or unitary)
     according to a permutation of the bit indices in the binary representation
     of row indices.

    :param matrix: Original unitary matrix
    :type matrix: np.ndarray
    :param permutation: Map from current qubit index (big-endian) to its new position, encoded as a list
    :type permutation: Tuple[int, ...]
    :return: Updated unitary matrix
    :rtype: np.ndarray
    """
    _assert_compatible_state_permutation(matrix, permutation)
    permuter = BitPermuter(permutation)

    return matrix[permuter.permute_all(), ...]


def permute_rows_cols_in_unitary(
    matrix: np.ndarray, permutation: Tuple[int, ...]
) -> np.ndarray:
    """Rearranges the rows of a unitary matrix according to a permutation of the qubit indices.

    :param matrix: Original unitary matrix
    :type matrix: np.ndarray
    :param permutation: Map from current qubit index (big-endian) to its new position, encoded as a list
    :type permutation: Tuple[int, ...]
    :return: Updated unitary matrix
    :rtype: np.ndarray
    """
    _assert_compatible_state_permutation(matrix, permutation)
    permuter = BitPermuter(permutation)
    all_perms = permuter.permute_all()
    permat = matrix[:, all_perms]
    permat = permat[all_perms, :]
    return permat


def generate_permutation_matrix(permutation: Tuple[int, ...]) -> np.ndarray:
    """Generates a unitary corresponding to the permutation of qubits.

    :param permutation: Map from current qubit index (big-endian) to its new position, encoded as a list
    :type permutation: Tuple[int, ...]
    :rtype: np.ndarray
    """

    identity = np.eye(1 << len(permutation))
    return permute_basis_indexing(identity, permutation)


def reverse_permutation_matrix(n_qubits: int) -> np.ndarray:
    """Returns a permutation matrix to reverse the order of qubits.

    :param n_qubits: Number of qubits in system
    :type n_qubits: int
    :return: Permutation matrix
    :rtype: np.ndarray
    """
    rev_perm = tuple(range(n_qubits - 1, -1, -1))
    return generate_permutation_matrix(rev_perm)


def permute_statearray_qb_labels(
    array: np.ndarray,
    original_labeling: Sequence["Qubit"],
    relabling_map: Dict["Qubit", "Qubit"],
) -> np.ndarray:
    """Permute statevector/unitary according to a relabelling of Qubits.

    :param array: The statevector or unitary
    :type array: np.ndarray
    :param original_labeling: A sequence of qubits in the order corresponding to
    the existing indexing.
    :type original_labeling: Sequence[Qubit]
    :param relabling_map: Map from original Qubits to new.
    :type relabling_map: Dict[Qubit, Qubit]
    :return: Permuted array.
    :rtype: np.ndarray
    """
    permutation = [0] * len(original_labeling)
    for i, orig_qb in enumerate(original_labeling):
        permutation[i] = original_labeling.index(relabling_map[orig_qb])
    permuter = (
        permute_basis_indexing
        if len(array.shape) == 1
        else permute_rows_cols_in_unitary
    )
    return permuter(array, tuple(permutation))


def compare_statevectors(first: np.ndarray, second: np.ndarray) -> bool:
    """Check approximate equality up to global phase for statevectors.

    :param first: First statevector.
    :type first: np.ndarray
    :param second: Second statevector.
    :type second: np.ndarray
    :return: Approximate equality.
    :rtype: bool
    """
    return np.isclose(np.abs(np.vdot(first, second)), 1)


def compare_unitaries(first: np.ndarray, second: np.ndarray) -> bool:
    """Check approximate equality up to global phase for unitaries.

    :param first: First unitary.
    :type first: np.ndarray
    :param second: Second unitary.
    :type second: np.ndarray
    :return: Approximate equality.
    :rtype: bool
    """
    conjug_prod = first @ second.conjugate().transpose()
    identity = np.identity(conjug_prod.shape[0], dtype=complex)
    return np.allclose(conjug_prod, identity * conjug_prod[0, 0])
