from psycopg2 import OperationalError
from psycopg2.extras import DictCursor
from .database_connection import get_connection
from app.models.get_in_touch_form import GetInTouchForm
from app.models.request_meeting_form import RequestMeetingForm
from app.utils.logging_config import app_logger, error_logger

def fetch_all_get_in_touch_forms():
    data = None
    conn = None
    try:
        conn = get_connection()
        app_logger.info("Opened connection to database")
        with conn.cursor(cursor_factory=DictCursor) as cur:
            query = "SELECT * FROM get_in_touch_form"
            cur.execute(query)
            data = cur.fetchall()
            app_logger.info(f"Fetched {len(data)} rows from 'get_in_touch_form'")
    except OperationalError as e:
        error_logger.error(f"Something went wrong when trying to insert new 'get in touch' form to database: {e}")
    except Exception as e:
        error_logger.error(f"Unexpected error: {e}")
    finally:
        if conn:
            conn.close()
            app_logger.info("Database connection closed")

    all_forms_list = []
    for row in data:
        new_form = GetInTouchForm(**row)
        all_forms_list.append(new_form)

    return all_forms_list


def fetch_all_request_meeting_forms():
    data = None
    conn = None
    try:
        conn = get_connection()
        app_logger.info("Opened connection to database")
        with conn.cursor(cursor_factory=DictCursor) as cur:
            query = "SELECT * FROM request_meeting_form"
            cur.execute(query)
            data = cur.fetchall()
            app_logger.info(f"Fetched {len(data)} rows from 'request_meeting_form'")
    except OperationalError as e:
        error_logger.error(f"Something went wrong when trying to insert new 'get in touch' form to database: {e}")
    except Exception as e:
        error_logger.error(f"Unexpected error: {e}")
    finally:
        if conn:
            conn.close()
            app_logger.info("Database connection closed")

    all_forms_list = []
    for row in data:
        new_form = RequestMeetingForm(**row)
        all_forms_list.append(new_form)

    return all_forms_list