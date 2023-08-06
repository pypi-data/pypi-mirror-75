from sqlalchemy import Column, String, Integer
from sqlalchemy.orm import validates

from dblit.base import Base


class LabelSet(Base):
    __tablename__ = 'label_set'

    id = Column(Integer, primary_key=True)
    code: str = Column(String(100), nullable=False, unique=True)

    def __init__(self, code: str):
        self.code = code

    @classmethod
    def find_or_create(cls, session, code: str):
        label_set = session.query(cls).filter_by(code=code).first()
        if label_set is None:
            label_set = cls(code=code)
            session.add(label_set)
        return label_set

    @validates('code')
    def validate_code(self, key, code: str):
        assert code is not None and len(code) > 0
        return code
