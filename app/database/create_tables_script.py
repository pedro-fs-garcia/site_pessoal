create_tables_script = """
                CREATE TABLE IF NOT EXISTS get_in_touch_form (
                    form_id SERIAL PRIMARY KEY,
                    name VARCHAR(100) NOT NULL,
                    email VARCHAR(100) NOT NULL,
                    phone VARCHAR(50),
                    message VARCHAR(500),
                    submission_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                );
                CREATE TABLE IF NOT EXISTS request_meeting_form (
                    form_id SERIAL PRIMARY KEY,
                    date DATE,
                    time TIME,
                    name VARCHAR(100) NOT NULL,
                    email VARCHAR(100) NOT NULL,
                    phone VARCHAR(50),
                    message VARCHAR(500),
                    web_development BOOLEAN,
                    mobile_development BOOLEAN,
                    API_development BOOLEAN,
                    database_management BOOLEAN,
                    cloud_services BOOLEAN,
                    consultation BOOLEAN,
                    project_timeline VARCHAR(50),
                    budget_range VARCHAR(50),
                    hear_about_us VARCHAR(50),
                    submission_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                );
            """