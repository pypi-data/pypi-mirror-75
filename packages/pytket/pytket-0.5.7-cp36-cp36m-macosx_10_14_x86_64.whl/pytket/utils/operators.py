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

from pytket.pauli import Pauli, QubitPauliString
from pytket.circuit import Qubit
from typing import Dict
from sympy import Symbol, sympify, Expr
from openfermion import QubitOperator


class QubitPauliOperator:
    """Generic data structure for generation of ansätze and expectation value calculation.
    Contains a dictionary from QubitPauliString to sympy Expr.
    """

    def __init__(self, dictionary: Dict[QubitPauliString, Expr] = None):
        self._dict = dict()
        if dictionary:
            self._dict = dict(
                (key, sympify(value)) for key, value in dictionary.items()
            )

    def __repr__(self):
        return self._dict.__repr__()

    def __getitem__(self, key):
        return self._dict[key]

    def __setitem__(self, key, value):
        self._dict[key] = sympify(value)

    def __getstate__(self):
        return self._dict

    def __setstate__(self, _dict):
        # values assumed to be already sympified
        self._dict = _dict

    def subs(self, symbol_dict: Dict[Symbol, complex]):
        for key, value in self._dict.items():
            self._dict[key] = value.subs(symbol_dict)

    def to_OpenFermion(self):
        op = QubitOperator()
        for key, value in self._dict.items():
            qubit_string = ""
            for qubit, tket_pauli in key.map.items():
                if qubit.reg_name != "q":
                    raise ValueError("Qubit register must have default name.")
                index = qubit.index
                if len(index) != 1:
                    raise ValueError("Qubit register must be 1-dimensional.")
                if tket_pauli != Pauli.I:
                    pauli = tket_pauli.name
                    qubit_string += pauli + str(index[0]) + " "
            coeff = complex(
                value
            )  # raises exception if value has un-substituted symbols
            op += QubitOperator(qubit_string, coeff)
        return op

    @classmethod
    def from_OpenFermion(cls, openf_op: QubitOperator):
        tk_op = dict()
        for term, coeff in openf_op.terms.items():
            string = QubitPauliString()
            for qubitnum, paulisym in term:
                qb = Qubit(qubitnum)
                pauli = _STRING_TO_PAULI[paulisym]
                string.map[qb] = pauli
            tk_op[string] = coeff
        return cls(tk_op)


_STRING_TO_PAULI = {
    "I": Pauli.I,
    "X": Pauli.X,
    "Y": Pauli.Y,
    "Z": Pauli.Z,
}
