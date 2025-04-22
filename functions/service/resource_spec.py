class ResourceSpecService:
    """Service for retrieving resource specifications"""
    
    def __init__(self, mdb_data):
        self.mdb_data = mdb_data
    
    def get_mdb_preset(self, service_type, preset_id):
        """Get MDB preset specifications"""
        service_data = self.mdb_data.get(service_type)
        if not service_data:
            raise ValueError(f"Service type '{service_type}' not found in the data structure")
        
        preset_data = service_data.get(preset_id)
        if not preset_data:
            raise ValueError(f"Preset ID '{preset_id}' not found in service type '{service_type}'")
        
        cores = preset_data.get("cores")
        core_fraction = preset_data.get("core_fraction")
        memory = preset_data.get("memory")
        
        if preset_id.startswith("s1") or preset_id.startswith("b1") or preset_id.startswith("hm1"):
            platform_id = "standard-v1"
        elif preset_id.startswith("s2") or preset_id.startswith("b2") or preset_id.startswith("m2") or preset_id.startswith("hm2") or preset_id.startswith("i2"):
            platform_id = "standard-v2"
        elif preset_id.startswith("s3") or preset_id.startswith("m3") or preset_id.startswith("c3") or preset_id.startswith("hm3") or preset_id.startswith("i3"):
            platform_id = "standard-v3"
        elif preset_id.startswith("s3f") or preset_id.startswith("m3f") or preset_id.startswith("c3f") or preset_id.startswith("i3f"): 
            platform_id = "highfreq-v3"
        else:
            platform_id = None

        return cores, core_fraction, memory, platform_id
