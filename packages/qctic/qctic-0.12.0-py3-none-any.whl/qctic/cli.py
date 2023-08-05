import argparse
import asyncio
import logging
import os
import pprint
import random

from qiskit import QuantumCircuit, execute

from qctic.api import QCticAPI
from qctic.backend import (QCticQasmSimulator, QCticStatevectorSimulator,
                           QCticUnitarySimulator)
from qctic.provider import QCticProvider
from qctic.utils import wait_result_async

_MIN_QUBITS = 2
_PROB_H = 0.5

_logger = logging.getLogger("qctic")


def init_logging():
    try:
        import coloredlogs
        coloredlogs.install(level=logging.DEBUG, logger=_logger)
    except ImportError:
        _logger.setLevel(logging.DEBUG)
        logging.basicConfig()


# pylint: disable=no-member
def random_circuit(max_qubits, unitary=False):
    max_qubits = max_qubits if max_qubits >= _MIN_QUBITS else _MIN_QUBITS
    qubits = random.randint(_MIN_QUBITS, max_qubits)
    circuit = QuantumCircuit(qubits, qubits)

    h_gates = [
        idx for idx in range(qubits)
        if random.random() <= _PROB_H
    ]

    if len(h_gates) == 0:
        h_gates.append(0)

    [circuit.h(idx) for idx in h_gates]

    if not unitary:
        measure_args = (list(range(qubits)),) * 2
        circuit.measure(*measure_args)

    return circuit


def build_result_msg_qasm(result, circuit):
    return "## Counts:\n{}\n## Memory:\n{}".format(
        pprint.pformat(result.get_counts(circuit)),
        pprint.pformat(result.get_memory(circuit)))


def build_result_msg_unitary(result, circuit):
    return "## Unitary:\n{}".format(
        pprint.pformat(result.get_unitary(circuit)))


def build_result_msg_statevector(result, circuit):
    return "## Statevector:\n{}".format(
        pprint.pformat(result.get_statevector(circuit)))


def log_result(result, circuits, backend_name):
    msg_funcs = {
        QCticQasmSimulator.NAME: build_result_msg_qasm,
        QCticUnitarySimulator.NAME: build_result_msg_unitary,
        QCticStatevectorSimulator.NAME: build_result_msg_statevector
    }

    msg_func = msg_funcs[backend_name]

    for idx, circ in enumerate(circuits):
        _logger.info("Circuit #%s results:\n%s", idx, msg_func(result, circ))


async def execute_jobs(qubits, backend_name, num_circuits, shots, gpu):
    qctic_provider = QCticProvider.from_env()
    qctic_backend = qctic_provider.get_backend(backend_name)

    is_unitary = backend_name == QCticUnitarySimulator.NAME

    circuits = [
        random_circuit(max_qubits=qubits, unitary=is_unitary)
        for _idx in range(num_circuits)
    ]

    for idx, circ in enumerate(circuits):
        _logger.info("Circuit #%s:\n%s", idx, circ.draw())

    backend_options = {}

    if gpu and backend_name == QCticQasmSimulator.NAME:
        backend_options.update({"method": "statevector_gpu"})
    elif gpu and backend_name != QCticQasmSimulator.NAME:
        _logger.warning("Ignoring GPU flag")

    memory = backend_name == QCticQasmSimulator.NAME

    qctic_job = execute(
        circuits,
        qctic_backend,
        shots=shots,
        backend_options=backend_options,
        memory=memory)

    await qctic_job.submit_task
    result = await wait_result_async(qctic_job)

    if not result.success:
        _logger.error("Some of the experiments failed")

        for idx, exp_res in enumerate(result.results):
            _logger.warning("Circuit #%s status: %s", idx, exp_res.status)

        return

    log_result(result=result, circuits=circuits, backend_name=backend_name)


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("--circuits", type=int, default=1)
    parser.add_argument("--shots", type=int, default=10)
    parser.add_argument("--qubits", type=int, default=4)
    parser.add_argument("--gpu", action="store_true")

    backend_choices = [
        QCticQasmSimulator.NAME,
        QCticStatevectorSimulator.NAME,
        QCticUnitarySimulator.NAME
    ]

    parser.add_argument(
        "--backend",
        default=QCticQasmSimulator.NAME,
        choices=backend_choices)

    return parser.parse_args()


def main():
    init_logging()
    loop = asyncio.get_event_loop()
    args = parse_args()

    _logger.debug("Arguments: %s", args)

    def stop_cb(fut):
        _logger.debug("Main task: %s", fut)
        loop.stop()

    try:
        main_task = asyncio.ensure_future(execute_jobs(
            qubits=args.qubits,
            backend_name=args.backend,
            num_circuits=args.circuits,
            shots=args.shots,
            gpu=args.gpu))

        main_task.add_done_callback(stop_cb)
        loop.run_forever()
    except:
        _logger.error("Error", exc_info=True)
    finally:
        _logger.debug("Closing loop")
        loop.close()


if __name__ == "__main__":
    main()
