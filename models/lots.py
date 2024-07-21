from db import db

class LotModel(db.Model):
    __tablename__ = "lots"
    id = db.Column(db.Integer, primary_key=True)
    lot_id = db.Column(db.Integer)
    lot_name = db.Column(db.String(80))
    product = db.Column(db.Integer)
    order_line_id = db.Column(db.Integer, db.ForeignKey("orderlines.id"), nullable=False)
    orderline = db.relationship("OrderLineModel", back_populates="lots")
    order_id = db.Column(db.Integer, db.ForeignKey("orders.id"), unique=False, nullable=False)
    order = db.relationship("OrderModel", back_populates="lots")
    quantity = db.Column(db.Float(precision=2))

    def json(self):
        return {
            "id": self.id,
            "lot_id":self.lot_id,
            "lot_name": self.lot_name,
            "product": self.product,
            "order_line_id": self.order_line_id,
            "order_id":self.order_id,
            "quantity": self.quantity
        }
