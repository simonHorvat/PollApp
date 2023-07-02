from pydantic import BaseModel


class PollAttendeesResponse(BaseModel):
    total_attendees: int