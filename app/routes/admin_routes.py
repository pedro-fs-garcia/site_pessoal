from flask import Blueprint, render_template, request, redirect
from flask_login import login_required, login_user
from app.database import forms
from app.models.get_in_touch_form import GetInTouchForm
from app.models.user import User
from app.schemas.request_meeting_form_schema import RequestMeetingFormSchema
from app.utils.logging_config import app_logger, error_logger
from global_data import global_data


admin = Blueprint('admin', __name__)


@admin.route("/admin", methods=["POST", "GET"])
def admin_access():
    if request.method == "POST":
        input_data = request.form.to_dict()

        user = User(password=input_data['access_token'], username=input_data['username'])
        if user.authenticate():
            login_user(user)
            app_logger.info("Granted admin access.")
            get_in_touch_forms = forms.fetch_all_get_in_touch_forms()
            request_meeting_forms = forms.fetch_all_request_meeting_forms()

            return render_template(
                "admin/admin_page.html", 
                global_data = global_data, 
                get_in_touch_forms = get_in_touch_forms, 
                request_meeting_forms = request_meeting_forms
                )

        error_logger.error("Denied admin access.")
        return redirect("/home")

    return render_template("admin/access_page.html", global_data = global_data)


@login_required
@admin.route("/dashboard", methods=["POST", "GET"])
def dashboard():
    get_in_touch_forms = forms.fetch_all_get_in_touch_forms()
    request_meeting_forms = forms.fetch_all_request_meeting_forms()

    return render_template(
    "admin/admin_page.html", 
    global_data = global_data, 
    get_in_touch_forms = get_in_touch_forms, 
    request_meeting_forms = request_meeting_forms
    )




@login_required
@admin.route("/update_get_in_touch_form", methods=["POST", "GET"])
def update_get_in_touch_form():
    form_data = request.form.to_dict()
    form_action = form_data.pop('action')
    
    get_in_touch_form = GetInTouchForm(**form_data)

    if form_action == "save":
        get_in_touch_form.update_form_to_database()
    elif form_action == "delete":
        get_in_touch_form.delete_form_from_database()

    return redirect('/admin')


@login_required
@admin.route("/update_request_meeting_form", methods=["GET", "POST"])
def update_request_meeting_form():
    form_data = request.form.to_dict()
    form_action = form_data.pop('action')

    schema = RequestMeetingFormSchema()
    request_meeting_form = schema.load(form_data)

    if form_action == 'save':
        request_meeting_form.update_form_to_database()
    elif form_action == 'delete':
        request_meeting_form.delete_from_database()

    return redirect('/admin')