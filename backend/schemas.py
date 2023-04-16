from flask_marshmallow import Marshmallow

ma = Marshmallow()

class ChartSchema(ma.Schema):
    class Meta:
        fields = ("id", "title", "year_start", "year_end", "data", "user_id")

chart_schema = ChartSchema()
charts_schema = ChartSchema(many=True)