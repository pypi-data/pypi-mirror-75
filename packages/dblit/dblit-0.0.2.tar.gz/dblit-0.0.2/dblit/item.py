from sqlalchemy import Column, ForeignKey, Integer, String, and_
from sqlalchemy.orm import relationship, validates

from typing import List, Optional

from dblit.base import Base
from dblit.job import Job
from dblit.label import Label
from dblit.label_set import LabelSet


class Item(Base):
    __tablename__ = 'item'

    id = Column(Integer, primary_key=True)

    job_id = Column(Integer, ForeignKey('job.id'), nullable=False)
    job: Job = relationship("Job", backref="items")

    uri = Column(String(4096), nullable=False)

    override_label_id = Column(Integer, ForeignKey('label.id'), nullable=True)
    override_label: Optional[Label] = relationship("Label")  # no backref!

    def __init__(self, job: Job, uri: str):
        self.job = job
        self.uri = uri

    @classmethod
    def find_all_by_label_set_and_uri(cls, session, label_set: LabelSet, uri: str) -> List["Item"]:
        items: List[Item] = session.query(cls).join(Job.items).filter(
            and_(Job.label_set_id == label_set.id, Item.uri == uri)).all()
        return items

    @validates('uri')
    def validate_uri(self, key, uri: str):
        assert uri is not None and len(uri) > 0
        return uri

    @validates('override_label')
    def validate_override_label(self, key, override_label: Optional[Label]):
        assert override_label is None or override_label.label_set == self.job.label_set
        return override_label
