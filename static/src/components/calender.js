/** @odoo-module **/
import { useState } from "@web/core/utils/hooks";
import { useService } from "@web/core/utils/hooks";
import { Component } from "@odoo/owl";

export class SaleOrderCalendar extends Component {
    setup() {
        this.state = useState({
            saleOrders: [],
        });

        this.orm = useService("orm");
        this.model = "sale.order";

        this.loadSaleOrders();
    }

    async loadSaleOrders() {
        const orders = await this.orm.searchRead(this.model, [], ["date_order", "name"]);
        this.state.saleOrders = orders;

        this.initializeCalendar();
    }

    initializeCalendar() {
        const events = this.state.saleOrders.map(order => ({
            title: order.name,
            start: order.date_order,
        }));

        // Initialize FullCalendar with sale order events
        const calendar = new FullCalendar.Calendar(document.getElementById('calendar'), {
            events: events,
        });
        calendar.render();
    }
}
