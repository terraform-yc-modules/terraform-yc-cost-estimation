import pytest
from processor.compute import ComputeInstanceProcessor
from unittest.mock import Mock

class TestComputeInstanceProcessor:
    @pytest.fixture
    def usage_collector_mock(self):
        mock = Mock()
        return mock
    
    @pytest.fixture
    def pricing_service_mock(self):
        mock = Mock()
        return mock
    
    @pytest.fixture
    def resource_spec_service_mock(self):
        mock = Mock()
        return mock
    
    def test_can_process(self, pricing_service_mock, resource_spec_service_mock):
        processor = ComputeInstanceProcessor(pricing_service_mock, resource_spec_service_mock)
        assert processor.can_process("yandex_compute_instance") is True
        assert processor.can_process("other_resource") is False
    
    def test_process_standard_v3(self, usage_collector_mock, pricing_service_mock, resource_spec_service_mock):
        processor = ComputeInstanceProcessor(pricing_service_mock, resource_spec_service_mock)
        
        # Create a sample resource for standard-v3 platform
        resource = {
            "type": "yandex_compute_instance",
            "name": "test-instance",
            "values": {
                "platform_id": "standard-v3",
                "resources": [
                    {
                        "cores": 2,
                        "memory": 4,
                        "core_fraction": 100,
                        "gpus": 0
                    }
                ],
                "scheduling_policy": [
                    {
                        "preemptible": False
                    }
                ],
                "network_interface": [
                    {
                        "nat": True
                    }
                ],
                "boot_disk": [
                    {
                        "initialize_params": [
                            {
                                "size": 20,
                                "type": "network-ssd"
                            }
                        ]
                    }
                ]
            }
        }
        
        processor.process(resource, usage_collector_mock)
        
        # Verify the usage collector was called with the right parameters
        # For standard-v3, non-preemptible, 100% core fraction
        usage_collector_mock.add_usage.assert_any_call(
            "dn2k3vqlk9snp1jv351u", 2, "test-instance", "yandex_compute_instance"
        )
        # For RAM
        usage_collector_mock.add_usage.assert_any_call(
            "dn2ilq72mjc3bej6j74p", 4, "test-instance", "yandex_compute_instance"
        )
        # For boot disk
        usage_collector_mock.add_usage.assert_any_call(
            "dn27ajm6m8mnfcshbi61", 20, "test-instance", "yandex_compute_instance"
        )
        # For public IP
        usage_collector_mock.add_usage.assert_any_call(
            "dn229q5mnmp58t58tfel", 1, "test-instance", "yandex_compute_instance"
        )
