import datetime

from marshmallow import (INCLUDE, Schema, ValidationError, fields, post_load,
                         pre_dump, pre_load, validate, validates_schema)
from qiskit.providers import JobStatus
from qiskit.qobj import QasmQobj as Qobj
from qiskit.result import Result


def _qiskit_model_validator(klass):
    def validator(val):
        try:
            klass.from_dict(val)
            return True
        except:
            return False

    return validator


class GetJobsQuerySchema(Schema):
    class Meta:
        unknown = INCLUDE

    limit = fields.Integer(
        default=10,
        required=True,
        validate=validate.Range(min=1, max=500))

    skip = fields.Integer(
        default=0,
        required=True,
        validate=validate.Range(min=0))

    status = fields.List(fields.Str(
        required=False,
        validate=validate.OneOf([item.name for item in JobStatus])))

    date_start = fields.DateTime(format="iso")
    date_end = fields.DateTime(format="iso")

    @validates_schema
    def validate_dtimes(self, data, **kwargs):
        start = data.get("start_dtime")
        end = data.get("end_dtime")

        if start and end and end <= start:
            raise ValidationError("end_dtime must be greater than start_dtime")

    @pre_dump
    def str_status_to_list(self, data, **kwargs):
        if isinstance(data.get("status", None), str):
            data["status"] = [data["status"]]

        return data


class JobSchema(Schema):
    class Meta:
        unknown = INCLUDE

    job_id = fields.Str(required=True)

    date_submit = fields.AwareDateTime(
        required=True,
        format="iso",
        default_timezone=datetime.timezone.utc)

    date_queue = fields.AwareDateTime(
        format="iso",
        default_timezone=datetime.timezone.utc)

    date_start = fields.AwareDateTime(
        format="iso",
        default_timezone=datetime.timezone.utc)

    date_end = fields.AwareDateTime(
        format="iso",
        default_timezone=datetime.timezone.utc)

    date_execute_start = fields.AwareDateTime(
        format="iso",
        default_timezone=datetime.timezone.utc)

    date_execute_end = fields.AwareDateTime(
        format="iso",
        default_timezone=datetime.timezone.utc)

    qobj = fields.Mapping(
        required=True,
        validate=_qiskit_model_validator(Qobj))

    status = fields.Str(
        required=True,
        validate=validate.OneOf([item.name for item in JobStatus]))

    result = fields.Mapping(
        required=False,
        validate=_qiskit_model_validator(Result),
        allow_none=True)

    error = fields.Str()
    run_params = fields.Mapping()


class BackendStatusSchema(Schema):
    class Meta:
        unknown = INCLUDE

    operational = fields.Boolean(required=True)
    pending_jobs = fields.Integer(required=True)
