import itertools
import operator
from collections import OrderedDict
from functools import lru_cache, reduce
from typing import Dict, Iterable, List, Tuple

import numpy as np
from scipy import sparse
from scipy.optimize import minimize
from pytket.circuit import Circuit, OpType, Qubit, Bit, Node
from pytket.utils.results import BitPermuter, CountsDict, StateTuple

MeasurementMap = Dict[Qubit, Bit]
ResultsMap = Dict[Node, int]


def compress_counts(
    counts: Dict[StateTuple, float], tol: float = 1e-6, round_to_int: bool = False
) -> CountsDict:
    """Filter counts to remove states that have a count value (which can be a floating-
    point number) below a tolerance, and optionally round to an integer.

    :param counts: Input counts
    :type counts: Dict[StateTuple, float]
    :param tol: Value below which counts are pruned. Defaults to 1e-6.
    :type tol: float, optional
    :param round_to_int: Whether to round each count to an integer. Defaults to False.
    :type round_to_int: bool, optional
    :return: Filtered counts
    :rtype: CountsDict
    """
    valprocess = (lambda x: int(round(x))) if round_to_int else (lambda x: x)
    processed_pairs = (
        (key, valprocess(val)) for key, val in counts.items() if val > tol
    )
    return {key: val for key, val in processed_pairs if val > 0}


@lru_cache(maxsize=128)
def binary_to_int(bintuple: Tuple[int]) -> int:
    """Convert a binary tuple to corresponding integer, with most significant bit as the first element of tuple.

    :param bintuple: Binary tuple
    :type bintuple: Tuple[int]
    :return: Integer
    :rtype: int
    """
    integer = 0
    for index, bitset in enumerate(reversed(bintuple)):
        if bitset:
            integer |= 1 << index
    return integer


@lru_cache(maxsize=128)
def int_to_binary(val: int, dim: int) -> Tuple[int]:
    """Convert an integer to corresponding binary tuple, with most significant bit as the first element of tuple.

    :param val: input integer
    :type val: int
    :param dim: Bit width
    :type dim: int
    :return: Binary tuple of width dim
    :rtype: Tuple[int]
    """
    return tuple(map(int, format(val, "0{}b".format(dim))))


def _get_measure_map(circ: Circuit) -> MeasurementMap:
    return {com.args[0]: com.args[1] for com in circ if com.op.type == OpType.Measure}


def _minimise_correct(
    matrix: sparse.csc_matrix, input_vector: np.ndarray, tol: float = 1e-6
):
    def least_squares_dif(trial_vec):
        diff = matrix.dot(trial_vec) - input_vector
        return diff.dot(diff)

    initial_trial = input_vector.copy()
    normalisation = {"type": "eq", "fun": lambda x: 1 - np.sum(x)}
    bounds = ((0.0, 1.0),) * len(initial_trial)
    minimiser = minimize(
        least_squares_dif,
        initial_trial,
        method="SLSQP",
        constraints=normalisation,
        bounds=bounds,
        tol=tol,
    )
    return minimiser.x


def _invert_correct(matrix: sparse.csr_matrix, input_vector: np.ndarray):
    invert = sparse.linalg.inv(sparse.csc_matrix(matrix))
    return invert.dot(input_vector)


def _bayesian_iterative_correct(
    error_matrix: sparse.csr_matrix,
    measurements: np.ndarray,
    tol: float = 1e-5,
    max_it: int = None,
):
    # based on method found in https://arxiv.org/abs/1910.00129

    vector_size = measurements.size
    # uniform initial
    true_states = np.full(vector_size, 1 / vector_size)
    prev_true = true_states.copy()
    converged = False
    error_matrix_T = error_matrix.transpose()
    count = 0
    while not converged:
        if max_it:
            if count >= max_it:
                break
            count += 1
        trial_measurements = error_matrix.dot(true_states)
        true_states *= error_matrix_T.dot(measurements / trial_measurements)
        converged = np.allclose(true_states, prev_true, atol=tol)
        prev_true = true_states.copy()

    return true_states


class SpamCorrecter:
    """A class for generating "state preparation and measurement" (SPAM) calibration
    experiments for ``pytket`` backends, and correcting counts generated from them.

    Supports saving calibrated state to a dictionary format, and restoring from the
    dictionary.

    """

    def __init__(self, qubit_subsets: List[List[Node]]):
        """Construct a new `SpamCorrecter`.

        :param qubit_subsets: A list of lists of correlated Nodes of a `Device`.
            Qubits within the same list are assumed to only have SPAM errors correlated
            with each other. Thus to allow SPAM errors between all qubits you should
            provide a single list.
        :type qubit_subsets: List[List[Node]]
        :raises ValueError: There are repeats in the `qubit_subsets` specification.
        """
        self.all_qbs = [qb for subset in qubit_subsets for qb in subset]

        if len(self.all_qbs) != len(set(self.all_qbs)):
            raise ValueError("Qubit subsets are not mutually disjoint.")

        self.subsets_matrix_map = OrderedDict.fromkeys(
            sorted(map(tuple, qubit_subsets), key=len, reverse=True)
        )
        self._subset_dimensions = [len(subset) for subset in self.subsets_matrix_map]
        # create base circuit with
        self._base_circuit = Circuit()
        self.c_reg = []
        for index, qb in enumerate(self.all_qbs):
            self._base_circuit.add_qubit(qb)
            c_bit = Bit(index)
            self.c_reg.append(c_bit)
            self._base_circuit.add_bit(c_bit)

        self._prepared_states = None
        self.prep_to_meas_sparse = None

    def calibration_circuits(self) -> List[Circuit]:
        """Generate calibration circuits according to the specified correlations.

        :return: A list of calibration circuits to be run on the machine. Results from
            these circuits must be given back to this class (via the
            `calculate_matrices` methos) in the same order.
        :rtype: List[Circuit]
        """
        major_state_dimensions = self._subset_dimensions[0]
        n_circuits = 1 << major_state_dimensions
        circuits = []
        self._prepared_states = []
        for major_state_index in range(n_circuits):
            circ = self._base_circuit.copy()
            # get bit string corresponding to basis state of biggest subset of qubits
            major_state = int_to_binary(major_state_index, major_state_dimensions)
            new_state_dicts = {}
            for dim, qubits in zip(self._subset_dimensions, self.subsets_matrix_map):
                new_state_dicts[qubits] = major_state[:dim]
                for flipped_qb in itertools.compress(qubits, major_state[:dim]):
                    circ.X(flipped_qb)
            circ.add_barrier(self.all_qbs)
            for qb, cb in zip(self.all_qbs, self.c_reg):
                circ.Measure(qb, cb)
            circuits.append(circ)

            self._prepared_states.append(new_state_dicts)

        return circuits

    def calculate_matrices(self, counts_list: List[CountsDict]):
        """Calculate the calibration matrices from the results of running calibration
        circuits.

        :param counts_list: List of result counts. Must be in the same order as the
            corresponding circuits generated by `calibration_circuits`.
        :type counts_list: List[CountsDict]
        :raises RuntimeError: Calibration circuits have not been generated yet.
        """
        if self._prepared_states is None:
            raise RuntimeError(
                "Ensure calibration states/circuits have been calculated first."
            )
        for qbs, dim in zip(self.subsets_matrix_map, self._subset_dimensions):
            self.subsets_matrix_map[qbs] = np.zeros((1 << dim,) * 2, dtype=float)

        for counts_dict, state_dict in zip(counts_list, self._prepared_states):
            for measured_state, count in counts_dict.items():
                for qb_sub in self.subsets_matrix_map:
                    measured_subset_state = measured_state[: len(qb_sub)]
                    measured_state = measured_state[len(qb_sub) :]

                    prepared_state_index = binary_to_int(state_dict[qb_sub])
                    measured_state_index = binary_to_int(measured_subset_state)
                    self.subsets_matrix_map[qb_sub][
                        measured_state_index, prepared_state_index
                    ] += count

        self.prep_to_meas_sparse = self.calculate_sparse_mat(
            self.subsets_matrix_map.values()
        )

    @staticmethod
    def calculate_sparse_mat(mat_it: Iterable[np.array]) -> sparse.csr_matrix:
        """Convert calibration matrices for subsets into a sparse Kronecker product.

        :param mat_it: Iterable of qubit-subset calibration matrices.
        :type mat_it: Iterable[np.array]
        :return: Sparse tensor-product matrix
        :rtype: sparse.csr_matrix
        """
        normalised_mats = (mat / np.sum(mat, axis=0) for mat in mat_it)
        return sparse.csr_matrix(reduce(sparse.kron, normalised_mats))

    def correct_counts(
        self,
        counts: CountsDict,
        res_map: ResultsMap,
        method: str = "minimise",
        options: Dict = {},
    ) -> CountsDict:
        """Correct results counts from calibrated backend according to calibration data,
        using the specified method.

        :param counts: Input counts
        :type counts: CountsDict
        :param res_map: Dictionary mapping each calibrated `Node` of the backend to the
            position in the `counts` state tuple corresponding to the result from that
            qubit.
        :type res_map: ResultsMap
        :param method: Method to use for calculating the corrected counts.
            Options are:

            * "minimise" (default): use a numeric optimisation algorithm to
              approximately invert the calibration matrix.
            * "bayesian": Use an iterative Bayesian technique to converge to the
              corrected counts.
            * "invert": Invert the whole calibration matrix (costly).
        :type method: str, optional
        :param options: Options for the method. Possible options are:

            * "tol": Convergence tolerance (for "minimise" and "bayesian" methods).
            * "maxiter": Number of iterations before terminating if convergence is not
              reached (for "bayesian" method).
        :type options: Dict, optional
        :raises RuntimeError: Calibration matrix has not been calculated, or results
            map does not provide a result position for all calibrated qubits.
        :raises ValueError: Invalid method string.
        :return: Corrected counts, possibly with floating-point count values.
        :rtype: CountsDict
        """
        if self.prep_to_meas_sparse is None:
            raise RuntimeError("Calibration matrix is not yet defined")
        if len(res_map) != len(next(iter(counts))):
            raise RuntimeError(
                "Results map does not map all calibrated qubits. Make sure all qubits in calibration pattern have a valid measurement index in the map. This may be caused by not all qubits having a measure operation in the compiled circuit."
            )
        valid_methods = ("invert", "minimise", "bayesian")
        permuter = BitPermuter(tuple(res_map[qb] for qb in self.all_qbs))
        big_dimension = len(self.all_qbs)
        vector_size = 1 << big_dimension
        in_vec = np.zeros(vector_size, dtype=float)
        for state, count in counts.items():
            in_vec[permuter.permute(binary_to_int(state), inverse=True)] = count

        counts = np.sum(in_vec)
        in_vec_norm = in_vec / counts
        if method == "minimise":
            outvec = _minimise_correct(self.prep_to_meas_sparse, in_vec_norm, **options)

        elif method == "bayesian":
            tol_val = options.get("tol", 1 / counts)
            maxit = options.get("maxiter", None)
            outvec = _bayesian_iterative_correct(
                self.prep_to_meas_sparse, in_vec_norm, tol=tol_val, max_it=maxit
            )

        elif method == "invert":
            outvec = _invert_correct(self.prep_to_meas_sparse, in_vec_norm)

        else:
            raise ValueError("Method must be one of: ", *valid_methods)

        outvec *= counts
        return {
            int_to_binary(permuter.permute(index), big_dimension): count
            for index, count in enumerate(outvec)
        }

    def to_dict(self) -> Dict:
        """Get calibration information as a dictionary.

        :return: Dictionary output
        :rtype: Dict
        """
        prep_states = [
            [
                (tuple((uid.reg_name, uid.index) for uid in subs), state)
                for subs, state in d.items()
            ]
            for d in self._prepared_states
        ]
        subsets_matrices = [
            (tuple((uid.reg_name, uid.index) for uid in s), m.tolist())
            for s, m in self.subsets_matrix_map.items()
        ]
        self_dict = {
            "subset_matrix_map": subsets_matrices,
            "_prepared_states": prep_states,
        }
        return self_dict

    @classmethod
    def from_dict(class_obj, dict: Dict) -> "SpamCorrecter":
        """Build a `SpamCorrecter` instance from a dictionary in the format returned by
        `to_dict`.

        :return: Dictionary of calibration information.
        :rtype: SpamCorrecter
        """
        subsets, mats = zip(
            *(
                (tuple(Node(*pair) for pair in subset_tuple), np.array(matlist))
                for subset_tuple, matlist in dict["subset_matrix_map"]
            )
        )
        new_inst = class_obj(list(subsets))
        for s, m in zip(subsets, mats):
            new_inst.subsets_matrix_map[s] = m
        new_inst._prepared_states = [
            {
                tuple(Qubit(*pair) for pair in qb_tuple): tuple(state)
                for qb_tuple, state in subst_list
            }
            for subst_list in dict["_prepared_states"]
        ]
        new_inst.prep_to_meas_sparse = class_obj.calculate_sparse_mat(
            new_inst.subsets_matrix_map.values()
        )

        return new_inst
