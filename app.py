from flask import Flask, request, jsonify,render_template
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy import desc
from flask_cors import CORS

from models import OrderModel
from db import db
from resource.orders import blp as OrderBlueprint


def create_app(db_url=None):
    app = Flask(__name__)
    CORS(app)
    app.config["SQLALCHEMY_DATABASE_URI"] = db_url or "sqlite:///tsm_data_backup.db"
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    db.init_app(app)

    with app.app_context():
        db.create_all()

    app.register_blueprint(OrderBlueprint)

    @app.route('/')
    def order_list():
        return render_template('order_list.html')

    @app.route('/order/<int:order_id>')
    def order_detail(order_id):
        order = OrderModel.query.get_or_404(order_id)
        return render_template('order_detail.html', order=order)

    return app






