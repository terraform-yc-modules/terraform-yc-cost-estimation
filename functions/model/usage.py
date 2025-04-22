from collections import defaultdict
import logging

class UsageCollector:
    """Collects and manages resource usage data"""
    
    def __init__(self, pricing_service):
        self.usage = []
        self.pricing_service = pricing_service
    
    def add_usage(self, sku, amount, resource_name, resource_type):
        """Add a usage record to the collector"""
        self.usage.append({
            "sku": sku, 
            "amount": amount, 
            "resource_name": resource_name, 
            "resource_type": resource_type
        })
    
    def get_usage(self):
        """Get a summarized view of usage data"""
        summary = defaultdict(lambda: {"amount": 0, "cost": 0.0})

        for item in self.usage:
            sku = item.get("sku")
            full_name = self.pricing_service.get_sku_name(sku)
            amount = item.get("amount")
            cost = self.pricing_service.get_latest_price(sku) * amount
            unit = self.pricing_service.get_sku_unit(sku)
            resource_name = item.get("resource_name")
            resource_type = item.get("resource_type")

            key = (sku, full_name, unit, resource_name, resource_type)
            summary[key]["amount"] += amount
            summary[key]["cost"] += cost
        
        # Convert the summary to a list of dictionaries with lowercase keys
        result = []
        for key, value in summary.items():
            sku, full_name, unit, resource_name, resource_type = key
            result.append({
                "sku_id": sku,
                "sku_name": full_name,
                "amount": value["amount"],
                "cost": value["cost"],
                "unit": unit,
                "resource_name": resource_name,
                "resource_type": resource_type
            })

        return result
    
    def print_usage(self):
        """Print usage data in a tabular format"""
        try:
            from tabulate import tabulate
            
            table_data = []
            headers = ["SKU", "Description", "Amount", "Cost(RUB)", "Unit", "Resource Name", "Resource Type"]

            summary = defaultdict(lambda: {"amount": 0, "cost": 0.0})

            for item in self.usage:
                sku = item.get("sku")
                full_name = self.pricing_service.get_sku_name(sku)
                amount = item.get("amount")
                cost = self.pricing_service.get_latest_price(sku) * amount
                unit = self.pricing_service.get_sku_unit(sku)
                resource_name = item.get("resource_name")
                resource_type = item.get("resource_type")

                key = (sku, full_name, unit, resource_name, resource_type)
                summary[key]["amount"] += amount
                summary[key]["cost"] += cost

            for key, value in summary.items():
                sku, full_name, unit, resource_name, resource_type = key
                row = [
                    sku,
                    full_name,
                    value["amount"],
                    f"{value['cost']:.2f}",
                    unit,
                    resource_name,
                    resource_type
                ]
                table_data.append(row)

            print(tabulate(table_data, headers=headers, tablefmt="grid"))
        except ImportError:
            logging.warning("tabulate package not found, using simple print instead")
            for item in self.get_usage():
                print(item)
    
    def calculate_total(self):
        """Calculate the total cost of all usage"""
        total = 0
        for item in self.usage:
            sku_id = item['sku']
            amount = item['amount']
            latest_price = self.pricing_service.get_latest_price(sku_id)
            total += amount * latest_price
            logging.info(f"{sku_id} - {amount * latest_price * 24 * 30}")
        return total
    
    def clear(self):
        """Clear all usage data"""
        self.usage.clear()
