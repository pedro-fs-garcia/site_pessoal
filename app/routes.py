from flask import Blueprint, render_template, request
from marshmallow import ValidationError
from app.utils.logging_config import app_logger, error_logger
from .schemas.get_in_touch_form_schema import GetInTouchFormSchema
from .schemas.request_meeting_form_schema import RequestMeetingFormSchema
from global_data import global_data
import json

main = Blueprint('main', __name__)

with open("app/static/projects.json", "r", encoding = "utf-8") as file:
    projects = json.load(file)

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
    print(projects)
    return render_template("work.html", global_data = global_data, projects=projects)


@main.route("/blogfeed")
def blogfeed():
    return "This page is not available yet. Please come back in the future."


@main.route("/services/<name>")
def services(name):
    return render_template(f"{name}.html", global_data=global_data)


@main.route("/submission_result/<result>")
def thank_you(result):
    result = True if result == "success" else False
    return render_template("submission_result.html", global_data = global_data, result = result)


@main.route("/get_in_touch", methods = ["POST", "GET"])
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
            return thank_you('success')
    
    except ValidationError as e:
        error_logger.error("Validation error:", e.messages)

    return thank_you('fail')


@main.route("/request_meeting", methods = ["POST", "GET"])
def request_meeting():
    input_data = request.form.to_dict()

    filtered_data = {key: value for key, value in input_data.items()}

    try:
        schema = RequestMeetingFormSchema()
        new_request_meeting = schema.load(filtered_data)
        app_logger.info("Object created: ", new_request_meeting)

        if new_request_meeting.save_new_to_database():
            return thank_you('success')

    except ValidationError as e:
        error_logger.error("Validation error: ", e.messages)

    return thank_you('fail')

