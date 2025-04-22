import json
from core.container import Container
from util.logging import configure_logging
import logging

# Initialize logging
configure_logging(logging.INFO)

def handler(event, context):
    plan = json.loads(event["body"])
    param_full = event.get("queryStringParameters", {}).get("full")

    if param_full and param_full.lower() == "true":
        param_full = True
    else:
        param_full = False

    # Get container and estimator
    container = Container.get_instance()
    container.initialize()
    estimator = container.get('estimator')
    
    result = estimator.process_plan(plan, param_full)

    return {
        'statusCode': 200,
        'body': json.dumps(result)
    }
