from sqlalchemy import Column, ForeignKey, Integer
from sqlalchemy.orm import relationship, validates

from typing import Optional

from dblit.base import Base
from dblit.label import Label
from dblit.label_set import LabelSet
from dblit.user import User


class Job(Base):
    __tablename__ = 'job'

    id = Column(Integer, primary_key=True)

    user_id = Column(Integer, ForeignKey('user.id'), nullable=True)
    user = relationship("User", backref="jobs")

    label_set_id = Column(Integer, ForeignKey('label_set.id'), nullable=False)
    label_set: LabelSet = relationship("LabelSet")  # no backref!

    default_label_id = Column(Integer, ForeignKey('label.id'), nullable=False)
    default_label: Label = relationship("Label")  # no backref!

    current_item_index = Column(Integer, default=0, nullable=False)

    def __init__(self, label_set: LabelSet, default_label: Label, user: Optional[User] = None):
        self.label_set = label_set
        self.default_label = default_label
        self.user = user

    @validates('current_item_index')
    def validate_current_item_index(self, key, current_item_index: int):
        assert current_item_index is not None and 0 <= current_item_index < len(self.items)
        return current_item_index

    @validates('default_label')
    def validate_default_label(self, key, default_label: Label):
        assert default_label is not None and default_label.label_set == self.label_set
        return default_label

    def name(self) -> str:
        return f"{self.label_set.code}/{self.id}"
