from datetime import datetime
from typing import Optional

from pydantic import BaseModel


class AttemptActivation(BaseModel):
    id: str
    ip_address: str
    user_agent: str
    token: Optional[str]
    created_at: str = datetime.now().isoformat()
    updated_at: str = datetime.now().isoformat()
