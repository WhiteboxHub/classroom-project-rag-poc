from db.models import ChatDatabase

class SessionManager:
    def __init__(self):
        self.db = ChatDatabase()

    def create_session(self, user_id: str = "default") -> str:
        return self.db.create_session(user_id)

    def get_history(self, session_id: str):
        return self.db.get_messages(session_id)

    def add_message(self, session_id: str, role: str, content: str):
        self.db.add_message(session_id, role, content)
