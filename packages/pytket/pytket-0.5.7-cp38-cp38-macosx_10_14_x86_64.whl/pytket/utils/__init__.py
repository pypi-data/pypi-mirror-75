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
"""Utility functions for performing high-level procedures in pytket"""

from .expectations import (
    expectation_from_shots,
    expectation_from_counts,
    get_pauli_expectation_value,
    get_operator_expectation_value,
)
from .measurements import append_pauli_measurement
from .results import (
    counts_from_shot_table,
    probs_from_counts,
    probs_from_state,
    permute_qubits_in_statevector,
    permute_basis_indexing,
)
from .term_sequence import gen_term_sequence_circuit
from .operators import QubitPauliOperator
from .outcomearray import OutcomeArray
from .graph import Graph
