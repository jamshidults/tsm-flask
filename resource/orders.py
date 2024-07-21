from flask import Blueprint, request, jsonify
from app import db
from models import OrderModel,OrderLineModel,PaymentModel,LotModel

blp = Blueprint('orders', __name__)


@blp.route('/orders', methods=['GET'])
def get_orders():
    search_term = request.args.get('search', '').lower()

    # Filter orders based on search term
    query = OrderModel.query
    if search_term:
        query = query.filter(
            (OrderModel.pos_reference.ilike(f'%{search_term}%')) |
            (OrderModel.id == int(search_term) if search_term.isdigit() else -1)
        )

    orders = query.order_by(OrderModel.id.desc()).limit(1000).all()
    data = [order.json() for order in orders]

    return jsonify(data), 200

@blp.route('/orders', methods=['POST'])
def create_order():
    data = request.get_json()
    ip_address = request.remote_addr  # Get the IP address of the client
    # Create the order
    new_order = OrderModel(
        reference=data.get('reference'),
        pos_reference=data.get('pos_reference'),
        total=data.get('total'),
        date=data.get('date'),
        session=data.get('session'),
        user=data.get('user'),
        customer=data.get('customer'),
        ip_address=ip_address,
        status=data.get('status')
    )

    # Add order lines and their lot details
    orderlines = data.get('orderlines', [])
    for ol_data in orderlines:
        new_orderline = OrderLineModel(
            product=ol_data.get('product'),
            quantity=ol_data.get('quantity'),
            price_unit=ol_data.get('price_unit'),
            discount=ol_data.get('discount'),
            subtotal=ol_data.get('subtotal'),
            tax=ol_data.get('tax'),
            subtotal_incl=ol_data.get('subtotal_incl')
        )

        # Add lots
        lots = ol_data.get('lots', [])
        for lot_data in lots:
            new_lot = LotModel(
                lot_name=lot_data.get('lot_name'),
                lot_id=lot_data.get('lot_id'),
                product=lot_data.get('product'),
                quantity=lot_data.get('quantity')
            )
            new_orderline.lots.append(new_lot)
            new_order.lots.append(new_lot)

        new_order.orderlines.append(new_orderline)


    # Add payments
    payments = data.get('payment_data', [])
    for payment_data in payments:
        new_payment = PaymentModel(
            payment_date=payment_data.get('payment_date'),
            payment_method=payment_data.get('payment_method'),
            amount=payment_data.get('amount')
        )
        new_order.payments.append(new_payment)

    db.session.add(new_order)
    db.session.commit()

    return jsonify(new_order.json()), 201




