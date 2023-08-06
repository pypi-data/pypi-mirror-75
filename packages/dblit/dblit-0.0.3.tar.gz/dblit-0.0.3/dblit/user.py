from sqlalchemy import Column, String, Integer
from sqlalchemy.orm import validates

from dblit.base import Base


class User(Base):
    __tablename__ = 'user'

    id = Column(Integer, primary_key=True)
    code: str = Column(String(100), nullable=False, unique=True)

    def __init__(self, code: str):
        self.code = code

    @classmethod
    def find_or_create(cls, session, code: str):
        user = session.query(cls).filter_by(code=code).first()
        if user is None:
            user = cls(code=code)
            session.add(user)
        return user

    @validates('code')
    def validate_code(self, key, code: str):
        assert code is not None and len(code) > 0
        return code
