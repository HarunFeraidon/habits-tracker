import os
from dotenv import load_dotenv
from flask import Flask, jsonify, request, url_for, render_template, redirect
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_marshmallow import Marshmallow
from flask_cors import CORS
from flask_login import LoginManager, current_user, login_required, login_user, UserMixin
import json
import jwt
from functools import wraps

from datetime import date, datetime, timedelta
from apscheduler.schedulers.background import BackgroundScheduler

app = Flask(__name__)
CORS(app)

login_manager = LoginManager()
login_manager.init_app(app)

load_dotenv()

app.config['SQLALCHEMY_DATABASE_URI'] = "mysql+pymysql://root:@localhost/habits_tracker"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY')

@login_manager.user_loader
def load_user(user_id):
    return User.query.get_or_404(user_id)

@app.route('/userinfo')
def user_info():
    if current_user.is_authenticated:
        user = {
            'id': current_user.id,
            'email': current_user.email,
            'authenticated': True,
            # add any other fields you want to return
        }
        return jsonify(user)
    else:
        return jsonify({'message': 'User is not logged in', 'authenticated': False})


db = SQLAlchemy(app)
migrate = Migrate(app, db)
ma = Marshmallow(app)

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(50), unique=True, nullable=False)
    charts = db.relationship('Chart', backref='user', lazy=True)

class Chart(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(50), nullable=False)
    year_start = db.Column(db.Date)
    year_end = db.Column(db.Date)
    data = db.Column(db.JSON)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

    def __init__(self, title):
        self.title = title
        reference_year = date.today().year
        self.year_start = datetime(reference_year, 1, 1)
        self.year_end = datetime(reference_year, 12, 31)
        self.data = self.init_data()
    
    def init_data(self):
        data_list = []
        data_list.append({"value": 0, "day": date.today().strftime('%Y-%m-%d')})
        return json.dumps(data_list)
    
    def complete_today(self):
        all_data = json.loads(self.data)
        all_data[-1]['value'] = 1
        self.data = json.dumps(all_data)

    def append_day(self):
        all_data = json.loads(self.data)
        all_data.append({"value": 0, "day": datetime.now().strftime('%Y-%m-%d')})
        if(date.today().year != self.year_end):
            reference_year = date.today().year
            self.year_end = datetime(reference_year, 12, 31)
        self.data = json.dumps(all_data)
        

class ChartSchema(ma.Schema):
    class Meta:
        fields = ('id', 'title', 'year_start', 'year_end', 'data', 'user_id')

chart_schema= ChartSchema()
charts_schema= ChartSchema(many=True)

@app.route('/create_user', methods=['POST'])
def create_user():
    email = request.form['email']
    user = User.query.filter_by(email=email).first()
    token = jwt.encode({
            'email': email,
            'exp': datetime.utcnow() + timedelta(minutes=30) # set token expiration time
        }, app.config['SECRET_KEY'], algorithm='HS256')

    if user is None:
        user = User(email=email)
        db.session.add(user)
        db.session.commit()
        return jsonify({
            'message': f"User with email '{email}' has been created!",
            'token': token # .decode('utf-8')
        }), 200
    else:
        return jsonify({
            'message': f"User with email '{email}' already exists.",
            'token': token # .decode('utf-8')
        }), 200
    
# Function to decode and verify JWT token
def decode_jwt(token):
    try:
        # Decode and verify JWT token using secret key
        payload = jwt.decode(token, app.config['SECRET_KEY'], algorithms=['HS256'])
        return payload
    except jwt.ExpiredSignatureError:
        # Handle expired token
        return None
    except jwt.InvalidTokenError:
        # Handle invalid token
        return None

def jwt_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        token = request.headers.get('Authorization')  # Get JWT token from request headers
        print(f"token: {token}")
        if token:
            decoded_token = decode_jwt(token)  # Decode and verify JWT token
            print(decoded_token)
            print(f"type(decoded_token) {decoded_token}")
            if decoded_token:
                # Token is valid, continue processing the route
                email = decoded_token['email']
                # print(email)
                # Retrieve user information based on the email or other identifier
                # ... (your code here)
                print("Authenticated route: Hello, {}".format(email))
            return f(*args, **kwargs)
        return jsonify({'error': 'Authentication failed.'}), 401
    return decorated_function

# Example of a protected route using the 'jwt_required' decorator
@app.route('/api/protected')
@jwt_required  # Apply 'jwt_required' decorator to protect this route
def protected_route():
    print("ligma ligma ligma")
    return jsonify({'message': 'This is a protected route. Authentication successful.'})


# Example route using JWT authentication
@app.route('/authenticated_route')
def authenticated_route():
    token = request.headers.get('Authorization')  # Get JWT token from request headers
    print(f"token: {token}")
    if token:
        decoded_token = decode_jwt(token)  # Decode and verify JWT token
        print(decoded_token)
        print(f"type(decoded_token) {decoded_token}")
        if decoded_token:
            # Token is valid, continue processing the route
            email = decoded_token['email']
            # print(email)
            # Retrieve user information based on the email or other identifier
            # ... (your code here)
            return "Authenticated route: Hello, {}".format(email)
        else:
            # Token is invalid or expired, return error response
            return "Unauthorized", 401
    else:
        # Token is missing, return error response
        return "Unauthorized", 401

@app.route('/inspect/<int:id>', methods=["GET"])
def inspect(id):
    chart = Chart.query.get_or_404(id)
    return chart.data

@app.route('/create/<title>', methods=["POST"])
# @login_required
def create_chart(title):
    new_chart = Chart(title=str(title))
    new_chart.user = current_user
    try:
        db.session.add(new_chart)
        db.session.commit()
        return chart_schema.jsonify(new_chart)
    except Exception as e:
        return f"something went wrong in create_task(): {e}"
    
@app.route('/create_bf', methods=["POST"])
def create_bf():
    new_chart = Chart(title=request.json["title"])
    new_chart.data = json.dumps(request.json["data"])
    try:
        db.session.add(new_chart)
        db.session.commit()
        return chart_schema.jsonify(new_chart)
    except Exception as e:
        return f"something went wrong in create_task(): {e}"
    
@app.route('/delete/<int:id>', methods=['DELETE'])
# @login_required
def delete_chart(id):
    chart_to_delete = Chart.query.get_or_404(id)
    try:
        db.session.delete(chart_to_delete)
        db.session.commit()
        return {"status" : 204}
    except:
        return {"status" : 404}

@app.route('/finish/<int:id>', methods=['POST'])
def mark_complete(id):
    chart = Chart.query.get_or_404(id)
    chart.complete_today()
    db.session.commit()
    return {"data" : chart.data}

def add_next_day():
    # This function will be triggered every day at midnight
    with app.app_context():
        charts = Chart.query.all()
        for chart in charts:
            chart.append_day()
        db.session.commit()

@app.route('/get/<int:id>', methods=['GET'])
def getChart(id):
    chart = Chart.query.get_or_404(id)
    return chart_schema.jsonify(chart)

@app.route('/listall')
# @login_required
def list_all():
    charts = Chart.query.filter_by(user_id=current_user.id).all()
    charts = charts_schema.dump(charts)
    return jsonify(charts)

scheduler = BackgroundScheduler()
scheduler.add_job(func=add_next_day, trigger='cron', hour=0, minute=0)
scheduler.start()


if __name__ == '__main__':
    app.run(debug=True)