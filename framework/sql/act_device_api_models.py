# coding: utf-8
import json

from sqlalchemy import BigInteger, Boolean, Column, DateTime, ForeignKey, Integer, SmallInteger, String, text, Text
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()
metadata = Base.metadata

json_serializable = [str, int, bool, dict, list]


class Device(Base):
    __tablename__ = 'devices'

    id = Column(Integer, primary_key=True, server_default=text("nextval('devices_id_seq'::regclass)"))
    platform = Column(String(32), nullable=False)
    user_id = Column(BigInteger, nullable=False)
    entered_at = Column(DateTime, nullable=False)
    removed = Column(Boolean, nullable=False, server_default=text("false"))
    created_at = Column(DateTime, nullable=False, server_default=text("now()"))
    updated_at = Column(DateTime, nullable=False, server_default=text("now()"))

    def serialize(self):
        return json.dumps({c.name: getattr(self, c.name) for c in self.__table__.columns})


class DevicesEvent(Base):
    __tablename__ = 'devices_events'

    id = Column(Integer, primary_key=True, server_default=text("nextval('devices_events_id_seq'::regclass)"))
    device_id = Column(ForeignKey('devices.id'))
    type = Column(SmallInteger, nullable=False)
    status = Column(SmallInteger, nullable=False)
    payload = Column(JSONB(astext_type=Text()))
    created_at = Column(DateTime, nullable=False, server_default=text("now()"))
    updated_at = Column(DateTime, nullable=False, server_default=text("now()"))

    device = relationship('Device')

    def serialize(self):
        return {c.name: getattr(self, c.name) if type(getattr(self, c.name)) in json_serializable else
        str(getattr(self, c.name)) for c in self.__table__.columns}
