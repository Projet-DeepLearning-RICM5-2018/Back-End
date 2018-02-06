"""
ORM representation of tables


Created on Fri Feb 24 22:44:09 2017

@author: Julian
"""

from sqlalchemy import Column, Integer, String, Boolean, ForeignKey, Date, Text
from sqlalchemy.orm import relationship
from SmartRecruiting_BackEnd.data.database import Base


class Formation(Base):
    __tablename__ = 'formation'
    id = Column(Integer, name="id", primary_key=True, nullable=False)
    label = Column(String(100), unique=True, nullable=False)
    description = Column(Text, unique=False, nullable=True)
    site = Column(String(100), unique=False, nullable=True)
    def serialize(self):
        return {
            'id': self.id,
            'label': self.label.decode("utf-8"),
            'description': self.description.decode("utf-8"),
            'site': self.site.decode("utf-8")
        }

        
        