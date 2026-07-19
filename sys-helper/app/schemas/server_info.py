from pydantic import BaseModel

class ServerInfo(BaseModel):
    id: str
    status: str
    note: str
