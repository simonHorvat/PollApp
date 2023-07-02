from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from .database import Base
import configparser


config = configparser.ConfigParser()
config.read("config.ini")

POLL_TABLE = config.get("DATABASE", "poll_table")
QUESTION_TABLE = config.get("DATABASE", "question_table")
CHOICE_TABLE = config.get("DATABASE", "choice_table")
ANSWER_TABLE = config.get("DATABASE", "answer_table")
MAX_TEXT_LEN = int(config.get("DATABASE", "max_text_len"))

class Poll(Base):
    __tablename__ = POLL_TABLE

    id = Column(Integer, primary_key=True)
    poll_text = Column(String(MAX_TEXT_LEN))
    pub_date = Column(DateTime)

    def __str__(self):
        return self.poll_text


class Question(Base):
    __tablename__ = QUESTION_TABLE

    id = Column(Integer, primary_key=True)
    poll_id = Column(Integer, ForeignKey(f'{POLL_TABLE}.id'))  # foreign key reference
    question_text = Column(String(MAX_TEXT_LEN))

    poll = relationship('Poll', backref='questions')

    def __str__(self):
        return self.question_text


class Choice(Base):
    __tablename__ = CHOICE_TABLE

    id = Column(Integer, primary_key=True)
    question_id = Column(Integer, ForeignKey(f'{QUESTION_TABLE}.id'))  # foreign key reference
    choice_text = Column(String(MAX_TEXT_LEN))

    question = relationship('Question', backref='choices')

    def __str__(self):
        return self.choice_text


class Answer(Base):
    __tablename__ = ANSWER_TABLE

    id = Column(Integer, primary_key=True)
    question_id = Column(Integer, ForeignKey(f'{QUESTION_TABLE}.id'))  # foreign key reference
    choice_id = Column(Integer, ForeignKey(f'{CHOICE_TABLE}.id'))  #  foreign key reference

    question = relationship('Question', backref='answers')
    choice = relationship('Choice', backref='answers')

    def __str__(self):
        return f"Question: {self.question.question_text}, Choice: {self.choice.choice_text}"
