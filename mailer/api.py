from flask import Blueprint
from flask_apispec import use_kwargs, marshal_with
from marshmallow import fields, validate, Schema
from http import HTTPStatus

from . import __about__
from .extensions import limiter, mailer


# ------------------------------------------------------------------------------


api_version = "v1"
api_base_url = ""

bp_name = "api"
bp = Blueprint(bp_name, __name__, url_prefix="/api")


# ------------------------------------------------------------------------------


class StrictSchema(Schema):
    class Meta:
        strict = True


class ApiInfoSchema(StrictSchema):
    name = fields.String(required=True)
    version = fields.String(required=True)
    api_version = fields.String(required=True)


class MailSchema(StrictSchema):
    email = fields.Email(required=True, validate=validate.Length(1, 50))
    name = fields.String(required=True, validate=validate.Length(1, 50))
    subject = fields.String(required=True, validate=validate.Length(1, 100))
    message = fields.String(required=True, validate=validate.Length(1, 200))
    honeypot = fields.String(required=False, validate=validate.Equal(""))


# ------------------------------------------------------------------------------


@bp.route("/")
@limiter.exempt
@marshal_with(ApiInfoSchema)
def get_api_info():
    data = {
        "name": __about__.__title__,
        "version": __about__.__version__,
        "api_version": api_version,
    }

    return data, HTTPStatus.OK


@bp.route("/mail", methods=["POST"])
@use_kwargs(MailSchema, locations=("json",))
@marshal_with(MailSchema)
def post_mail(**kwargs):
    email = kwargs.get("email")
    name = kwargs.get("name")
    subject = kwargs.get("subject")
    message = kwargs.get("message")

    mailer.send_mail(from_email=email, from_name=name, subject=subject, message=message)

    return kwargs, HTTPStatus.ACCEPTED
