import json
import logging
import argparse
from core.container import Container
from util.logging import configure_logging

# Initialize logging
configure_logging(logging.INFO)

# Function to be called from main.py
def process_plan(plan, param_full):
    container = Container.get_instance()
    container.initialize()
    estimator = container.get('estimator')
    return estimator.process_plan(plan, param_full)

# Command-line interface
def main():
    from cli.commands import process_plan_command
    process_plan_command()

if __name__ == "__main__":
    main()
