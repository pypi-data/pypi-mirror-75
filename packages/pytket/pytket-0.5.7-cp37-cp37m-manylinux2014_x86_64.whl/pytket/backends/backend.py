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

""" Abstract base class for all Backend encapsulations."""
import warnings
from abc import ABC, abstractmethod
from typing import Dict, Iterable, List, Optional, Tuple, Union, overload

import numpy as np
from pytket.circuit import BasisOrder, Circuit, OpType
from pytket.device import Device
from pytket.passes import BasePass
from pytket.predicates import Predicate
from pytket.utils.results import KwargTypes, ResultCache, counts_from_shot_table

from .backend_exceptions import (
    CircuitNotValidError,
    InvalidResultType,
    CircuitNotRunError,
)
from .backendresult import BackendResult
from .resulthandle import ResultHandle, _ResultIdTuple
from .status import CircuitStatus


class Backend(ABC):
    """
    This abstract class defines the structure of a backend as something that
    can run quantum circuits and produce output as at least one of shots,
    counts, state, or unitary
    """

    _supports_shots = False
    _supports_counts = False
    _supports_state = False
    _supports_unitary = False
    _supports_expectation = False
    _expectation_allows_nonhermitian = True
    _persistent_handles = False

    def __init__(self) -> None:
        self._cache: Dict[ResultHandle, ResultCache] = {}

    @property
    @abstractmethod
    def required_predicates(self) -> List[Predicate]:
        """
        The minimum set of predicates that a circuit must satisfy before it can
        be successfully run on this backend.

        :return: Required predicates.
        :rtype: List[Predicate]
        """
        ...

    def valid_circuit(self, circuit: Circuit) -> bool:
        """
        Checks that the circuit satisfies all of required_predicates.

        :param circuit: The circuit to check.
        :type circuit: Circuit
        :return: Whether or not all of required_predicates are satisfied.
        :rtype: bool
        """
        return all(pred.verify(circuit) for pred in self.required_predicates)

    def _check_all_circuits(
        self, circuts: Iterable[Circuit], nomeasure_warn: Optional[bool] = None
    ) -> bool:

        if nomeasure_warn is None:
            nomeasure_warn = self.supports_counts or self.supports_shots
        for i, circ in enumerate(circuts):
            errors = (
                CircuitNotValidError(i, repr(pred))
                for pred in self.required_predicates
                if not pred.verify(circ)
            )
            for error in errors:
                raise error
            if nomeasure_warn:
                if circ.n_gates_of_type(OpType.Measure) < 1:
                    warnings.warn(
                        f"Circuit with index {i} in submitted does not contain a measure operation."
                    )
        return True

    @property
    @abstractmethod
    def default_compilation_pass(self) -> BasePass:
        """
        A suggested compilation pass that will guarantee the resulting circuit
        will be suitable to run on this backend with as few preconditions as
        possible.

        :return: Compilation pass guaranteeing required predicates.
        :rtype: BasePass
        """
        ...

    def compile_circuit(self, circuit: Circuit) -> None:
        """Apply the default_compilation_pass to a circuit in place.

        :param circuit: The circuit to compile.
        :type circuit: Circuit
        """
        self.default_compilation_pass.apply(circuit)

    @property
    @abstractmethod
    def _result_id_type(self) -> _ResultIdTuple:
        """Identifier type signature for ResultHandle for this backend.

        :return: Type signature (tuple of hashable types)
        :rtype: _ResultIdTuple
        """
        ...

    def _check_handle_type(self, reshandle: ResultHandle) -> None:
        """Check a result handle is valid for this backend, raises TypeError if not.

        :param reshandle: Handle to check
        :type reshandle: ResultHandle
        :raises TypeError: Types of handle identifiers don't match those of backend.
        """
        if (len(reshandle) != len(self._result_id_type)) or not all(
            isinstance(idval, ty) for idval, ty in zip(reshandle, self._result_id_type)
        ):
            raise TypeError(
                "{0!r} does not match expected identifier types {1}".format(
                    reshandle, self._result_id_type
                )
            )

    @property
    def persistent_handles(self) -> bool:
        """
        Whether the backend produces `ResultHandle` objects that can be reused with other
        instances of the backend class.
        """
        return self._persistent_handles

    def process_circuit(
        self,
        circuit: Circuit,
        n_shots: Optional[int] = None,
        valid_check: bool = True,
        **kwargs: KwargTypes,
    ) -> ResultHandle:
        """
        Submit a single circuit to the backend for running. See :py:meth:`Backend.process_circuits`.
        """
        return self.process_circuits(
            [circuit], n_shots=n_shots, valid_check=valid_check, **kwargs
        )[0]

    @abstractmethod
    def process_circuits(
        self,
        circuits: Iterable[Circuit],
        n_shots: Optional[int] = None,
        valid_check: bool = True,
        **kwargs: KwargTypes,
    ) -> List[ResultHandle]:

        """
        Submit circuits to the backend for running. The results will be stored
        in the backend's result cache to be retrieved by the corresponding
        get_<data> method.

        Use keyword arguments to specify parameters to be used in submitting circuits
        See specific Backend derived class for available parameters, from the following
        list:

        * `seed`: RNG seed for simulators

        :param circuits: Circuits to process on the backend.
        :type circuits: Iterable[Circuit]
        :param n_shots: Number of shots to run per circuit. None is to be used
            for state/unitary simulators. Defaults to None.
        :type n_shots: Optional[int], optional
        :param valid_check: Explicitly check that all circuits satisfy all required
            predicates to run on the backend. Defaults to True
        :type valid_check: bool, optional
        :return: Handles to results for each input circuit, as an interable in
            the same order as the circuits.
        :rtype: List[ResultHandle]
        """
        ...

    @abstractmethod
    def circuit_status(self, handle: ResultHandle) -> CircuitStatus:
        """
        Return a CircuitStatus reporting the status of the circuit execution
        corresponding to the ResultHandle
        """
        ...

    def empty_cache(self) -> None:
        """Manually empty the result cache on the backend.
        """
        self._cache = {}

    def pop_result(self, handle: ResultHandle) -> ResultCache:
        """Remove cache entry corresponding to handle from the cache and return.

        :param handle: ResultHandle object
        :type handle: ResultHandle
        :return: Cache entry corresponding to handle
        :rtype: Any
        """
        return self._cache.pop(handle)

    @property
    def device(self) -> Optional[Device]:
        """Retrieve the Device targeted by the backend if it exists.

        :return: The Device that this backend targets if it exists. The Device
            object contains information about gate errors and device architecture.
        :rtype: Optional[Device]
        """
        raise NotImplementedError("Backend does not support retrieving Device.")

    def get_result(self, handle: ResultHandle, **kwargs: KwargTypes) -> BackendResult:
        """Return a BackendResult corresponding to the handle.

        Use keyword arguments to specify parameters to be used in retrieving results.
        See specific Backend derived class for available parameters, from the following
        list:

        * `timeout`: maximum time to wait for remote job to finish
        * `wait`: polling interval between remote calls to check job status

        :param handle: handle to results
        :type handle: ResultHandle
        :return: Results corresponding to handle.
        :rtype: BackendResult
        """
        self._check_handle_type(handle)
        if handle in self._cache and "result" in self._cache[handle]:
            return self._cache[handle]["result"]
        raise CircuitNotRunError(handle)

    def _get_or_process(self, *args, **kwargs) -> Tuple[BackendResult, ResultHandle]:
        if isinstance(args[0], Circuit):
            handle = self.process_circuits([args[0]], **kwargs)[0]
            warnings.warn(
                (
                    "Calling `get_<result_type>` methods with `Circuit` is deprecated: "
                    "use `ResultHandle` instead. "
                    "Make sure you are not running a `Circuit` twice by calling "
                    "`process_circuits` and `get_<result_type>`."
                ),
                DeprecationWarning,
            )
        elif isinstance(args[0], ResultHandle):
            handle = args[0]
            self._check_handle_type(handle)

        else:
            raise TypeError(
                (
                    "Provide either a Circuit to run or a ResultHandle"
                    "to a previously submitted circuit."
                )
            )
        return self.get_result(handle, **kwargs), handle

    @property
    def supports_shots(self) -> bool:
        """Does this backend support shot result retrieval via `get_shots`."""
        return self._supports_shots

    @overload
    def get_shots(
        self,
        circuit: Circuit,
        n_shots: int,
        basis: BasisOrder = BasisOrder.ilo,
        valid_check: bool = True,
        **kwargs: KwargTypes,
    ) -> np.ndarray:
        ...

    @overload
    def get_shots(
        self,
        circuit: ResultHandle,
        n_shots: Optional[
            int
        ] = None,  # ignored optional parameter required to make overload work
        basis: BasisOrder = BasisOrder.ilo,
    ) -> np.ndarray:
        ...

    def get_shots(
        self,
        circuit: Union[Circuit, ResultHandle],
        n_shots: Optional[int] = None,
        basis: BasisOrder = BasisOrder.ilo,
        valid_check: bool = True,
        **kwargs: KwargTypes,
    ) -> np.ndarray:
        """Obtain the table of shots from an experiment. Can either accept a :py:class:`~pytket.backends.resulthandle.ResultHandle` for a processed circuit
        to retrieve the data from the backend's cache, or a
        :py:class:`~pytket.circuit.Circuit` to be run and immediately returned. This
        will fail if the circuit does not match the device's requirements.

        Calling this method with a :py:class:`~pytket.circuit.Circuit` is deprecated:
        please use a :py:class:`~pytket.backends.resulthandle.ResultHandle` instead. In
        particular, :py:class:`~pytket.backends.resulthandle.ResultHandle` must be used
        after a call to :py:meth:`~process_circuits`.

        :param circuit: The circuit to run, or results to retrieve
        :type circuit: Union[Circuit, ResultHandle]
        :param n_shots: Number of shots to generate from the circuit. Defaults to None
        :type n_shots: Optional[int], optional
        :param basis: Toggle between ILO (increasing lexicographic order of bit ids) and
            DLO (decreasing lexicographic order) for column ordering. Defaults to
            BasisOrder.ilo.
        :type basis: BasisOrder, optional
        :param valid_check: Explicitly check that the circuit satisfies all of the
            required predicates before running. Defaults to True
        :type valid_check: bool, optional
        :raises NotImplementedError: If backend implementation does not support shot
            table retrieval
        :return: Table of shot results. Each row is a single shot, with columns ordered
            by classical bit order (according to `basis`). Entries are 0 or 1
            corresponding to qubit basis states.
        :rtype: np.ndarray
        """
        result, _ = self._get_or_process(
            circuit, n_shots=n_shots, valid_check=valid_check, **kwargs
        )
        c_bits = (
            sorted(result.c_bits.keys(), reverse=(basis is not BasisOrder.ilo))
            if result.c_bits
            else None
        )
        return result.get_shots(c_bits).to_readouts()

    @property
    def supports_counts(self) -> bool:
        """Does this backend support counts result retrieval via `get_counts`."""
        return self._supports_counts

    @overload
    def get_counts(
        self,
        circuit: Circuit,
        n_shots: int,
        basis: BasisOrder = BasisOrder.ilo,
        valid_check: bool = True,
        **kwargs: KwargTypes,
    ) -> Dict[Tuple[int, ...], int]:
        ...

    @overload
    def get_counts(
        self,
        circuit: ResultHandle,
        n_shots: Optional[
            int
        ] = None,  # ignored optional parameter required to make overload work
        basis: BasisOrder = BasisOrder.ilo,
    ) -> Dict[Tuple[int, ...], int]:
        ...

    def get_counts(
        self,
        circuit: Union[Circuit, ResultHandle],
        n_shots: Optional[int] = None,
        basis: BasisOrder = BasisOrder.ilo,
        valid_check: bool = True,
        **kwargs: KwargTypes,
    ) -> Dict[Tuple[int, ...], int]:
        """Obtain a summary of results, accumulating the shots for each result from an
        experiment. Can either accept a
        :py:class:`~pytket.backends.resulthandle.ResultHandle` for a processed circuit
        to retrieve the data from the backend's cache, or a
        :py:class:`~pytket.circuit.Circuit` to be run and immediately returned. This
        will fail if the circuit does not match the device's requirements.

        Calling this method with a :py:class:`~pytket.circuit.Circuit` is deprecated:
        please use a :py:class:`~pytket.backends.resulthandle.ResultHandle` instead. In
        particular, :py:class:`~pytket.backends.resulthandle.ResultHandle` must be used
        after a call to :py:meth:`~process_circuits`.

        :param circuit: The circuit to run, or results to retrieve
        :type circuit: Union[Circuit, ResultHandle]
        :param n_shots: Number of shots to generate from the circuit. Defaults to None
        :type n_shots: Optional[int], optional
        :param basis: Toggle between ILO (increasing lexicographic order of bit ids) and
            DLO (decreasing lexicographic order) for column ordering. Defaults to
            BasisOrder.ilo.
        :type basis: BasisOrder, optional
        :param valid_check: Explicitly check that the circuit satisfies all of the
            required predicates before running. Defaults to True
        :type valid_check: bool, optional
        :raises NotImplementedError: If backend implementation does not support counts
            retrieval
        :return: Dictionary mapping observed readouts to the number of times observed.
        :rtype: Dict[Tuple[int, ...], int]
        """

        result, _ = self._get_or_process(
            circuit, n_shots=n_shots, valid_check=valid_check, **kwargs
        )
        c_bits = (
            sorted(result.c_bits.keys(), reverse=(basis is not BasisOrder.ilo))
            if result.c_bits
            else None
        )
        try:
            return {
                tuple(outcome.to_readouts()[0]): count
                for outcome, count in result.get_counts(c_bits).items()
            }
        except InvalidResultType:
            shots = self.get_shots(
                circuit, n_shots=n_shots, basis=basis, valid_check=valid_check, **kwargs
            )
            return counts_from_shot_table(shots)

    @property
    def supports_state(self) -> bool:
        """Does this backend support statevector retrieval via `get_state`."""
        return self._supports_state

    @overload
    def get_state(
        self,
        circuit: Circuit,
        basis: BasisOrder = BasisOrder.ilo,
        valid_check: bool = True,
    ) -> np.ndarray:
        ...

    @overload
    def get_state(
        self, circuit: ResultHandle, basis: BasisOrder = BasisOrder.ilo
    ) -> np.ndarray:
        ...

    def get_state(
        self,
        circuit: Union[Circuit, ResultHandle],
        basis: BasisOrder = BasisOrder.ilo,
        valid_check: bool = True,
    ) -> np.ndarray:
        """Obtain a statevector from a simulation. Can either accept a
        :py:class:`~pytket.backends.resulthandle.ResultHandle` for a processed circuit
        to retrieve data from the backend's cache, or a
        :py:class:`~pytket.circuit.Circuit` to be run and immediately returned. This
        will fail if the circuit does not match the simulator's requirements.

        Calling this method with a :py:class:`~pytket.circuit.Circuit` is deprecated:
        please use a :py:class:`~pytket.backends.resulthandle.ResultHandle` instead. In
        particular, :py:class:`~pytket.backends.resulthandle.ResultHandle` must be used
        after a call to :py:meth:`~process_circuits`.

        :param circuit: The circuit to run, or results to retrieve
        :type circuit: Union[Circuit, ResultHandle]
        :param basis: Toggle between ILO-BE (increasing lexicographic order of bit ids,
            big-endian) and DLO-BE (decreasing lexicographic order, big-endian) for
            ordering the coefficients. Defaults to BasisOrder.ilo.
        :type basis: BasisOrder, optional
        :param valid_check: Explicitly check that the circuit satisfies all of the
            required predicates before running. Defaults to True
        :type valid_check: bool, optional
        :raises NotImplementedError: If backend implementation does not support
            statevector retrieval
        :return: A big-endian statevector for the circuit in the encoding given by
            `basis`; e.g. :math:`[a_{00}, a_{01}, a_{10}, a_{11}]` where :math:`a_{01}`
            is the amplitude of the :math:`\\left|01\\right>` state (in ILO, this means
            qubit q[0] is in state :math:`\\left|0\\right>` and q[1] is in state
            :math:`\\left|1\\right>`, and the reverse in DLO)
        :rtype: np.ndarray
        """

        result, _ = self._get_or_process(circuit, valid_check=valid_check)
        q_bits = (
            sorted(result.q_bits.keys(), reverse=(basis is not BasisOrder.ilo))
            if result.q_bits
            else None
        )
        return result.get_state(q_bits)

    @property
    def supports_unitary(self) -> bool:
        """Does this backend support unitary retrieval via `get_unitary`."""
        return self._supports_unitary

    @property
    def supports_expectation(self) -> bool:
        """Does this backend support expectation value calculation for operators."""
        return self._supports_expectation

    @property
    def expectation_allows_nonhermitian(self) -> bool:
        """If expectations are supported, is the operator allowed to be non-Hermitan?"""
        return self._expectation_allows_nonhermitian
