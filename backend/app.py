import os
import random
from dotenv import load_dotenv
from flask import Flask, jsonify, request, url_for, render_template, redirect
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_marshmallow import Marshmallow
from flask_cors import CORS
import json
import jwt
from functools import wraps

from datetime import date, datetime, timedelta
from apscheduler.schedulers.background import BackgroundScheduler

app = Flask(__name__)
CORS(app)


load_dotenv()

app.config["SQLALCHEMY_DATABASE_URI"] = "mysql+pymysql://root:@localhost/habits_tracker"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["SECRET_KEY"] = os.environ.get("SECRET_KEY")

db = SQLAlchemy(app)
migrate = Migrate(app, db)
ma = Marshmallow(app)


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(50), unique=True, nullable=False)
    charts = db.relationship("Chart", backref="user", lazy=True)


# Function to decode and verify JWT token
def decode_jwt(token):
    """
    Function to decode and verify JWT token

    Args:
        token (str): hashed string representing a token

    Returns:
        dict: dict with token decoded
    """
    try:
        # Decode and verify JWT token using secret key
        payload = jwt.decode(token, app.config["SECRET_KEY"], algorithms=["HS256"])
        return payload
    except jwt.ExpiredSignatureError:
        # Handle expired token
        return None
    except jwt.InvalidTokenError:
        # Handle invalid token
        return None


def jwt_required(f):
    """
    Decorator that takes care or authentication
    """
    @wraps(f)
    def decorated_function(*args, **kwargs):
        token = request.headers.get(
            "Authorization"
        )  # Get JWT token from request headers
        if token:
            decoded_token = decode_jwt(token)  # Decode and verify JWT token
            if decoded_token:
                # Token is valid, continue processing the route
                email = decoded_token["email"]
                kwargs["email"] = email
                print("Authenticated route: Hello, {}".format(email))
            return f(*args, **kwargs)
        return jsonify({"error": "Authentication failed."}), 401

    return decorated_function


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


class ChartSchema(ma.Schema):
    class Meta:
        fields = ("id", "title", "year_start", "year_end", "data", "user_id")


chart_schema = ChartSchema()
charts_schema = ChartSchema(many=True)


@app.route("/create_user", methods=["POST"])
def create_user():
    """
    Route to authenticate or create a new user.
    It is called upon after user signs in via Google
    Args:
        None
    Returns:
        tuple: a Response object and HTTP status code
    """
    email = request.form["email"]
    user = User.query.filter_by(email=email).first()
    token = jwt.encode(
        {
            "email": email,
            "exp": datetime.utcnow()
            + timedelta(minutes=30),  # set token expiration time
        },
        app.config["SECRET_KEY"],
        algorithm="HS256",
    )

    if user is None:
        user = User(email=email)
        db.session.add(user)
        db.session.commit()
        return (
            jsonify(
                {
                    "message": f"User with email '{email}' has been created!",
                    "token": token,  # .decode('utf-8')
                }
            ),
            200,
        )
    else:
        return (
            jsonify(
                {
                    "message": f"User with email '{email}' already exists.",
                    "token": token,  # .decode('utf-8')
                }
            ),
            200,
        )


@app.route("/create/<title>", methods=["POST"])
# @login_required
@jwt_required
def create_chart(title, **kwargs):
    """
    Authentication required, this function creates a Chart object for the user
    Args:
        title (str): the title of the new Chart
        email (str): will be used to bond chart to user
    Returns:
        dict: includes created Chart object if successful
    """
    email = kwargs.get("email")
    new_chart = Chart(title=str(title))
    print(new_chart)
    user = User.query.filter_by(
        email=email
    ).first()  # Use .first() to retrieve a single User object
    print(user)
    new_chart.user = user
    try:
        db.session.add(new_chart)
        db.session.commit()
        return chart_schema.jsonify(new_chart)
    except Exception as e:
        return jsonify({"error": f"something went wrong in create_task(): {e}"})



@app.route("/create_sample/<title>", methods=["POST"])
# @login_required
@jwt_required
def create_sample_chart(title, **kwargs):
    """
    This also creates a chart, the difference is that it will populate with random data.
    Args:
        title (str): the title of the new Chart
        email (str): will be used to bond chart to user
    Returns:
        dict: includes created Chart object if successful
    """
    email = kwargs.get("email")
    print(f"inside create_sample_chart: {email}")
    new_chart = Chart(title=str(title))
    new_chart.sample_data()
    user = User.query.filter_by(
        email=email
    ).first()  # Use .first() to retrieve a single User object
    new_chart.user = user
    try:
        db.session.add(new_chart)
        db.session.commit()
        return chart_schema.jsonify(new_chart)
    except Exception as e:
        return jsonify({"error": f"something went wrong in create_task(): {e}"})


@app.route("/delete/<int:id>", methods=["DELETE"])
def delete_chart(id):
    """
    Will delete the specified Chart object
    Args:
        id (int): the id of the Chart to delete
    Returns:
        dict: dict with http response
    """
    chart_to_delete = Chart.query.get_or_404(id)
    try:
        db.session.delete(chart_to_delete)
        db.session.commit()
        return {"status": 204}
    except:
        return {"status": 404}


@app.route("/finish/<int:id>", methods=["POST"])
def mark_complete(id):
    """
    Will update the input Chart object to "complete" today
    Args:
        id (int): the id of the Chart to update
    Returns:
        dict: dict with updated data of Chart, to render on front end
    """
    chart = Chart.query.get_or_404(id)
    chart.complete_today()
    db.session.commit()
    return {"data": chart.data}


@app.route("/listall")
@jwt_required
def list_all(**kwargs):
    """
    gets and returns all list belonging to a user
    Args:
        email (str): email to find all Charts bonded to User object
    Returns:
        dict: dict with updated data of Chart, to render on front end
    """
    email = kwargs.get("email")
    print(f"inside list_all: {email}")
    user = User.query.filter_by(email=email).first()
    if user:
        charts = Chart.query.filter_by(user=user).all()
        charts = charts_schema.dump(charts)
        return jsonify(charts)
    else:
        return jsonify({"message": "User not found"})


def add_next_day():
    """
    this function will be triggered everyday, at midnight, to move the Chart object forward
    Args:
        None
    Returns:
        None
    """
    with app.app_context():
        charts = Chart.query.all()
        for chart in charts:
            chart.append_day()
        db.session.commit()


scheduler = BackgroundScheduler()
scheduler.add_job(func=add_next_day, trigger="cron", hour=0, minute=0)
scheduler.start()


if __name__ == "__main__":
    app.run(debug=True)
