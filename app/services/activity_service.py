# app/services/activity_service.py

from app.models import ActivityRegistry, SharedActivity, User
from sqlalchemy import func
from datetime import date, timedelta, datetime
from flask_login import current_user

def get_weekly_calories_summary(user_id: int, goal: int = 300):
    today = date.today()
    start = today - timedelta(days=6)

    raw_data = (
        ActivityRegistry.query
        .with_entities(ActivityRegistry.activity_date, func.sum(ActivityRegistry.calories_burned))
        .filter(
            ActivityRegistry.upload_user_id == user_id,
            ActivityRegistry.activity_date.between(start, today)
        )
        .group_by(ActivityRegistry.activity_date)
        .all()
    )

    summary = {}
    for activity_date, total in raw_data:
        weekday = activity_date.strftime("%a")  # e.g., Mon, Tue
        summary[weekday] = round(total, 2)

    return {"goal": goal, "summary": summary}

def get_shared_activities_with_user(user_email: str):
    shares = SharedActivity.query.filter_by(user_shared_with=user_email).all()
    
    shared_data = []
    for share in shares:
        activity = ActivityRegistry.query.filter_by(
            upload_user_id=share.sharing_user,
            upload_time=share.activity_upload_time
        ).first()

        sharing_user = User.query.get(share.sharing_user)

        if activity and sharing_user:
            shared_data.append({
                "activity_type": activity.activity_type.title(),
                "activity_length": activity.activity_length,
                "activity_date": activity.activity_date.strftime('%Y-%m-%d'),
                "calories_burned": activity.calories_burned,
                "shared_by": sharing_user.email
            })

    return shared_data

def get_user_activities(user_id: int):
    records = ActivityRegistry.query.filter_by(upload_user_id=user_id).all()

    return [
        {
            "activity_type": r.activity_type,
            "activity_length": str(r.activity_length),
            "activity_date": r.activity_date.strftime('%Y-%m-%d'),
            "calories_burned": r.calories_burned,
            "upload_time": r.upload_time.isoformat()  # optional for share
        }
        for r in records
    ]

def get_latest_activity_entry(user_id: int):
    record = (
        ActivityRegistry.query
        .filter_by(upload_user_id=user_id)
        .order_by(ActivityRegistry.activity_date.desc(), ActivityRegistry.upload_time.desc())
        .first()
    )

    if not record:
        return {
            "activity": "None selected",
            "calories": 0,
            "duration": 0
        }

    # Parse duration from time object to minutes
    duration_minutes = record.activity_length.hour * 60 + record.activity_length.minute + record.activity_length.second / 60

    return {
        "activity": record.activity_type.title(),
        "calories": round(record.calories_burned, 2),
        "duration": round(duration_minutes)
    }
