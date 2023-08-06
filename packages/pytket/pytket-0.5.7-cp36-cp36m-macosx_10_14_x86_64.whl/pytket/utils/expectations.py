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
from typing import TYPE_CHECKING, Dict, Iterable, Optional, Tuple

import numpy as np
from pytket.circuit import Circuit, Qubit
from pytket.pauli import Pauli, QubitPauliString
from pytket.partition import (
    measurement_reduction,
    PauliPartitionStrat,
    GraphColourMethod,
)
from pytket._tket.simulation import operator_matrix, pauli_tensor_matrix
from pytket.predicates import CompilationUnit

from .measurements import _all_pauli_measurements, append_pauli_measurement
from .results import KwargTypes
from .operators import QubitPauliOperator

if TYPE_CHECKING:
    from pytket.backends.backend import Backend


def expectation_from_shots(shot_table: np.ndarray) -> float:
    """Estimates the expectation value of a circuit from its shots.
    Computes the parity of '1's across all bits to determine a +1 or -1 contribution from each row, and returns the average.

    :param shot_table: The table of shots to interpret.
    :type shot_table: np.ndarray
    :return: The expectation value in the range [-1, 1].
    :rtype: float
    """
    aritysum = 0.0
    for row in shot_table:
        aritysum += np.sum(row) % 2
    return -2 * aritysum / len(shot_table) + 1


def expectation_from_counts(counts: Dict[Tuple[int, ...], int]) -> float:
    """Estimates the expectation value of a circuit from shot counts.
    Computes the parity of '1's across all bits to determine a +1 or -1 contribution from each readout, and returns the weighted average.

    :param counts: Counts of each measurement outcome observed.
    :type counts: Dict[Tuple[int, ...], int]
    :return: The expectation value in the range [-1, 1].
    :rtype: float
    """
    aritysum = 0.0
    total_shots = 0
    for row, count in counts.items():
        aritysum += count * (np.sum(row) % 2)
        total_shots += count
    return -2 * aritysum / total_shots + 1


def _default_index(q: Qubit) -> int:
    if q.reg_name != "q" or len(q.index) != 1:
        raise ValueError("Non-default qubit register")
    return q.index[0]


def get_pauli_expectation_value(
    state_circuit: Circuit,
    pauli: QubitPauliString,
    backend: "Backend",
    n_shots: Optional[int] = None,
) -> complex:
    """Estimates the expectation value of the given circuit with respect to the Pauli term by preparing measurements in the appropriate basis, running on the backend and interpreting the counts/statevector

    :param state_circuit: Circuit that generates the desired state :math:`\\left|\\psi\\right>`.
    :type state_circuit: Circuit
    :param pauli: Pauli operator
    :type pauli: QubitPauliString
    :param backend: pytket backend to run circuit on.
    :type backend: Backend
    :param n_shots: Number of shots to run if backend supports shots/counts. Set to None to calculate using statevector if supported by the backend. Defaults to None
    :type n_shots: Optional[int], optional
    :return: :math:`\\left<\\psi | P | \\psi \\right>`
    :rtype: float
    """
    if not pauli:
        return 1
    if not n_shots:
        if backend.supports_expectation:
            return backend.get_pauli_expectation_value(state_circuit, pauli)
        handle = backend.process_circuit(state_circuit)
        state = backend.get_state(handle)
        op = pauli_tensor_matrix(
            [(_default_index(q), p.name) for q, p in pauli.map.items()],
            state_circuit.n_qubits,
        )
        return np.vdot(state, op.dot(state))
    measured_circ = state_circuit.copy()
    append_pauli_measurement(pauli, measured_circ)
    backend.compile_circuit(measured_circ)
    handle = backend.process_circuit(measured_circ, n_shots)
    if backend.supports_counts:
        counts = backend.get_counts(handle)
        return expectation_from_counts(counts)
    elif backend.supports_shots:
        shot_table = backend.get_shots(handle)
        return expectation_from_shots(shot_table)
    else:
        raise ValueError("Backend does not support counts or shots")


def get_operator_expectation_value(
    state_circuit: Circuit,
    operator: QubitPauliOperator,
    backend: "Backend",
    n_shots: Optional[int] = None,
    partition_strat: Optional[PauliPartitionStrat] = None,
    colour_method: GraphColourMethod = GraphColourMethod.LargestFirst,
    **kwargs: KwargTypes,
) -> complex:
    """Estimates the expectation value of the given circuit with respect to the operator based on its individual Pauli terms.
    If the QubitPauliOperator has symbolic values the expectation value will also be symbolic.
    The input circuit must belong to the default qubit register and have contiguous qubit ordering.

    :param state_circuit: Circuit that generates the desired state :math:`\\left|\\psi\\right>`
    :type state_circuit: Circuit
    :param operator: Operator :math:`H`.
    :type operator: QubitPauliOperator
    :param backend: pytket backend to run circuit on.
    :type backend: Backend
    :param n_shots: Number of shots to run if backend supports shots/counts. None will force the backend to give the full state if available. Defaults to None
    :type n_shots: Optional[int], optional
    :param partition_strat: If retrieving shots, can perform measurement reduction using a chosen strategy
    :type partition_strat: Optional[PauliPartitionStrat], optional
    :return: :math:`\\left<\\psi | H | \\psi \\right>`
    :rtype: complex
    """
    if not n_shots:
        coeffs = operator._dict.values()
        try:
            coeffs = [complex(coeff) for coeff in coeffs]
        except TypeError:
            raise ValueError("Operator contains unevaluated symbols")
        if backend.supports_expectation and (
            backend.expectation_allows_nonhermitian or all(z.imag == 0 for z in coeffs)
        ):
            return backend.get_operator_expectation_value(state_circuit, operator)
        handle = backend.process_circuit(state_circuit)
        state = backend.get_state(handle)
        terms = [(list(p), c) for p, c in operator.terms.items()]
        op = operator_matrix(terms, state_circuit.n_qubits)
        return np.vdot(state, op.dot(state))
    energy: complex
    id_string = QubitPauliString()
    if id_string in operator._dict:
        energy = operator[id_string]
    else:
        energy = 0
    if not partition_strat:
        coeffs = [c for p, c in operator._dict.items() if (p != id_string)]
        pauli_circuits = list(_all_pauli_measurements(operator, state_circuit))
        for c in pauli_circuits:
            backend.compile_circuit(c)
        handles = backend.process_circuits(pauli_circuits, n_shots, **kwargs)
        if backend.supports_counts:
            for handle, coeff in zip(handles, coeffs):
                counts = backend.get_counts(handle)
                energy += coeff * expectation_from_counts(counts)
            return energy
        elif backend.supports_shots:
            for handle, coeff in zip(handles, coeffs):
                shots = backend.get_shots(handle)
                energy += coeff * expectation_from_shots(shots)
            return energy
        else:
            raise ValueError("Backend does not support counts or shots")
    else:
        qubit_pauli_string_list = [p for p in operator._dict.keys() if (p != id_string)]
        measurement_expectation = measurement_reduction(
            qubit_pauli_string_list, partition_strat, colour_method
        )
        # note: this implementation requires storing all the results
        # in memory simultaneously to filter through them.
        measure_circs = []
        for pauli_circ in measurement_expectation.measurement_circs:
            circ = state_circuit.copy()
            circ.append(pauli_circ)
            backend.compile_circuit(circ)
            measure_circs.append(circ)
        handles = backend.process_circuits(measure_circs, n_shots, **kwargs)

        for pauli_string in measurement_expectation.results:
            bitmaps = measurement_expectation.results[pauli_string]
            coeff = operator[pauli_string]
            for bm in bitmaps:
                index = bm.circ_index
                aritysum = 0.0
                if backend.supports_counts:
                    counts = backend.get_counts(handles[index])
                    total_shots = 0
                    for row, count in counts.items():
                        aritysum += count * (np.sum([row[i] for i in bm.bits]) % 2)
                        total_shots += count
                    e = ((-1) ** bm.invert) * coeff * (-2 * aritysum / total_shots + 1)
                    energy += e
                elif backend.supports_shots:
                    shots = backend.get_shots(handles[index])
                    for row in shots:
                        aritysum += np.sum([row[i] for i in bm.bits]) % 2
                    e = ((-1) ** bm.invert) * coeff * (-2 * aritysum / len(shots) + 1)
                    energy += e
                else:
                    raise ValueError("Backend does not support counts or shots")
        return energy
