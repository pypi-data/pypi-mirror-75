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

from .operators import QubitPauliOperator
from pytket import Circuit, Qubit
from pytket.circuit import PauliExpBox, CircBox
from pytket.pauli import Pauli
from pytket.partition import (
    term_sequence,
    PauliPartitionStrat,
    GraphColourMethod,
)
from typing import Optional


def gen_term_sequence_circuit(
    operator: QubitPauliOperator,
    reference_state: Circuit,
    partition_strat: PauliPartitionStrat = PauliPartitionStrat.CommutingSets,
    colour_method: GraphColourMethod = GraphColourMethod.Lazy,
) -> Circuit:
    """Sequences QubitPauliOperator terms to generate a circuit made of CircBoxes.
    Each CircBox contains a sequence of PauliExpBox objects.

    :param operator: The operator terms to sequence
    :type operator: QubitPauliOperator
    :param reference_state: reference state to add sequenced terms to.
    :type reference_state: Circuit
    :param partition_strat: a Partition strategy
    :type partition_strat: PauliPartitionStrat, optional
    """
    qps_list = list(operator._dict.keys())
    qps_list_list = term_sequence(qps_list, partition_strat, colour_method)
    n_qbs = reference_state.n_qubits
    circ = reference_state.copy()
    qbs = circ.qubits
    for out_qps_list in qps_list_list:
        circ_to_box = Circuit(n_qbs)
        for qps in out_qps_list:
            coeff = operator[qps]
            qubits = list()
            paulis = list()
            for qb, pauli in qps.map.items():
                qubits.append(qb)
                paulis.append(pauli)
            pbox = PauliExpBox(paulis, coeff)
            circ_to_box.add_pauliexpbox(pbox, qubits)
        cbox = CircBox(circ_to_box)
        circ.add_circbox(cbox, qbs)
    return circ
