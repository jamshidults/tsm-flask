from db import db

class PaymentModel(db.Model):
    __tablename__ = "payments"
    id = db.Column(db.Integer, primary_key=True)
    payment_date = db.Column(db.String(80))
    payment_method = db.Column(db.Integer)
    amount = db.Column(db.Float(precision=2))
    order_id = db.Column(db.Integer, db.ForeignKey("orders.id"), nullable=False)
    order = db.relationship("OrderModel", back_populates="payments")

    def json(self):
        return {
            "id": self.id,
            "payment_date": self.payment_date,
            "payment_method": self.payment_method,
            "amount": self.amount,
            "order_id": self.order_id
        }
