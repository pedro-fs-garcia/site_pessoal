from psycopg2 import OperationalError
from app.database.database_connection import get_connection
from app.utils.logging_config import app_logger, error_logger

class GetInTouchForm:
    def __init__(
            self,
            form_id = -1,
            name = None,
            email = None,
            phone = None,
            message = None,
            submission_date = None
    ):
        self.name = name
        self.email = email
        self.phone = phone
        self.message = message
        self.form_id = form_id
        self.submission_date = submission_date
    
    def __repr__(self):
        return f"<GetInTouchForm(name={self.name}, email={self.email}, phone={self.phone}, message={self.message}, form_id={self.form_id})>"


    def save_new_to_database(self):
        operation_success = False
        conn = None
        try:
            conn = get_connection()
            app_logger.info("Opened connection to database")
            with conn.cursor() as cur:
                query = "INSERT INTO get_in_touch_form (name, email, phone, message) VALUES (%s, %s, %s, %s)"
                values = (self.name, self.email, self.phone, self.message)
                cur.execute(query, values)
                app_logger.info("new 'get in touch' form was added to the database.")
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
                    UPDATE get_in_touch_form 
                    SET name = %s, email = %s, phone = %s, message = %s
                    WHERE form_id = %s
                    """
                values = (self.name, self.email, self.phone, self.message, self.form_id)
                cur.execute(query, values)
                app_logger.info(f"'get in touch' form number {self.form_id} was updated.")
            conn.commit()
            operation_success = True
            cur.close()
        except OperationalError as e:
            error_logger.error(f"Something went wrong when trying to update 'get in touch' form number {self.form_id} to database: {e}")
        finally:
            if conn:
                conn.close()
        return operation_success
    
    def delete_form_from_database(self):
        conn = None
        operation_success = False
        try:
            conn = get_connection()
            app_logger.info("Opened connection to database")
            with conn.cursor() as cur:
                query = "DELETE FROM get_in_touch_form WHERE form_id = %s"
                values = (self.form_id)
                cur.execute(query, values)
                app_logger.info(f"'get in touch' form number {self.form_id} was deleted from database.")
            conn.commit()
            operation_success = True
            cur.close()
        except OperationalError as e:
            error_logger.error(f"Something went wrong when trying to delete 'get in touch' form number {self.form_id} from database: {e}")
        finally:
            if conn:
                conn.close()
        return operation_success