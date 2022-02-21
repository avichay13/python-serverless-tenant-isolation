import boto3

from decorators import get_dynamodb_session_keys


def query_all(tenant_id):
    session = boto3.Session(**get_dynamodb_session_keys())
    dynamodb = session.resource("dynamodb")
    table = dynamodb.Table("OurTable")
    response = table.query(
        KeyConditionExpression="#pk = :pk",
        ExpressionAttributeNames={"#pk": "PK"},
        ExpressionAttributeValues={":pk": f"TENANT#{tenant_id}"},
    )

    items = response.get("Items", [])
    return items
