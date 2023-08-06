from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker


class App:

    def __init__(self, connect_string: str, create_schema_up_front: bool = True, log_sql_statements: bool = True):
        """
        :param connect_string: structure and contents depends on the database to be used
            SQLite (in memory): f"sqlite:///:memory:"
            MySQL: f"mysql+pymysql://{user_name}>:{password}>@{host}/{db_name}"
        """
        self.__engine = create_engine(connect_string, echo=log_sql_statements)
        if create_schema_up_front:
            self.__create_schema()

    def create_session(self,
                       autoflush=True,
                       autocommit=False,
                       expire_on_commit=True):
        """
        :param autoflush:
        :param autocommit:
        :param expire_on_commit:
        :return: a session that provides the following interface
            - session.begin()
            - session.add(orm-object)
            - session.rollback()
            - session.commit()
            - session.close()
        """
        session = sessionmaker(
            bind=self.__engine, autoflush=autoflush, autocommit=autocommit, expire_on_commit=expire_on_commit)()
        return session

    def __create_schema(self):
        from dblit.base import Base
        from dblit.item import Item
        from dblit.job import Job
        from dblit.label import Label
        from dblit.label_set import LabelSet
        from dblit.user import User

        Base.metadata.create_all(self.__engine)
