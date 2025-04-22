class PricingService:
    """Service for retrieving pricing information"""
    
    def __init__(self, prices_data):
        self.prices_data = prices_data
    
    def get_latest_price(self, sku_id):
        """Get the latest price for a SKU"""
        for sku in self.prices_data['skus']:
            if sku['id'] == sku_id:
                latest_pricing_version = max(sku['pricingVersions'], key=lambda x: x['effectiveTime'])
                latest_price = latest_pricing_version['pricingExpressions'][0]['rates'][0]['unitPrice']
                return float(latest_price)
        return 0
    
    def get_sku_name(self, sku_id):
        """Get the name of a SKU"""
        for sku in self.prices_data['skus']:
            if sku['id'] == sku_id:
                return sku['name']
        return 0
    
    def get_sku_unit(self, sku_id):
        """Get the pricing unit of a SKU"""
        for sku in self.prices_data['skus']:
            if sku['id'] == sku_id:
                return sku['pricingUnit']
        return 0
