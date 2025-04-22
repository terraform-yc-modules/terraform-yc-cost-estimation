import pytest
from service.pricing import PricingService

class TestPricingService:
    @pytest.fixture
    def sample_prices_data(self):
        return {
            "skus": [
                {
                    "id": "test-sku-1",
                    "name": "Test SKU 1",
                    "pricingUnit": "hour",
                    "pricingVersions": [
                        {
                            "effectiveTime": "2023-01-01T00:00:00Z",
                            "pricingExpressions": [
                                {
                                    "rates": [
                                        {
                                            "unitPrice": "10.0"
                                        }
                                    ]
                                }
                            ]
                        }
                    ]
                }
            ]
        }
    
    def test_get_latest_price(self, sample_prices_data):
        service = PricingService(sample_prices_data)
        price = service.get_latest_price("test-sku-1")
        assert price == 10.0
    
    def test_get_sku_name(self, sample_prices_data):
        service = PricingService(sample_prices_data)
        name = service.get_sku_name("test-sku-1")
        assert name == "Test SKU 1"
    
    def test_get_sku_unit(self, sample_prices_data):
        service = PricingService(sample_prices_data)
        unit = service.get_sku_unit("test-sku-1")
        assert unit == "hour"
    
    def test_nonexistent_sku(self, sample_prices_data):
        service = PricingService(sample_prices_data)
        assert service.get_latest_price("nonexistent") == 0
        assert service.get_sku_name("nonexistent") == 0
        assert service.get_sku_unit("nonexistent") == 0
