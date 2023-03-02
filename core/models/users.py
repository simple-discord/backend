from sqlalchemy import Column, INT, TIMESTAMP, String, UniqueConstraint

from sql_app.databases import Base


class Users(Base):
    __tablename__ = 'users'

    id = Column('id', INT, primary_key=True, autoincrement=True)
    username = Column('name', String(30), nullable=False, unique=True)
    registration_date = Column('delete_date', TIMESTAMP(), nullable=True)
    avatar = Column('image', String(50), nullable=True)


