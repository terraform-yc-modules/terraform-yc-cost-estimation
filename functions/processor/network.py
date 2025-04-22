from processor.base import ResourceProcessor

class VPCAddressProcessor(ResourceProcessor):
    """Processor for VPC Address resources"""
    
    def can_process(self, resource_type):
        return resource_type == "yandex_vpc_address"
    
    def process(self, resource, usage_collector):
        resource_type = resource["type"]
        resource_name = resource["name"]
        resource_values = resource["values"]

        if resource_values.get("external_ipv4_address"):
            usage_collector.add_usage("dn229q5mnmp58t58tfel", 1, resource_name, resource_type) # Public IP address [gbyte*hour]

        return 0
