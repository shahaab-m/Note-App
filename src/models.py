from sqlalchemy import String, Integer, Column, Boolean

from database import Base, engine
def create_tables():
    Base.metadata.create_all(engine)
class Note(Base):
    __tablename__ = 'note'
    id = Column(Integer, primary_key=True)
    author = Column(String(40), nullable=False)
    content = Column(String(80), nullable=False)
