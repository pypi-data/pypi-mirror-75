__all__ = ['ORM_Base', 'SessionLocal', 'execute_SQL']

from sqlalchemy import text, create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base, declared_attr
import os
import json

"""
This provides a battery-included base model for SQLAlchemy models.
use it like this:
    class User(ORM_Base):
        Pass

"""

SQLALCHEMY_DATABASE_URL = os.getenv('DATABASE_URL', None)

engine = create_engine(SQLALCHEMY_DATABASE_URL, echo=False)
SessionLocal = sessionmaker(bind=engine)


def execute_SQL(sql):
    sql = sql.replace('$SCHEMA', os.getenv('DATABASE_SCHEMA'))
    with engine.connect() as conn:
        result = conn.execute(sql)
    return [dict(row.items()) for row in result]


class MyBase(object):
    __table_args__ = {'schema': os.getenv('DATABASE_SCHEMA')}

    @declared_attr
    def __tablename__(cls):
        return cls.__name__.lower()

    @classmethod
    def all(cls, *order_by, **filter_by):
        db = SessionLocal()
        query = db.query(cls)
        if filter_by:
            query = query.filter_by(**filter_by)
        if order_by:
            query = query.order_by(*[getattr(cls, x) for x in order_by])
        result = query.all()
        db.close()
        return result

    @classmethod
    def rawSQL(cls, whereSQL=None, orderSQL=None, limit=None):
        db = SessionLocal()
        query = db.query(cls)
        if whereSQL:
            query = query.filter(text(whereSQL))
        if orderSQL:
            query = query.order_by(text(orderSQL))
        if limit:
            query = query.limit(limit)
        result = query.all()
        db.close()
        return result

    @classmethod
    def within(cls, field, in_list, order_by_list=[]):
        db = SessionLocal()
        if isinstance(in_list, str):
            in_list = json.loads(in_list)
        query = db.query(cls).filter(getattr(cls, field).in_(in_list))
        if order_by_list:
            query = query.order_by(*[getattr(cls, x) for x in order_by_list])
        result = query.all()
        db.close()
        return result

    @classmethod
    def list(cls, field, in_list):
        db = SessionLocal()
        if isinstance(in_list, str):
            in_list = json.loads(in_list)
        result = db.query(cls).filter(getattr(cls, field).in_(in_list)).all()
        result.sort(key=lambda x: in_list.index(getattr(x, field)))
        db.close()
        return result

    @classmethod
    def count(cls, **filter_by):
        db = SessionLocal()
        result = db.query(cls).filter_by(**filter_by).count()
        db.close()
        return result

    @classmethod
    def exist(cls, **filter_by):
        return cls.count(**filter_by) > 0

    @classmethod
    def one(cls, **filter_by):
        db = SessionLocal()
        result = db.query(cls).filter_by(**filter_by).one()
        db.close()
        return result

    @classmethod
    def create(cls, **props):
        db = SessionLocal()
        obj = cls(**props)
        db.add(obj)
        db.commit()
        db.close()
        return True

    @classmethod
    def create_many(cls, dict_ls):
        db = SessionLocal()
        for d in dict_ls:
            obj = cls(**d)
            db.add(obj)
        db.commit()
        db.close()
        return True

    @classmethod
    def delete(cls, **filter_by):
        db = SessionLocal()
        obj = db.query(cls).filter_by(**filter_by).one()
        db.delete(obj)
        db.commit()
        db.close()
        return True

    @classmethod
    def delete_many(cls, **filter_by):
        db = SessionLocal()
        objs = db.query(cls).filter_by(**filter_by).all()
        for obj in objs:
            db.delete(obj)
        db.commit()
        db.close()
        return True

    @classmethod
    def update(cls, update_dict, **filter_by):
        db = SessionLocal()
        obj = db.query(cls).filter_by(**filter_by).one()
        for k, v in update_dict.items():
            setattr(obj, k, v)
        db.commit()
        db.close()
        return True

    @classmethod
    def update_many(cls, update_dict, **filter_by):
        db = SessionLocal()
        query = db.query(cls)
        if filter_by:
            query = query.filter_by(**filter_by)
        objs = query.all()
        for obj in objs:
            for k, v in update_dict.items():
                setattr(obj, k, v)
        db.commit()
        db.close()
        return True

    @classmethod
    def upsert(cls, **props):
        db = SessionLocal()
        obj = cls(**props)
        db.merge(obj)
        db.commit()
        db.close()
        return True

    @classmethod
    def upsert_many(cls, dict_ls):
        db = SessionLocal()
        for d in dict_ls:
            obj = cls(**d)
            db.merge(obj)
        db.commit()
        db.close()
        return True


ORM_Base = declarative_base(cls=MyBase)
metadata = ORM_Base.metadata
