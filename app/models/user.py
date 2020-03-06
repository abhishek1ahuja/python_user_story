from sqlalchemy import Column, Integer, String, Time, Float, TIMESTAMP
from app.database import Base
from app import database

class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True)
    username = Column(String, unique=True)
    name = Column(String)
    user_type = Column(String)

    def __repr__(self):
        return "User<(username='%s', user_type='%s')>" % (
            self.username, self.user_type)
