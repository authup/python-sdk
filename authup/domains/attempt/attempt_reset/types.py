from datetime import datetime
from typing import Optional

from pydantic import BaseModel


class AttemptReset(BaseModel):
    id: str
    ip_address: str
    user_agent: str
    email: str
    token: Optional[str]
    created_at: str = datetime.now().isoformat()
    updated_at: str = datetime.now().isoformat()
