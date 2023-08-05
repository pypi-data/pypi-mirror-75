import re

from marshmallow import Schema, fields, validate, validates_schema, ValidationError


class ValidatesSchema(Schema):
    @validates_schema(skip_on_field_errors=True)
    def validate_to_field(self, data, **kwargs):
        if data['channel'] == 'email':
            email = re.compile('[^@]+@[^@]+\.[^@]+')
            if not email.match(data['to']):
                raise ValidationError('to must be an email address', field_name='to')
        elif data['channel'] == 'sms':
            sms = re.compile('/^[0-9 ()+-]+$/')
            if not sms.match(data['to']):
                raise ValidationError('to must be a phone number', field_name='to')


class CreateVerificationBaseSchema(Schema):
    template_name = fields.Str(required=True)
    subject_params = fields.Dict(allow_none=True)
    body_params = fields.Dict(allow_none=True)


class CreateVerificationInputSchema(CreateVerificationBaseSchema, ValidatesSchema):
    channel = fields.Str(validate=validate.OneOf(['email', 'sms']), required=True)
    to = fields.Str(required=True)


class CreateVerificationOutputSchema(CreateVerificationBaseSchema):
    id = fields.Int(required=True)
    channel = fields.Str(validate=validate.OneOf(['email', 'sms']), required=True)
    code = fields.Str(required=True)
    expiration_date = fields.Str(required=True)
    status = fields.Str(validate=validate.OneOf(['pending']))


class CheckVerificationInputSchema(ValidatesSchema):
    channel = fields.Str(validate=validate.OneOf(['email', 'sms']), required=True)
    to = fields.Str()
    code = fields.Str(allow_none=False)


class CheckVerificationOutputSchema(CheckVerificationInputSchema):
    id = fields.Int(required=True)
    status = fields.Str(validate=validate.OneOf(['approved', 'denied']))
    denied_reason = fields.Str()


create_verification_input_schema = CreateVerificationInputSchema()
create_verification_output_schema = CreateVerificationOutputSchema()
check_verification_input_schema = CheckVerificationInputSchema()
check_verification_output_schema = CheckVerificationOutputSchema()
