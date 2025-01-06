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
            api_development,
            database_management,
            cloud_services,
            consultation,
            project_timeline,
            budget_range,
            hear_about_us,
            form_id=-1,
            submission_date = None

    ):
        self.date = date
        self.time = time
        self.name = name
        self.email = email
        self.phone = phone
        self.message = message
        self.web_development = web_development
        self.mobile_development = mobile_development
        self.api_development = api_development
        self.database_management = database_management
        self.cloud_services = cloud_services
        self.consultation = consultation
        self.project_timeline = project_timeline
        self.budget_range = budget_range
        self.hear_about_us = hear_about_us
        self.form_id = form_id
        self.submission_date = submission_date

    def __repr__(self):
        return f"<RequestMeetingForm(date={self.date}, time={self.time})>"
    
    def save_new_to_database(self):
        operation_success = False
        try:
            conn = get_connection()
            app_logger.info("Opened connection to database")
            with conn.cursor() as cur:
                query = "INSERT INTO request_meeting_form (date, time, name, email, phone, message, web_development, mobile_development, API_development, database_management, cloud_services, consultation, project_timeline, budget_range, hear_about_us) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
                values = (self.date, self.time, self.name, self.email, self.phone, self.message, (self.web_development=="on"), (self.mobile_development=="on"), self.api_development=="on", self.database_management=="on", self.cloud_services=="on", self.consultation=="on", self.project_timeline, self.budget_range, self.hear_about_us)
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
    

    def update_form_to_database(self):
        conn = None
        operation_success = False
        try:
            conn = get_connection()
            app_logger.info("Opened connection to database")
            with conn.cursor() as cur:
                query = """
                    UPDATE request_meeting_form 
                    SET date = %s, time = %s, name = %s, email = %s, phone = %s, message = %s, web_development = %s, mobile_development = %s, API_development = %s, database_management = %s, cloud_services = %s, consultation = %s, project_timeline = %s, budget_range = %s, hear_about_us = %s
                    WHERE form_id = %s
                    """
                values = (self.date, self.time, self.name, self.email, self.phone, self.message, self.web_development=='on', self.mobile_development=='on', self.api_development=='on', self.database_management=='on', self.cloud_services=='on', self.consultation=='on', self.project_timeline, self.budget_range, self.hear_about_us, self.form_id)
                cur.execute(query, values)
                app_logger.info(f"'request meeting' form number {self.form_id} was updated.")
            conn.commit()
            operation_success = True
            cur.close()
        except OperationalError as e:
            error_logger.error(f"Something went wrong when trying to update 'request meeting' form number {self.form_id} to database: {e}")
        finally:
            if conn:
                conn.close()
        return operation_success


    def delete_from_database(self):
        conn = None
        operation_success = False
        try:
            conn = get_connection()
            app_logger.info("Opened connection to database")
            with conn.cursor() as cur:
                query = f"DELETE FROM request_meeting_form WHERE form_id = {self.form_id}"
                # values = (self.form_id)
                cur.execute(query)
                app_logger.info(f"'request meeting' form number {self.form_id} was deleted from database.")
            conn.commit()
            operation_success = True
            cur.close()
        except OperationalError as e:
            error_logger.error(f"Something went wrong when trying to delete 'request meeting' form number {self.form_id} from database: {e}")
        finally:
            if conn:
                conn.close()
        return operation_success