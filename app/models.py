from sqlalchemy import Integer, String, Date, Time, DateTime, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column
from app import db
from datetime import date, time, datetime

class User(db.Model):
    user_id: Mapped[int] = mapped_column(primary_key=True)
    username: Mapped[str] = mapped_column(unique=True)
    email: Mapped[str] = mapped_column(unique=True) 

class ActivityRegistry(db.Model):
    user_id: Mapped[int] = mapped_column(ForeignKey('User.id'), primary_key=True)
    upload_time: Mapped[datetime] = mapped_column(DateTime, primary_key=True)
    activity_date: Mapped[date] = mapped_column(Date, nullable=False)
    activity_type: Mapped[str] = mapped_column(nullable=False)
    activity_length: Mapped[time] = mapped_column(Time,nullable=False)