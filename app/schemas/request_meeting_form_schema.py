from marshmallow import Schema, fields, post_load
from app.models.request_meeting_form import RequestMeetingForm

class RequestMeetingFormSchema(Schema):
    date = fields.Str(allow_none=True, missing = "")
    time = fields.Str(allow_none=True, missing = "")
    name = fields.Str(required = True)
    email = fields.Email(required=True)
    phone = fields.Str(allow_none=True, missing="")
    message = fields.Str(required=True)
    web_development = fields.Str(allow_none = True, missing = None)
    mobile_development = fields.Str(allow_none = True, missing = None)
    API_development = fields.Str(allow_none = True, missing = None)
    database_management = fields.Str(allow_none = True, missing = None)
    cloud_services = fields.Str(allow_none = True, missing = None)
    consultation = fields.Str(allow_none = True, missing = None)
    project_timeline = fields.Str(allow_none = True, missing = None)
    budget_range = fields.Str(allow_none = True, missing = None)
    hear_about_us = fields.Str(allow_none = True, missing = None)
    form_id = fields.Int(missing = -1)

    @post_load
    def make_object(self, data, **kwargs):
        return RequestMeetingForm(**data)