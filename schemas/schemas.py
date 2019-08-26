from marshmallow import Schema, fields, ValidationError, validates, validate, post_dump
from marshmallow.fields import Nested, Integer
from marshmallow.validate import Length, Range, Regexp, OneOf
from datetime import date


class CreateCitizenSchema(Schema):
    citizen_id = fields.Int(required=True, validate=Range(min=0))
    town = fields.Str(required=True, validate=[Length(min=1, max=256), Regexp('(?=.*\\w).{1,}')])
    street = fields.Str(required=True, validate=[Length(min=1, max=256), Regexp('(?=.*\\w).{1,}')])
    building = fields.Str(required=True, validate=[Length(min=1, max=256), Regexp('(?=.*\\w).{1,}')])
    apartment = fields.Int(required=True, validate=Range(min=0))
    name = fields.Str(required=True, validate=Length(min=1, max=256))
    birth_date = fields.Date(required=True, format='%d.%m.%Y')
    gender = fields.Str(required=True, validate=OneOf(choices=["male", "female"]))
    relatives = fields.List(fields.Integer(), required=True)

    @validates("birth_date")
    def validate_birth_date(self, value):
        if value >= date.today():
            raise ValidationError('Birth date is invalid', value)

    @validates("relatives")
    def validate_relatives_is_unique(self, value):
        if len(value) > len(set(value)):
            raise ValidationError('Relatives id must be unique', value)


class ImportSchema(Schema):
    citizens = Nested(CreateCitizenSchema, required=True, many=True, dump_to='data')


class UpdateCitizenSchema(Schema):
    town = fields.Str(required=True, validate=[Length(min=1, max=256), Regexp('(?=.*\\w).{1,}')])
    street = fields.Str(required=True, validate=[Length(min=1, max=256), Regexp('(?=.*\\w).{1,}')])
    building = fields.Str(required=True, validate=[Length(min=1, max=256), Regexp('(?=.*\\w).{1,}')])
    apartment = fields.Int(required=True, validate=Range(min=0))
    name = fields.Str(required=True, validate=Length(min=1, max=256))
    birth_date = fields.Date(format='%d.%m.%Y', required=True)
    gender = fields.Str(required=True, validate=OneOf(choices=["male", "female"]))
    relatives = fields.List(fields.Integer(), required=True)

    @validates("relatives")
    def validate_relatives_is_unique(self, value):
        if len(value) > len(set(value)):
            raise ValidationError('Relatives id must be unique', value)
