# -*- coding: utf-8 -*-
from sqlalchemy import Column, String, DateTime, Integer
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class Device(Base):

    __tablename__ = "device_lease_history"

    event_id = Column(Integer, primary_key=True)
    event_ts = Column(String)
    name = Column(String)
    mac = Column(String)
    ip = Column(String)
    lease_time_remaining = Column(String)
