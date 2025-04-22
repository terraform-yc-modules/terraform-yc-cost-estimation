import pytest
from service.resource_spec import ResourceSpecService

class TestResourceSpecService:
    @pytest.fixture
    def sample_mdb_data(self):
        return {
            "mysql": {
                "s1.micro": {
                    "cores": 1,
                    "memory": 2,
                    "core_fraction": 100
                }
            }
        }
    
    def test_get_mdb_preset(self, sample_mdb_data):
        service = ResourceSpecService(sample_mdb_data)
        cores, core_fraction, memory, platform_id = service.get_mdb_preset("mysql", "s1.micro")
        assert cores == 1
        assert memory == 2
        assert core_fraction == 100
        assert platform_id == "standard-v1"
    
    def test_platform_id_detection(self, sample_mdb_data):
        service = ResourceSpecService(sample_mdb_data)
        
        # Test different preset IDs for platform detection
        _, _, _, platform_id_s1 = service.get_mdb_preset("mysql", "s1.micro")
        assert platform_id_s1 == "standard-v1"
        
        # Add more test data for other platform types
        sample_mdb_data["mysql"]["s2.micro"] = {"cores": 1, "memory": 2, "core_fraction": 100}
        _, _, _, platform_id_s2 = service.get_mdb_preset("mysql", "s2.micro")
        assert platform_id_s2 == "standard-v2"
        
        sample_mdb_data["mysql"]["s3.micro"] = {"cores": 1, "memory": 2, "core_fraction": 100}
        _, _, _, platform_id_s3 = service.get_mdb_preset("mysql", "s3.micro")
        assert platform_id_s3 == "standard-v3"
    
    def test_service_not_found(self, sample_mdb_data):
        service = ResourceSpecService(sample_mdb_data)
        with pytest.raises(ValueError, match="Service type 'nonexistent' not found"):
            service.get_mdb_preset("nonexistent", "s1.micro")
    
    def test_preset_not_found(self, sample_mdb_data):
        service = ResourceSpecService(sample_mdb_data)
        with pytest.raises(ValueError, match="Preset ID 'nonexistent' not found"):
            service.get_mdb_preset("mysql", "nonexistent")
