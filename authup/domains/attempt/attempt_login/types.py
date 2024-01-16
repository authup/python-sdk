from datetime import datetime

from pydantic import BaseModel

from ...user.types import User


class AttemptLogin(BaseModel):
    id: str
    ip_address: str
    user_agent: str
    email: str
    success: bool
    user: User
    user_id: str
    created_at: str = datetime.now().isoformat()
    updated_at: str = datetime.now().isoformat()
