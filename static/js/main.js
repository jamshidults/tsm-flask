document.addEventListener('DOMContentLoaded', function() {
    fetch('/orders')
        .then(response => response.json())
        .then(data => {
            let ordersList = document.getElementById('orders-list');
            data.forEach(order => {
                let orderItem = document.createElement('li');
                orderItem.className = 'list-group-item';
                orderItem.innerHTML = `<a href="/order/${order.id}">Order #${order.id} - ${order.reference}</a>`;
                ordersList.appendChild(orderItem);
            });
        })
        .catch(error => console.error('Error fetching orders:', error));
});
