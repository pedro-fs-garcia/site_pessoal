from psycopg2 import OperationalError
from app.database.database_connection import get_connection
from app.utils.logging_config import app_logger, error_logger

class RequestMeetingForm:
    def __init__(
            self,
            date,
            time,
            name,
            email,
            phone,
            message,
            web_development,
            mobile_development,
            API_development,
            database_management,
            cloud_services,
            consultation,
            project_timeline,
            budget_range,
            hear_about_us,
            form_id=-1

    ):
        self.date = date
        self.time = time
        self.name = name
        self.email = email
        self.phone = phone
        self.message = message
        self.web_development = web_development
        self.mobile_development = mobile_development
        self.API_development = API_development
        self.database_management = database_management
        self.cloud_services = cloud_services
        self.consultation = consultation
        self.project_timeline = project_timeline
        self.budget_range = budget_range
        self.hear_about_us = hear_about_us
        self.form_id = form_id

    def __repr__(self):
        return f"<RequestMeetingForm(date={self.date}, time={self.time})>"
    
    def save_new_to_database(self):
        operation_success = False
        try:
            conn = get_connection()
            app_logger.info("Opened connection to database")
            with conn.cursor() as cur:
                query = "INSERT INTO request_meeting_form (date, time, name, email, phone, message, web_development, API_development, database_management, cloud_services, consultation, project_timeline, budget_range, hear_about_us) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
                values = (self.date, self.time, self.name, self.email, self.phone, self.message, (self.web_development=="on"), (self.mobile_development=="on"), self.database_management=="on", self.cloud_services=="on", self.consultation=="on", self.project_timeline, self.budget_range, self.hear_about_us)
                cur.execute(query, values)
                app_logger.info("new 'request meeting' form was added to the database.")
            conn.commit()
            operation_success = True
        except OperationalError as e:
            error_logger.error(f"Something went wrong when trying to insert new 'get in touch' form to database: {e}")
        finally:
            if conn:
                conn.close()
        return operation_success
    
