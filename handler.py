import json
from data_layer import query_all
from decorators import dynamodb_tenant_isolation


@dynamodb_tenant_isolation
def handler(event, context):
    path_parameters = event["pathParameters"]
    querying_tenant_id = path_parameters["tenant_id"]

    body = query_all(querying_tenant_id)
    return {
        "statusCode": 200,
        "body": json.dumps(body)
    }
