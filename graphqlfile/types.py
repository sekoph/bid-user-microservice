from typing import Optional, List
from strawberry import type
from datetime import datetime

@type
class UserTypeQl:
    id: int
    username: str
    email: str
    name: str
    disabled: bool
    date_created: datetime
