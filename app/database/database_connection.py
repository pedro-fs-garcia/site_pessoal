from psycopg2 import sql, pool, OperationalError, connect
import app.config as config
from app.utils.logging_config import app_logger, error_logger
from .create_tables_script import create_tables_script


configure = {
    "user": config.DB_USER,
    "password": config.DB_PASSWORD,
    "host": config.DB_HOST,
    "database": config.DB_NAME,
    "port": config.DB_PORT
}

def get_connection():
    try:
        connection = connect(**configure)
        app_logger.info("Conection with PostgreSQL created successfully!")
        return connection
    except OperationalError as e:
        error_logger.error(f"Something went wrong connecting to the database: {e}")
        return None


def create_tables():
    try:
        conn = connect(user = config.DB_USER,
                       password = config.DB_PASSWORD,
                       host = config.DB_HOST,
                       database = config.DB_NAME)
        
        with conn.cursor() as cur:
            cur.execute(create_tables_script)
            app_logger.info("Tabelas criadas ou já existentes.")
        conn.commit()
        conn.close()
    except OperationalError as e:
        error_logger.error(f"Erro ao conectar ou criar as tabelas no banco de dados {e}")


def create_database_if_not_exists():
    try:
        conn = connect(user = config.DB_USER,
                       password = config.DB_PASSWORD,
                       host = config.DB_HOST)
        
        conn.autocommit = True
        with conn.cursor() as cur:
            cur.execute("SELECT 1 FROM pg_database WHERE datname = %s", (configure["database"],))
            exists = cur.fetchone()
            if not exists:
                cur.execute(sql.SQL("CREATE DATABASE {}").format(sql.Identifier(configure["database"])))
                app_logger.info(f"Banco de dados '{configure['database']}' criado com sucesso!")
                create_tables()
            else:
                app_logger.info(f"Banco de dados '{configure['database']}' já existe.")
                create_tables()
        conn.close()
    except OperationalError as e:
        error_logger.error(f"Erro ao criar o banco de dados: {e}")


def init_db():
    create_database_if_not_exists()

    