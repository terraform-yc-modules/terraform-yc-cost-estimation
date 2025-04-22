import logging
from service.pricing import PricingService
from service.resource_spec import ResourceSpecService
from model.usage import UsageCollector
from processor import ProcessorRegistry

class TerraformCostEstimator:
    """Main application class for estimating Terraform costs"""
    
    def __init__(self, pricing_service, resource_spec_service):
        self.pricing_service = pricing_service
        self.resource_spec_service = resource_spec_service
        self.processor_registry = ProcessorRegistry(self.pricing_service, self.resource_spec_service)
    
    def process_plan(self, tf_plan, param_full):
        """Process a Terraform plan and estimate costs with comparison"""
        # Process prior state (current infrastructure)
        prior_collector = UsageCollector(self.pricing_service)
        prior_collector.clear()
        
        if "prior_state" in tf_plan and "values" in tf_plan["prior_state"] and "root_module" in tf_plan["prior_state"]["values"]:
            prior_resources = tf_plan["prior_state"]["values"]["root_module"].get("resources", [])
            for resource in prior_resources:
                resource_type = resource["type"]
                processor = self.processor_registry.get_processor(resource_type)
                
                if processor:
                    processor.process(resource, prior_collector)
                    logging.info(f'Prior state: {resource_type} is processed.')
                else:
                    logging.info(f'Prior state: {resource_type} is ignored.')
        
        # Process planned values (future infrastructure)
        planned_collector = UsageCollector(self.pricing_service)
        planned_collector.clear()
        
        if "planned_values" in tf_plan and "root_module" in tf_plan["planned_values"]:
            planned_resources = tf_plan["planned_values"]["root_module"].get("resources", [])
            for resource in planned_resources:
                resource_type = resource["type"]
                processor = self.processor_registry.get_processor(resource_type)
                
                if processor:
                    processor.process(resource, planned_collector)
                    logging.info(f'Planned values: {resource_type} is processed.')
                else:
                    logging.info(f'Planned values: {resource_type} is ignored.')
        
        # Calculate costs
        prior_hourly = prior_collector.calculate_total()
        prior_monthly = prior_hourly * 24 * 31
        
        planned_hourly = planned_collector.calculate_total()
        planned_monthly = planned_hourly * 24 * 31
        
        # Calculate difference
        diff_hourly = planned_hourly - prior_hourly
        diff_monthly = diff_hourly * 24 * 31
        diff_percentage = (diff_hourly / prior_hourly * 100) if prior_hourly > 0 else 0
        
        # Apply a small threshold to avoid floating point issues
        has_changes = abs(diff_hourly) > 0.01
        
        # Prepare result
        result = {
            "current": {
                "hourly": round(prior_hourly, 2),
                "monthly": round(prior_monthly, 2)
            },
            "planned": {
                "hourly": round(planned_hourly, 2),
                "monthly": round(planned_monthly, 2)
            },
            "difference": {
                "hourly": round(diff_hourly, 2),
                "monthly": round(diff_monthly, 2),
                "percentage": round(diff_percentage, 2)
            },
            "currency": "RUB",
            "has_changes": has_changes
        }
        
        # Add usage details if requested
        if param_full:
            result["current_usage"] = prior_collector.get_usage()
            result["planned_usage"] = planned_collector.get_usage()
        
        return result
    
    def get_usage_collector(self):
        """Create and return a new usage collector"""
        return UsageCollector(self.pricing_service)
