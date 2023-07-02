from pydantic import BaseModel


class ChoiceVotes(BaseModel):
    choice: str
    votes: int

class QuestionVotes(BaseModel):
    question: str
    choice_votes: list[ChoiceVotes]

class PollChoiceStatisticsResponse(BaseModel):
    question_votes: list[QuestionVotes]