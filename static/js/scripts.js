document.addEventListener("DOMContentLoaded", function() {
    const ordersContainer = document.getElementById('orders-container');
    const pagination = document.getElementById('pagination');

    function fetchOrders(page = 1) {
        fetch(`/orders?page=${page}`)
            .then(response => response.json())
            .then(data => {
                const orders = data.items;
                const totalPages = data.pages;
                let tableHtml = `
                    <table class="table table-striped">
                        <thead>
                            <tr>
                                <th>ID</th>
                                <th>Reference</th>
                                <th>Total</th>
                                <th>Tax</th>
                                <th>Date</th>
                            </tr>
                        </thead>
                        <tbody>
                `;

                orders.forEach(order => {
                    tableHtml += `
                        <tr>
                            <td>${order.id}</td>
                            <td>${order.reference}</td>
                            <td>${order.total}</td>
                            <td>${order.tax}</td>
                            <td>${order.date}</td>
                        </tr>
                    `;
                });

                tableHtml += `
                        </tbody>
                    </table>
                `;

                ordersContainer.innerHTML = tableHtml;

                let paginationHtml = '';
                if (data.has_prev) {
                    paginationHtml += `<li class="page-item"><a class="page-link" href="#" onclick="fetchOrders(${data.page - 1})">Previous</a></li>`;
                }

                for (let i = 1; i <= totalPages; i++) {
                    paginationHtml += `<li class="page-item ${data.page === i ? 'active' : ''}"><a class="page-link" href="#" onclick="fetchOrders(${i})">${i}</a></li>`;
                }

                if (data.has_next) {
                    paginationHtml += `<li class="page-item"><a class="page-link" href="#" onclick="fetchOrders(${data.page + 1})">Next</a></li>`;
                }

                pagination.innerHTML = paginationHtml;
            });
    }

    fetchOrders(); // Fetch the first page by default
});
