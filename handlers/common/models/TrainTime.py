from sqlalchemy import Column, String, Integer, DateTime, Boolean
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class TrainTime(Base):
    __tablename__ = 'train_times'

    id = Column(Integer, primary_key=True)

    station_short_code = Column(String, nullable=True)
    station_uic_code = Column(Integer, nullable=True)

    country_code = Column(String, nullable=True)
    type = Column(String, nullable=True)
    train_stopping = Column(Boolean, nullable=True)
    commercial_stop = Column(Boolean, nullable=True)

    commercial_track = Column(String, nullable=True)
    cancelled = Column(Boolean, nullable=True)
    scheduled_time = Column(String, nullable=True)
    actual_time = Column(String, nullable=True)
    difference_in_minutes = Column(Integer, nullable=True)

    causes = Column(String, nullable=True)
    train_ready = Column(String, nullable=True)
    accepted = Column(Boolean, nullable=True)
    timestamp = Column(DateTime, nullable=True)

    live_estimate_time = Column(DateTime, nullable=True)
    estimate_source = Column(String, nullable=True)
    train_ready = Column(Object, nullable=True)

