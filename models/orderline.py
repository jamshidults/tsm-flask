from db import db
class OrderLineModel(db.Model):
    __tablename__ = "orderlines"
    id = db.Column(db.Integer, primary_key=True)
    order_id = db.Column(db.Integer, db.ForeignKey("orders.id"), unique=False, nullable=False)
    order = db.relationship("OrderModel", back_populates="orderlines")
    product = db.Column(db.Integer)
    price_unit = db.Column(db.Float(precision=2))
    discount = db.Column(db.Float(precision=2))
    quantity = db.Column(db.Float(precision=2))
    subtotal = db.Column(db.Float(precision=2))
    tax = db.Column(db.Float(precision=2))
    subtotal_incl = db.Column(db.Float(precision=2))
    lots = db.relationship("LotModel", back_populates="orderline", lazy="dynamic", cascade="all, delete-orphan")

    def json(self):
        return {
            "id": self.id,
            "product": self.product,
            "quantity":self.quantity,
            "price_unit": self.price_unit,
            "discount": self.discount,
            "subtotal": self.subtotal,
            "tax": self.tax,
            "subtotal_incl": self.subtotal_incl,
            "lots": [lot.json() for lot in self.lots]
        }
