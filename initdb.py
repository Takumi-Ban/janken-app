from email.policy import default
from sqlalchemy import Column, Integer, String, Float, DateTime
from dbsetting import Engine
from dbsetting import Base

class User(Base):
    """
    ユーザモデル
    """

    __tablename__ = 'user_info'
    __table_args__ = {
        'comment': 'ユーザ情報のマスターテーブル'
    }

    id = Column('id', Integer, primary_key=True, autoincrement=True)
    name = Column('name', String(50))
    password = Column('password', String(100))
    time = Column('datetime', DateTime)

class Results(Base):
    """
    実行結果の保存
    """

    __tablename__ = 'results'
    __table_args__ = {
        'comment': '実行結果情報のマスターテーブル'
    }

    id = Column('id', Integer, primary_key=True, autoincrement=True)
    username = Column('username', String(50))
    correctlabel = Column('correct_label', Integer)
    result_label = Column('result_label', Integer)
    point = Column('point', Integer)
    time = Column('datetime', DateTime)

if __name__ == '__main__':
    Base.metadata.create_all(bind=Engine)