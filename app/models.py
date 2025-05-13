from sqlalchemy import Integer, String, Date, Time, DateTime, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column
from app.database import db
from datetime import date, time, datetime
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin

class User(db.Model, UserMixin):
    __tablename__ = "Users"
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True, name="user_id")
    username: Mapped[str] = mapped_column(unique=True)
    email: Mapped[str] = mapped_column(unique=True, nullable=False) 
    password_hash: Mapped[str] = mapped_column(nullable=False)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def __repr__(self):
        return f"<User {self.username}>"

class ActivityRegistry(db.Model):
    __tablename__ = "ActivityRegistry"
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True, name="Sr_no")
    upload_user_id: Mapped[int] = mapped_column(ForeignKey('Users.user_id'), nullable=False, name="upload_user_id")
    upload_time: Mapped[datetime] = mapped_column(DateTime, nullable=False)
    activity_date: Mapped[date] = mapped_column(Date, nullable=False)
    activity_type: Mapped[str] = mapped_column(nullable=False)
    activity_length: Mapped[time] = mapped_column(Time, nullable=False)
    calories_burned: Mapped[float] = mapped_column(nullable=False, default=0.0)

    distance_m: Mapped[float] = mapped_column(nullable=True)
    weight_kg: Mapped[float] = mapped_column(nullable=True)
    average_speed_mps: Mapped[float] = mapped_column(nullable=True)
    max_speed_mps: Mapped[float] = mapped_column(nullable=True)
    start_lat: Mapped[str] = mapped_column(nullable=True)  # GPS at the start
    end_lat: Mapped[str] = mapped_column(nullable=True)    # GPS at the end


class SharedActivity(db.Model):
    __tablename__ = "SharedActivity"
    sharing_user: Mapped[int] = mapped_column(ForeignKey('ActivityRegistry.upload_user_id'), primary_key=True, name="sharing_user")
    activity_upload_time: Mapped[datetime] = mapped_column(ForeignKey('ActivityRegistry.upload_time'), primary_key=True, name="activity_upload_time")
    user_shared_with: Mapped[str] = mapped_column(ForeignKey('Users.email'), primary_key=True, name="user_shared_with")