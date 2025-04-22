class ResourceProcessor:
    """Base class for all resource processors"""
    
    def __init__(self, pricing_service, resource_spec_service):
        self.pricing_service = pricing_service
        self.resource_spec_service = resource_spec_service
    
    def can_process(self, resource_type):
        """Check if this processor can handle the given resource type"""
        return False
    
    def process(self, resource, usage_collector):
        """Process a resource and add usage to the collector"""
        pass
