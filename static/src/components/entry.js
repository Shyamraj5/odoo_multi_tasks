/** @odoo-module **/
import { registry } from "@web/core/registry";
import { useService } from "@web/core/utils/hooks";
const { Component, useState, onWillStart } = owl;

export class SaleOrderDashboard extends Component {
    setup() {
        this.orm = useService("orm");
        this.model = "sale.order";

        this.state = useState({
            saleOrders: [],
            totalSalePrice: 0,
            totalProfit: 0,
            totalProducts: 0,
            totalOrders: 0,
            monthFilter: "2025-01", // Default to January 2025
        });

        onWillStart(async () => {
            await this.GetSaleOrders();
        });
    }

    async GetSaleOrders() {
        const domain = this.state.monthFilter
            ? [["date_order", ">=", `${this.state.monthFilter}-01`], ["date_order", "<=", `${this.state.monthFilter}-31`]]
            : [];

        // Fetch sale orders for the selected month
        const orders = await this.orm.searchRead(this.model, domain, ["id", "name", "amount_total", "amount_untaxed", "date_order", "state", "order_line"]);

        this.state.saleOrders = orders;
        this.calculateQuickInfo();
    }

    calculateQuickInfo() {
        let totalSalePrice = 0;
        let totalProfit = 0;
        let totalProducts = 0;

        this.state.saleOrders.forEach(order => {
            totalSalePrice += order.amount_total;
            totalProfit += order.amount_untaxed;  // Modify if your profit calculation differs
            totalProducts += order.order_line.length;
        });

        this.state.totalSalePrice = totalSalePrice;
        this.state.totalProfit = totalProfit;
        this.state.totalProducts = totalProducts;
        this.state.totalOrders = this.state.saleOrders.length;
    }

    updateMonthFilter(event) {
        this.state.monthFilter = event.target.value;
        this.GetSaleOrders();  // Reload sale orders based on new filter
    }
}

SaleOrderDashboard.template = "sale_order_dashboard.SaleOrderTemplate";

registry.category("actions").add("owl.action_sale_order_dashboard", SaleOrderDashboard);
