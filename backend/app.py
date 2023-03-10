from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_marshmallow import Marshmallow
from flask_cors import CORS
import json

from datetime import date, datetime, timedelta
from apscheduler.schedulers.background import BackgroundScheduler

app = Flask(__name__)
CORS(app)

app.config['SQLALCHEMY_DATABASE_URI'] = "mysql+pymysql://root:@localhost/habits_tracker"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
migrate = Migrate(app, db)
ma = Marshmallow(app)

class Chart(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(50), nullable=False)
    year_start = db.Column(db.Date)
    year_end = db.Column(db.Date)
    data = db.Column(db.JSON)

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
        fields = ('id', 'title', 'date_created', 'year_start', 'year_end', 'data')

chart_schema= ChartSchema()
charts_schema= ChartSchema(many=True)

@app.route('/inspect/<int:id>', methods=["GET"])
def inspect(id):
    chart = Chart.query.get_or_404(id)
    return chart.data

@app.route('/create/<title>', methods=["POST"])
def create_chart(title):
    new_chart = Chart(title=str(title))
    
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
def list_all():
    charts = Chart.query.all()
    charts = charts_schema.dump(charts)
    return jsonify(charts)

scheduler = BackgroundScheduler()
scheduler.add_job(func=add_next_day, trigger='cron', hour=0, minute=0)
scheduler.start()


if __name__ == '__main__':
    app.run(debug=True)