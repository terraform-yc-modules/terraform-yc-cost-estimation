import pytest
from model.usage import UsageCollector
from unittest.mock import Mock

class TestUsageCollector:
    @pytest.fixture
    def pricing_service_mock(self):
        mock = Mock()
        mock.get_sku_name.return_value = "Test SKU"
        mock.get_sku_unit.return_value = "hour"
        mock.get_latest_price.return_value = 10.0
        return mock
    
    def test_add_usage(self, pricing_service_mock):
        collector = UsageCollector(pricing_service_mock)
        collector.add_usage("test-sku", 5, "test-resource", "test-type")
        
        usage = collector.usage
        assert len(usage) == 1
        assert usage[0]["sku"] == "test-sku"
        assert usage[0]["amount"] == 5
        assert usage[0]["resource_name"] == "test-resource"
        assert usage[0]["resource_type"] == "test-type"
    
    def test_get_usage(self, pricing_service_mock):
        collector = UsageCollector(pricing_service_mock)
        collector.add_usage("test-sku", 5, "test-resource", "test-type")
        
        usage = collector.get_usage()
        assert len(usage) == 1
        assert usage[0]["sku_id"] == "test-sku"
        assert usage[0]["sku_name"] == "Test SKU"
        assert usage[0]["amount"] == 5
        assert usage[0]["cost"] == 50.0  # 5 * 10.0
        assert usage[0]["unit"] == "hour"
        assert usage[0]["resource_name"] == "test-resource"
        assert usage[0]["resource_type"] == "test-type"
    
    def test_calculate_total(self, pricing_service_mock):
        collector = UsageCollector(pricing_service_mock)
        collector.add_usage("test-sku-1", 5, "test-resource-1", "test-type")
        collector.add_usage("test-sku-2", 3, "test-resource-2", "test-type")
        
        # Both SKUs have price 10.0 from our mock
        total = collector.calculate_total()
        assert total == 80.0  # (5 + 3) * 10.0
    
    def test_clear(self, pricing_service_mock):
        collector = UsageCollector(pricing_service_mock)
        collector.add_usage("test-sku", 5, "test-resource", "test-type")
        collector.clear()
        
        assert len(collector.usage) == 0
