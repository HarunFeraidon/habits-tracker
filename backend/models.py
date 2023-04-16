from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

from datetime import date, datetime, timedelta
import random
import json

db = SQLAlchemy()
migrate = Migrate()

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(50), unique=True, nullable=False)
    charts = db.relationship("Chart", backref="user", lazy=True)

class Chart(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(50), nullable=False)
    year_start = db.Column(db.Date)
    year_end = db.Column(db.Date)
    data = db.Column(db.JSON)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)

    def __init__(self, title):
        self.title = title
        reference_year = date.today().year
        self.year_start = datetime(reference_year, 1, 1)
        self.year_end = datetime(reference_year, 12, 31)
        self.data = self.init_data()

    def init_data(self):
        data_list = []
        data_list.append({"value": 0, "day": date.today().strftime("%Y-%m-%d")})
        return json.dumps(data_list)

    def sample_data(self):
        """
        Populates Chart object's data with random data from Jan. 1 to current day
        """
        data_list = []
        reference_year = date.today().year
        day = datetime(reference_year, 1, 1)
        today = datetime.now().date()
        bias_towards_1 = random.random()
        while day.date() <= today:
            value = random.choices([0, 1], weights=[1-bias_towards_1, bias_towards_1])[0]
            data_list.append(
                {"value": value, "day": day.strftime("%Y-%m-%d")}
            )
            day += timedelta(days=1)
        self.data = json.dumps(data_list)

    def complete_today(self):
        """
        Trigged when user opts to 'complete' today
        """
        all_data = json.loads(self.data)
        all_data[-1]["value"] = 1
        self.data = json.dumps(all_data)

    def append_day(self):
        """
        Adds another day to Chart object's data
        """
        all_data = json.loads(self.data)
        all_data.append({"value": 0, "day": datetime.now().strftime("%Y-%m-%d")})
        if date.today().year != self.year_end:
            reference_year = date.today().year
            self.year_end = datetime(reference_year, 12, 31)
        self.data = json.dumps(all_data)