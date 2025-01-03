from marshmallow import Schema, fields, post_load
from app.models.get_in_touch_form import GetInTouchForm

class GetInTouchFormSchema(Schema):
    name = fields.Str(required=True)
    email = fields.Email(required=True)
    phone = fields.Str(allow_none=True, missing="")
    message = fields.Str(required=True)
    form_id = fields.Int(missing=-1)
    submission_date = fields.DateTime(missing = None)

    @post_load
    def make_object(self, data, **kwargs):
        return GetInTouchForm(**data)