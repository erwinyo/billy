# Built-in imports

# Third-party imports

# Local imports
from pydantic import BaseModel


class EmailRequest(BaseModel):
    subject: str
    body: str
    recipient: str
