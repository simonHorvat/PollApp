from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError

import logging
import configparser

from database.database import get_db
from database.models import Poll, Question, Choice, Answer
from schemas.PollAttendeesResponse import PollAttendeesResponse
from schemas.PollChoiceStatisticsResponse import PollChoiceStatisticsResponse

# Read configuration from config.ini
config = configparser.ConfigParser()
config.read("config.ini")

LOG_FORMAT = config.get("LOGGING", "format")
GET_ATTENDEES_DESC = config.get("ROUTES", "get_attendees")
GET_CHOICE_STATISTICS_DESC = config.get("ROUTES", "get_choice_statistics")

# Set up logging
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

ch = logging.StreamHandler()
ch.setLevel(logging.DEBUG)
formatter = logging.Formatter(LOG_FORMAT)
ch.setFormatter(formatter)
logger.addHandler(ch)

router = APIRouter()


@router.get("/polls/{id}/attendees", description=GET_ATTENDEES_DESC)
async def get_attendees(id: int, db: Session = Depends(get_db)) -> PollAttendeesResponse:
    try:
        logger.info(f"get_attendees called with id: {id}")

        # Validate the id parameter
        if not (id is None or (isinstance(id, int) and id > 0)):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="id must be a positive integer"
            )

        # Retrieve the poll from the database
        poll = db.query(Poll).filter(Poll.id == id).first()
        if poll is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Poll not found"
            )

        # Calculate the total attendees
        total_questions = db.query(Question).filter(Question.poll_id == id).count()
        total_answers = db.query(Answer).join(Choice).join(Question).filter(Question.poll_id == id).count()
        total_attendees = total_answers / total_questions

        # Log the total attendees
        logger.info(f"Total attendees for poll {id}: {total_attendees}")

        # Return the response
        return PollAttendeesResponse(total_attendees=total_attendees)

    # Error handling
    except HTTPException:
        raise  # Re-raise the HTTPException as it is
    except SQLAlchemyError as e:
        db.rollback()
        logger.error(f"An error occurred in get_attendees: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="An error occurred while retrieving attendees"
        )



@router.get("/polls/{id}/choice_statistics", description=GET_CHOICE_STATISTICS_DESC)
async def get_choice_statistics(id: int, db: Session = Depends(get_db)) -> PollChoiceStatisticsResponse:
    try:
        logger.info(f"get_choice_statistics called with id: {id}")

        # Validate the id parameter
        if not (id is None or (isinstance(id, int) and id > 0)):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="id must be a positive integer"
            )

        # Retrieve the poll from the database
        poll = db.query(Poll).filter(Poll.id == id).first()
        if poll is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Poll not found"
            )

        # Calculate the choice statistics
        question_votes = []
        for question in poll.questions:
            choice_votes = []
            for choice in question.choices:
                votes_per_choice = db.query(Answer).filter(Answer.question_id == question.id,
                                                           Answer.choice_id == choice.id).count()
                choice_votes.append({"choice": choice.choice_text, "votes": votes_per_choice})
            question_votes.append({"question": question.question_text, "choice_votes": choice_votes})

        # Log the choice statistics
        logger.info(f"Choice statistics for poll {id}: {question_votes}")

        # Return the response
        return PollChoiceStatisticsResponse(question_votes=question_votes)

    except HTTPException:
        raise  # Re-raise the HTTPException as it is
    except SQLAlchemyError as e:
        db.rollback()
        logger.error(f"An error occurred in get_choice_statistics: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="An error occurred while retrieving choice statistics"
        )

