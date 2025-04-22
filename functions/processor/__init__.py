from processor.base import ResourceProcessor
from processor.compute import ComputeInstanceProcessor, ComputeDiskProcessor, ComputeFilesystemProcessor, ComputeInstanceGroupProcessor
from processor.database import MDBMySQLProcessor, MDBPostgreProcessor, MDBClickhouseProcessor, MDBGreenplumProcessor, MDBKafkaProcessor, MDBRedisProcessor, MDBOpensearchProcessor, MDBYDBProcessor
from processor.kubernetes import KubernetesClusterProcessor, KubernetesNodeGroupProcessor
from processor.network import VPCAddressProcessor

class ProcessorRegistry:
    """Registry for resource processors"""
    
    def __init__(self, pricing_service, resource_spec_service):
        self.processors = []
        self._register_processors(pricing_service, resource_spec_service)
    
    def _register_processors(self, pricing_service, resource_spec_service):
        """Register all available processors"""
        # Compute processors
        self.processors.append(ComputeInstanceProcessor(pricing_service, resource_spec_service))
        self.processors.append(ComputeDiskProcessor(pricing_service, resource_spec_service))
        self.processors.append(ComputeFilesystemProcessor(pricing_service, resource_spec_service))
        self.processors.append(ComputeInstanceGroupProcessor(pricing_service, resource_spec_service))
        
        # Database processors
        self.processors.append(MDBMySQLProcessor(pricing_service, resource_spec_service))
        self.processors.append(MDBPostgreProcessor(pricing_service, resource_spec_service))
        self.processors.append(MDBClickhouseProcessor(pricing_service, resource_spec_service))
        self.processors.append(MDBGreenplumProcessor(pricing_service, resource_spec_service))
        self.processors.append(MDBKafkaProcessor(pricing_service, resource_spec_service))
        self.processors.append(MDBRedisProcessor(pricing_service, resource_spec_service))
        self.processors.append(MDBOpensearchProcessor(pricing_service, resource_spec_service))
        self.processors.append(MDBYDBProcessor(pricing_service, resource_spec_service))
        
        # Kubernetes processors
        self.processors.append(KubernetesClusterProcessor(pricing_service, resource_spec_service))
        self.processors.append(KubernetesNodeGroupProcessor(pricing_service, resource_spec_service))
        
        # Network processors
        self.processors.append(VPCAddressProcessor(pricing_service, resource_spec_service))
    
    def get_processor(self, resource_type):
        """Get a processor for the given resource type"""
        for processor in self.processors:
            if processor.can_process(resource_type):
                return processor
        return None
