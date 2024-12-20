from flask import Blueprint, render_template, request, jsonify
from marshmallow import ValidationError
from app.utils.logging_config import app_logger, error_logger
from .schemas.get_in_touch_form_schema import GetInTouchFormSchema
from .schemas.request_meeting_form_schema import RequestMeetingFormSchema
from global_data import global_data


main = Blueprint('main', __name__)


@main.route('/')
@main.route("/home")
def home():
    return render_template('index.html', global_data = global_data)


@main.route('/schedule')
def about():
    return render_template("schedule.html", global_data = global_data)


@main.route("/pgp")
def pgp_page():
    return render_template("pgp_page.html", global_data = global_data)


@main.route("/work")
def work():
    return render_template("work.html", global_data = global_data)


@main.route("/services/<name>")
def services(name):
    return render_template(f"{name}.html", global_data=global_data)


@main.route("/get_in_touch", methods = ["POST"])
def get_in_touch():
    input_data = request.form.to_dict()

    allowed_fields = {"name", "email", "phone", "message"}
    filtered_data = {key: value for key, value in input_data.items() if key in allowed_fields}

    # Usando o schema para validar e criar o objeto
    try:
        schema = GetInTouchFormSchema()
        new_get_in_touch_form = schema.load(filtered_data)
        app_logger.info("Object created:", new_get_in_touch_form)

        if new_get_in_touch_form.save_new_to_database():
            return ("Your request was saved. Please wait for our contact in you provided email.")
    
    except ValidationError as e:
        error_logger.error("Validation error:", e.messages)

    return ("Something went wrong. Please try again later.")


@main.route("/request_meeting", methods = ["POST"])
def request_meeting():
    input_data = request.form.to_dict()

    filtered_data = {key: value for key, value in input_data.items()}

    try:
        schema = RequestMeetingFormSchema()
        new_request_meeting = schema.load(filtered_data)
        app_logger.info("Object created: ", new_request_meeting)

        if new_request_meeting.save_new_to_database():
            return ("Your request was saved. Please wait for our contact in you provided email.")

    except ValidationError as e:
        error_logger.error("Validation error: ", e.messages)

    return ("Something went wrong. Please try again later.")

