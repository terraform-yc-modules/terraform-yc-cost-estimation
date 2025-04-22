import json
import argparse
import logging
from core.container import Container
from util.logging import configure_logging
import sys

# ANSI color codes for terminal output
class Colors:
    RESET = '\033[0m'
    RED = '\033[91m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    BLUE = '\033[94m'
    BOLD = '\033[1m'

def process_plan_command():
    """Command-line interface for processing Terraform plans"""
    parser = argparse.ArgumentParser(description="Process a Terraform plan JSON file")
    parser.add_argument("json_file", help="Path to the JSON file")
    parser.add_argument("--full", action="store_true", help="Include detailed usage breakdown")
    parser.add_argument("--no-color", action="store_true", help="Disable colored output")
    args = parser.parse_args()

    # Initialize logging
    configure_logging(logging.INFO)
    
    # Check if tabulate is available
    has_tabulate = True
    try:
        from tabulate import tabulate
    except ImportError:
        has_tabulate = False
        logging.warning("tabulate package not found, using simple print format instead")
    
    # Get container and services
    container = Container.get_instance()
    container.initialize()
    estimator = container.get('estimator')
    
    try:
        with open(args.json_file, 'r') as f:
            data = json.load(f)
            result = estimator.process_plan(data, args.full)
            
            # Print cost comparison
            print("\n=== TERRAFORM COST ESTIMATION ===\n")
            
            print("CURRENT INFRASTRUCTURE:")
            print(f"  Hourly:  {result['current']['hourly']} RUB")
            print(f"  Monthly: {result['current']['monthly']} RUB")
            
            print("\nPLANNED INFRASTRUCTURE:")
            print(f"  Hourly:  {result['planned']['hourly']} RUB")
            print(f"  Monthly: {result['planned']['monthly']} RUB")
            
            # Format difference with sign
            diff_hourly = result['difference']['hourly']
            diff_monthly = result['difference']['monthly']
            diff_percentage = result['difference']['percentage']
            
            sign = "+" if diff_hourly > 0 else ""
            if diff_hourly == 0:
                sign = ""
            
            print("\nDIFFERENCE:")
            print(f"  Hourly:  {sign}{diff_hourly} RUB")
            print(f"  Monthly: {sign}{diff_monthly} RUB")
            print(f"  Change:  {sign}{diff_percentage}%")
            
            # Print usage details if requested
            if args.full and "current_usage" in result and "planned_usage" in result:
                # Create lookup dictionaries for current and planned usage
                current_usage_dict = {}
                for item in result['current_usage']:
                    key = (item['resource_name'], item['resource_type'], item.get('sku_id', ''))
                    current_usage_dict[key] = item
                
                planned_usage_dict = {}
                for item in result['planned_usage']:
                    key = (item['resource_name'], item['resource_type'], item.get('sku_id', ''))
                    planned_usage_dict[key] = item
                
                # Find common keys (resources that exist in both current and planned)
                common_keys = set(current_usage_dict.keys()) & set(planned_usage_dict.keys())
                
                # Current usage details
                print("\n=== CURRENT USAGE DETAILS ===\n")
                if has_tabulate:
                    # Use tabulate for formatted output
                    headers = ["Resource", "Type", "Amount", "Unit", "SKU Name", "Cost (RUB/hour)"]
                    current_table = []
                    for item in result['current_usage']:
                        key = (item['resource_name'], item['resource_type'], item.get('sku_id', ''))
                        row = [
                            item['resource_name'],
                            item['resource_type'],
                            item['amount'],
                            item['unit'],
                            item['sku_name'],
                            f"{item['cost']:.2f}"
                        ]
                        
                        # Highlight if this resource exists in both and has changed
                        if key in common_keys and not args.no_color:
                            if abs(current_usage_dict[key]['amount'] - planned_usage_dict[key]['amount']) > 0.001:
                                # This resource has changed, highlight it
                                row = [f"{Colors.YELLOW}{cell}{Colors.RESET}" for cell in row]
                        
                        current_table.append(row)
                    
                    print(tabulate(current_table, headers=headers, tablefmt="grid"))
                else:
                    # Fallback to simple formatting
                    for item in result['current_usage']:
                        key = (item['resource_name'], item['resource_type'], item.get('sku_id', ''))
                        line = f"{item['resource_name']} ({item['resource_type']}): {item['amount']} {item['unit']} of {item['sku_name']} = {item['cost']:.2f} RUB/hour"
                        
                        # Highlight if this resource exists in both and has changed
                        if key in common_keys and not args.no_color:
                            if abs(current_usage_dict[key]['amount'] - planned_usage_dict[key]['amount']) > 0.001:
                                # This resource has changed, highlight it
                                line = f"{Colors.YELLOW}{line}{Colors.RESET}"
                        
                        print(line)
                
                # Planned usage details
                print("\n=== PLANNED USAGE DETAILS ===\n")
                if has_tabulate:
                    # Use tabulate for formatted output
                    planned_table = []
                    for item in result['planned_usage']:
                        key = (item['resource_name'], item['resource_type'], item.get('sku_id', ''))
                        row = [
                            item['resource_name'],
                            item['resource_type'],
                            item['amount'],
                            item['unit'],
                            item['sku_name'],
                            f"{item['cost']:.2f}"
                        ]
                        
                        # Highlight if this resource exists in both and has changed
                        if key in common_keys and not args.no_color:
                            if abs(current_usage_dict[key]['amount'] - planned_usage_dict[key]['amount']) > 0.001:
                                # This resource has changed, highlight it
                                row = [f"{Colors.GREEN}{cell}{Colors.RESET}" for cell in row]
                        
                        planned_table.append(row)
                    
                    print(tabulate(planned_table, headers=headers, tablefmt="grid"))
                else:
                    # Fallback to simple formatting
                    for item in result['planned_usage']:
                        key = (item['resource_name'], item['resource_type'], item.get('sku_id', ''))
                        line = f"{item['resource_name']} ({item['resource_type']}): {item['amount']} {item['unit']} of {item['sku_name']} = {item['cost']:.2f} RUB/hour"
                        
                        # Highlight if this resource exists in both and has changed
                        if key in common_keys and not args.no_color:
                            if abs(current_usage_dict[key]['amount'] - planned_usage_dict[key]['amount']) > 0.001:
                                # This resource has changed, highlight it
                                line = f"{Colors.GREEN}{line}{Colors.RESET}"
                        
                        print(line)
                
                # Print a summary of changes
                if common_keys:
                    print("\n=== RESOURCE CHANGES ===\n")
                    changes = []
                    for key in common_keys:
                        current = current_usage_dict[key]
                        planned = planned_usage_dict[key]
                        
                        if abs(current['amount'] - planned['amount']) > 0.001:
                            changes.append((current, planned))
                    
                    if changes:
                        if has_tabulate:
                            # Use tabulate for formatted output
                            change_headers = ["Resource", "Type", "Amount Change", "Unit", "Cost Change (RUB/hour)", "Difference"]
                            changes_table = []
                            for current, planned in changes:
                                changes_table.append([
                                    current['resource_name'],
                                    current['resource_type'],
                                    f"{current['amount']} → {planned['amount']}",
                                    current['unit'],
                                    f"{current['cost']:.2f} → {planned['cost']:.2f}",
                                    f"{planned['cost'] - current['cost']:.2f}"
                                ])
                            
                            print(tabulate(changes_table, headers=change_headers, tablefmt="grid"))
                        else:
                            # Fallback to simple formatting
                            for current, planned in changes:
                                print(f"{current['resource_name']} ({current['resource_type']}): {current['amount']} → {planned['amount']} {current['unit']}, Cost: {current['cost']:.2f} → {planned['cost']:.2f} RUB/hour (Diff: {planned['cost'] - current['cost']:.2f})")
                    else:
                        print("No changes in existing resources.")
    except FileNotFoundError:
        print(f"File {args.json_file} not found.")
    except json.JSONDecodeError:
        print("Failed to decode JSON. Please check the file format.")
    except Exception as e:
        print(f"Error: {str(e)}")
