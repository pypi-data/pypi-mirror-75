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
"""Parser from OPENQASM to :math:`\\mathrm{t|ket}\\rangle` Circuits"""

__path__ = __import__("pkgutil").extend_path(__path__, __name__)

from .qasm import (
    circuit_from_qasm,
    circuit_to_qasm,
    circuit_from_qasm_str,
    circuit_to_qasm_str,
    circuit_from_qasm_io,
    circuit_to_qasm_io,
)
