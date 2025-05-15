from app.models import ActivityRegistry, SharedActivity, User
from app.database import db
from sqlalchemy import func
from datetime import date, timedelta, datetime
from flask_login import current_user


from collections import defaultdict
from datetime import timedelta

def get_weekly_calories_summary(user_id: int, start_date: date, goal: int = 300):
    end_date = start_date + timedelta(days=6)

    # Initialize all 7 days with 0
    summary = {}
    for i in range(7):
        d = start_date + timedelta(days=i)
        summary[d.strftime("%Y-%m-%d")] = 0.0

    # Query summed calories per day
    raw_data = (
        ActivityRegistry.query
        .with_entities(ActivityRegistry.activity_date, func.sum(ActivityRegistry.calories_burned))
        .filter(
            ActivityRegistry.upload_user_id == user_id,
            ActivityRegistry.activity_date.between(start_date, end_date)
        )
        .group_by(ActivityRegistry.activity_date)
        .all()
    )

    for activity_date, total in raw_data:
        key = activity_date.strftime("%Y-%m-%d")
        summary[key] = round(total, 2)

    return {
        "goal": goal,
        "summary": summary,
        "start_date": start_date.strftime("%Y-%m-%d"),
        "end_date": end_date.strftime("%Y-%m-%d")
    }


def get_shared_activities_with_user(user_email: str):
    shares = SharedActivity.query.filter_by(user_shared_with=user_email).all()

    shared_data = []
    for share in shares:
        activity = ActivityRegistry.query.get(share.activity_id)
        sharing_user = User.query.get(share.sharing_user_id)
        if activity:
            shared_data.append({
                "activity_type": activity.activity_type.title(),
                "activity_length": activity.activity_length,
                "activity_date": activity.activity_date.strftime('%Y-%m-%d'),
                "calories_burned": activity.calories_burned,
                "shared_by": sharing_user.email if sharing_user else "Unknown"
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

def get_global_leaderboard():
    results = (
        db.session.query(User.username, func.sum(ActivityRegistry.calories_burned).label("total_calories"))
        .join(ActivityRegistry, User.id == ActivityRegistry.upload_user_id)
        .group_by(User.username)
        .order_by(func.sum(ActivityRegistry.calories_burned).desc())
        .all()
    )
    return [{"username": row.username, "calories": round(row.total_calories, 2)} for row in results]


def get_shared_activity_summary_by_type(user_email: str):
    today = date.today()
    week_start = today - timedelta(days=today.weekday())  # 本週一
    week_end = week_start + timedelta(days=6)

    shares = (
        db.session.query(ActivityRegistry.activity_type, ActivityRegistry.activity_length)
        .join(SharedActivity, SharedActivity.activity_id == ActivityRegistry.id)
        .filter(
            SharedActivity.user_shared_with == user_email,
            ActivityRegistry.activity_date.between(week_start, week_end)
        )
        .all()
    )

    from collections import defaultdict
    summary = defaultdict(float)

    for activity_type, duration in shares:
        minutes = duration.hour * 60 + duration.minute + duration.second / 60
        summary[activity_type.title()] += minutes

    return dict(summary)
