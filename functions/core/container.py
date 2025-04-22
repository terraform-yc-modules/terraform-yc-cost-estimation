import json
import logging
from service.pricing import PricingService
from service.resource_spec import ResourceSpecService
from core.estimator import TerraformCostEstimator

class Container:
    """Dependency injection container"""
    
    _instance = None
    
    @classmethod
    def get_instance(cls):
        """Get or create the singleton instance"""
        if cls._instance is None:
            cls._instance = Container()
        return cls._instance
    
    def __init__(self):
        self._services = {}
        self._initialized = False
    
    def initialize(self, sku_path='./sku.json', mdb_path='./mdb.json'):
        """Initialize the container with required services"""
        if self._initialized:
            return
        
        # Load data files
        try:
            with open(sku_path) as f:
                prices = json.load(f)
            
            with open(mdb_path) as f:
                mdb = json.load(f)
                
            # Create services
            pricing_service = PricingService(prices)
            resource_spec_service = ResourceSpecService(mdb)
            
            # Register services
            self._services['pricing_service'] = pricing_service
            self._services['resource_spec_service'] = resource_spec_service
            self._services['estimator'] = TerraformCostEstimator(
                pricing_service, resource_spec_service
            )
            
            self._initialized = True
            logging.info("Container initialized successfully")
        except Exception as e:
            logging.error(f"Failed to initialize container: {str(e)}")
            raise
    
    def get(self, service_name):
        """Get a service by name"""
        if not self._initialized:
            self.initialize()
        
        if service_name not in self._services:
            raise KeyError(f"Service '{service_name}' not found in container")
        
        return self._services[service_name]
