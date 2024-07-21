from db import db
class OrderModel(db.Model):
    __tablename__ = "orders"
    id = db.Column(db.Integer, primary_key=True)
    reference = db.Column(db.String(80), unique=False)
    pos_reference = db.Column(db.String(80), unique=False)
    total = db.Column(db.Float(precision=2), unique=False)
    tax = db.Column(db.Float(precision=2))
    date = db.Column(db.String(80))
    session = db.Column(db.Integer)
    user = db.Column(db.Integer)
    customer = db.Column(db.Integer)
    ip_address = db.Column(db.String(45))
    status = db.Column(db.String(40))
    orderlines = db.relationship("OrderLineModel", back_populates="order", lazy="dynamic", cascade="all, delete-orphan")
    payments = db.relationship("PaymentModel", back_populates="order", lazy="dynamic", cascade="all, delete-orphan")
    lots = db.relationship("LotModel", back_populates="order", lazy="dynamic", cascade="all, delete-orphan")
    def json(self):
        return {
            "id": self.id,
            "reference": self.reference,
            "pos_reference":self.pos_reference,
            "ip_address": self.ip_address,
            "date":self.date,
            "total": self.total,
            "tax": self.tax,
            "orderlines": [orderline.json() for orderline in self.orderlines],
            "payments": [payment.json() for payment in self.payments]
        }
