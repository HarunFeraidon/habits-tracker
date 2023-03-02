from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from flask_cors import CORS

from datetime import date
from apscheduler.schedulers.background import BackgroundScheduler

app = Flask(__name__)
CORS(app)

app.config['SQLALCHEMY_DATABASE_URI'] = "mysql+pymysql://root:@localhost/habits_tracker"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
ma = Marshmallow(app)

class Chart(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(50), nullable=False)
    date_created = db.Column(db.Date, default=date.today())
    data = db.Column(db.String(365))

    def __init__(self, title):
        self.title = title
        today = date.today()
        self.date_created = today
        self.data = "0" * 365

    def complete_today(self):
        lst = list(self.data)
        lst[-1] = '1'
        self.data = "".join(lst)

class ChartSchema(ma.Schema):
    class Meta:
        fields = ('id', 'title', 'date_created', 'data')

chart_schema= ChartSchema()
charts_schema= ChartSchema(many=True)

@app.route('/create', methods=["POST"])
def create_chart():
    chart_title = request.json['title']
    new_chart = Chart(title=chart_title)
    
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
        return chart_schema.jsonify(chart_to_delete)
    except:
        return "something went wrong in delete_chart()" 

@app.route('/finish/<int:id>', methods=['POST'])
def mark_complete(id):
    chart = Chart.query.get_or_404(id)
    chart.complete_today()
    db.session.commit()
    return chart_schema.jsonify(chart)

def shift_data_left():
    # This function will be triggered every day at midnight
    with app.app_context():
        charts = Chart.query.all()
        for chart in charts:
            chart.data = chart.data[1:] + '0'
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
scheduler.add_job(func=shift_data_left, trigger='cron', hour=0, minute=0)
scheduler.start()


if __name__ == '__main__':
    app.run(debug=True)