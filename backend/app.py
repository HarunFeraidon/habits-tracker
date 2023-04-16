import os
from dotenv import load_dotenv
from flask import Flask, jsonify, request
from flask_cors import CORS
import jwt
from functools import wraps
from datetime import datetime, timedelta
from apscheduler.schedulers.background import BackgroundScheduler

from models import db, migrate, User, Chart
from schemas import ma, chart_schema, charts_schema

app = Flask(__name__)
CORS(app)

load_dotenv()

app.config["SQLALCHEMY_DATABASE_URI"] = "mysql+pymysql://root:@localhost/habits_tracker"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["SECRET_KEY"] = os.environ.get("SECRET_KEY")

db.init_app(app)
migrate.init_app(app, db)
ma.init_app(app)


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

@app.route("/")
def home():
    return "Welcome to My Flask Application!"



scheduler = BackgroundScheduler()
scheduler.add_job(func=add_next_day, trigger="cron", hour=0, minute=0)
scheduler.start()


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)