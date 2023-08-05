# pylint: disable=no-member

import datetime
import random
import uuid

from qiskit import Aer, QuantumCircuit, assemble
from qiskit.providers import JobStatus


def fake_circuit():
    circuit = QuantumCircuit(2, 2)
    circuit.h(0)
    circuit.cx(0, 1)
    circuit.measure([0, 1], [0, 1])

    return circuit


def fake_qobj():
    backend = Aer.get_backend("qasm_simulator")
    return assemble(fake_circuit(), backend)


def fake_job_dict():
    job_id = str(uuid.uuid4())
    qobj = fake_qobj()

    return {
        "job_id": job_id,
        "date_submit": datetime.datetime.now().isoformat(),
        "qobj": qobj.to_dict(),
        "status": random.choice([
            JobStatus.INITIALIZING.name,
            JobStatus.RUNNING.name,
            JobStatus.QUEUED.name
        ])
    }
