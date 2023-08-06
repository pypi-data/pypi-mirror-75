from sqlalchemy import Column, ForeignKey, String, Integer, UniqueConstraint, or_
from sqlalchemy.orm import relationship, validates

from dblit.base import Base
from dblit.label_set import LabelSet


class Label(Base):
    __tablename__ = 'label'

    id = Column(Integer, primary_key=True)
    code = Column(String(100), nullable=False)
    name = Column(String(100), nullable=False)

    label_set_id = Column(Integer, ForeignKey('label_set.id'), nullable=False)
    label_set = relationship("LabelSet", backref="labels")

    __table_args__ = (
        UniqueConstraint('code', 'label_set_id'),
        UniqueConstraint('name', 'label_set_id'),
    )

    def __init__(self, code: str, name: str, label_set: LabelSet):
        self.code = code
        self.name = name
        self.label_set = label_set

    @classmethod
    def find_or_create(cls, session, code: str, name: str, label_set: LabelSet):
        label: Label = session.query(cls).filter_by(label_set_id=label_set.id).filter(
            or_(Label.code == code, Label.name == name)).first()
        if label is None:
            label = cls(code=code, name=name, label_set=label_set)
            session.add(label)
        else:
            label.code = code
            label.name = name
        return label

    @validates('code')
    def validate_code(self, key, code: str):
        assert code is not None and len(code) > 0
        return code

    @validates('name')
    def validate_code(self, key, name: str):
        assert name is not None and len(name) > 0
        return name
