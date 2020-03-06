from sqlalchemy import Column, Integer, String, Time, Float, TIMESTAMP
from json import JSONDecoder, JSONEncoder
from app.database import Base
from app import database


class Story(Base):
    __tablename__ = 'stories'

    id = Column(Integer, primary_key=True)
    summary = Column(String)
    description = Column(String)
    story_type = Column(String)
    complexity = Column(String)
    estimated_time = Column(String)
    cost = Column(Float)
    created_at = Column(TIMESTAMP)
    created_by = Column(String)
    status = Column(String)
    last_updated_at = Column(TIMESTAMP)
    last_updated_by = Column(String)

    def __repr__(self):
        return "<Story(summary='%s', status='%s')>" % (
            self.summary, self.status)

    def to_dict(self):
        res_dict = {}
        res_dict['id'] = self.id
        res_dict['summary'] = self.summary
        res_dict['status'] = self.status
        return res_dict

    def to_dict_full(self):
        res_dict = {'id': self.id, 'summary': self.summary, 'description': self.description,
            'story_type': self.story_type, 'complexity': self.complexity,
            'estimated_time': self.estimated_time, 'cost':self.cost,
            'created_at':self.created_at, 'created_by':self.created_by,
            'status':self.status,
            'last_updated_by':self.last_updated_by, 'last_updated_at':self.last_updated_at
        }
        return res_dict

