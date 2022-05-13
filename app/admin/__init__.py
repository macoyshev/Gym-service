import asyncio

from flask import Flask
from flask_admin import Admin

from app.configs import settings
from app.db import Session, create_db
from app.db.models import Exercise, Muscle, Train, User

from .views import ExerciseModel, MusclesModel, TrainModal, UserModal


def create_admin() -> Flask:
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    loop.run_until_complete(create_db())

    app = Flask(__name__)

    app.secret_key = settings.admin_key

    admin = Admin(app, name='Admin', template_mode='bootstrap4')

    admin.add_view(
        MusclesModel(
            Muscle,
            Session,
        )
    )
    admin.add_view(
        ExerciseModel(
            Exercise,
            Session,
        )
    )
    admin.add_view(
        UserModal(
            User,
            Session,
        )
    )
    admin.add_view(
        TrainModal(
            Train,
            Session,
        )
    )

    return app
