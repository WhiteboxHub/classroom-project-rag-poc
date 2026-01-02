import psycopg2
from psycopg2.extras import RealDictCursor
import sqlite3
import uuid
import os
from typing import List, Dict, Optional
from utils.config import Config
from utils.logging import setup_logger

logger = setup_logger(__name__)

USE_LOCAL_DB = os.getenv("USE_LOCAL_DB", "False").lower() == "true"
LOCAL_DB_PATH = "chat_history.db"

def get_db_connection():
    if USE_LOCAL_DB:
        try:
            conn = sqlite3.connect(LOCAL_DB_PATH)
            # Enable row factory to behave like RealDictCursor
            conn.row_factory = sqlite3.Row
            return conn
        except Exception as e:
            logger.error(f"Error connecting to SQLite: {e}")
            raise e
    else:
        try:
            conn = psycopg2.connect(
                host=Config.POSTGRES_HOST,
                database=Config.POSTGRES_DB,
                user=Config.POSTGRES_USER,
                password=Config.POSTGRES_PASSWORD,
                port=Config.POSTGRES_PORT
            )
            return conn
        except Exception as e:
            logger.error(f"Error connecting to Postgres: {e}")
            raise e

def init_db():
    try:
        conn = get_db_connection()
        cur = conn.cursor()
        
        if USE_LOCAL_DB:
            logger.info("Initializing SQLite database...")
            with open('db/init_sqlite.sql', 'r') as f:
                schema = f.read()
            cur.executescript(schema)
        else:
            logger.info("Initializing Postgres database...")
            with open('db/init.sql', 'r') as f:
                schema = f.read()
            cur.execute(schema)
            
        conn.commit()
        cur.close()
        conn.close()
        logger.info("Database initialized successfully.")
    except Exception as e:
        logger.error(f"Failed to initialize database: {e}")

class ChatDatabase:
    def __init__(self):
        # We assume init_db is called at startup
        pass

    def create_session(self, user_id: str = "default_user") -> str:
        session_id = str(uuid.uuid4())
        conn = get_db_connection()
        try:
            cur = conn.cursor()
            cur.execute("INSERT INTO sessions (id, user_id) VALUES (?, ?)" if USE_LOCAL_DB else "INSERT INTO sessions (id, user_id) VALUES (%s, %s)", (session_id, user_id))
            conn.commit()
            return session_id
        except Exception as e:
            conn.rollback()
            logger.error(f"Error creating session: {e}")
            raise e
        finally:
            conn.close()

    def add_message(self, session_id: str, role: str, content: str):
        conn = get_db_connection()
        try:
            cur = conn.cursor()
            cur.execute("INSERT INTO messages (session_id, role, content) VALUES (?, ?, ?)" if USE_LOCAL_DB else "INSERT INTO messages (session_id, role, content) VALUES (%s, %s, %s)", 
                       (session_id, role, content))
            conn.commit()
        except Exception as e:
            conn.rollback()
            logger.error(f"Error adding message: {e}")
            raise e
        finally:
            conn.close()

    def get_messages(self, session_id: str) -> List[Dict[str, str]]:
        conn = get_db_connection()
        try:
            cur = conn.cursor()
            query = "SELECT role, content FROM messages WHERE session_id = ? ORDER BY created_at ASC" if USE_LOCAL_DB else "SELECT role, content FROM messages WHERE session_id = %s ORDER BY created_at ASC"
            cur.execute(query, (session_id,))
            rows = cur.fetchall()
            
            if USE_LOCAL_DB:
                 # SQLite rows are accessible by index or name
                return [{"role": row['role'], "content": row['content']} for row in rows]
            else:
                return [{"role": row[0], "content": row[1]} for row in rows]
        except Exception as e:
            logger.error(f"Error fetching messages: {e}")
            return []
        finally:
            conn.close()

