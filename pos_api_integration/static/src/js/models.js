/** @odoo-module **/

import {Order} from 'point_of_sale.models';
const Registries = require('point_of_sale.Registries');

const PosAPIOrder = (Order) => class PosAPIOrder extends Order {

    async push_order_data(){
        const order = this.export_as_JSON();
        var order_lines = [];
        var payment_lines = [];
        order.lines.forEach(item => {
            var line = item[2];
            var lot_lines = [];
            line.pack_lot_ids.forEach(item => {
                var lot_line = item[2];
                var line_data = {
                    lot_id: false,
                    lot_name: lot_line.lot_name,
                    product: line.product_id,
                    quantity: 0.0
                }
                lot_lines.push(line_data);
            });
            var line_data = {
                product: line.product_id,
                quantity: line.qty,
                price_unit: line.price_unit,
                discount: line.discount,
                subtotal: line.price_subtotal,
                tax: (line.price_subtotal_incl - line.price_subtotal).toFixed(2),
                subtotal_incl: line.price_subtotal_incl,
                lots: lot_lines
            }
            order_lines.push(line_data);
        });
        order.statement_ids.forEach(item => {
            var line = item[2];
            console.log(typeof line.name);
            var line_data = {
                payment_date: line.name,
                payment_method: line.payment_method_id,
                amount: line.amount
            }
            payment_lines.push(line_data);
            
        });
        var order_data = {
            reference: order.uid,
            pos_reference: order.name,
            total: order.amount_total,
            date: order.creation_date.toLocaleString(),
            session: order.pos_session_id,
            user: order.user_id,
            customer: order.partner_id,
            status: '',
            orderlines: order_lines,
            payment_data: payment_lines
        }
        var url = this.pos.config.pos_order_sync_api;
        if (url && order_data){
            $.ajax({
                url: url,
                type: 'POST',
                contentType: 'application/json',
                data: JSON.stringify(order_data),
                success: function(response) {
                    console.log('Success:', response);
                },
                error: function(error) {
                    console.error('Error:', error);
                }
            });
        }
    }

    export_for_printing(){
        this.push_order_data();
        return super.export_for_printing();
    }

};
Registries.Model.extend(Order, PosAPIOrder);
return Order;