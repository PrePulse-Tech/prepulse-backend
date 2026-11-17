from datetime import datetime

from pydantic import BaseModel, IPvAnyAddress


class LogLine(BaseModel):
    """One parsed log line.

    Mirrors the log_line table in the ERD, except for the database keys
    (log_line_id, log_source_id), which are added when the line is stored.

    source_ip, username, message and raw_line can contain personal data and
    must be masked before anything is sent to the AI service.
    """

    logged_at: datetime
    level: str | None = None
    message: str | None = None
    source_ip: IPvAnyAddress | None = None
    username: str | None = None
    status_code: int | None = None
    raw_line: str
