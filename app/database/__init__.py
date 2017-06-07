#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time : 2017/5/29 0:10
# @Author : BlackMatrix
# @Site : https://github.com/blackmatrix7
# @File : __init__.py
# @Software: PyCharm
from datetime import datetime
from flask_sqlalchemy import SQLAlchemy

__author__ = 'blackmatrix'

db = SQLAlchemy()


class ModelBase(db.Model):

    __abstract__ = True

    id = db.Column(db.Integer, primary_key=True, index=True)
    created_time = db.Column(db.DateTime, default=datetime.now)
    updated_time = db.Column(db.DateTime, default=datetime.now,
                             onupdate=datetime.now)

    def __init__(self, **kwargs):
        columns = [c.name for c in self.__table__.columns]
        super().__init__(**{attr: value for attr, value in kwargs.items()
                            if attr in columns})


class ModelMixin(db.Model):

    __abstract__ = True

    def __getitem__(self, item):
        return getattr(self, item)

    def __setitem__(self, key, value):
        setattr(self, key, value)

    def upsert(self):
        db.session.add(self)
        return self

    def delete(self):
        db.session.delete(self)
        return self

    @property
    def columns(self):
        yield from (c.name for c in self.__table__.columns)

    @staticmethod
    def commit():
        db.session.commit()

    @classmethod
    def get_by_id(cls, id_):
        return db.session.query(cls).filter(cls.id == int(id_)).first()

    def to_dict(self, columns=None):
        """
        将SQLALCHEMY MODEL 转换成 dict
        :param columns: dict 的 key, 如果为None, 则返回全部列
        :return:
        """
        if columns is None:
            columns = self.columns
        return {c: getattr(self, c) for c in columns}

    def to_json(self):
        pass


if __name__ == '__main__':
    pass
