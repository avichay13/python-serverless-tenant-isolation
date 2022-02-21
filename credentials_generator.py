import os
import boto3
import jwt

account_id = os.getenv("ACCOUNT_ID")
region = os.getenv("REGION")


def generate_credentials(event):
    tenant_id = extract_tenant_from_auth_header(event)
    dynamic_policy = generate_dynamodb_policy(tenant_id)
    sts_client = boto3.client("sts")
    assumed_role = sts_client.assume_role(
        RoleArn=f"arn:aws:iam::{account_id}:role/DynamodbRoleToAssume",
        RoleSessionName="assume-role-session-name",
        Policy=dynamic_policy,
    )
    credentials = assumed_role["Credentials"]
    return {
        "aws_access_key_id": credentials["AccessKeyId"],
        "aws_secret_access_key": credentials["SecretAccessKey"],
        "aws_session_token": credentials["SessionToken"],
    }


def extract_tenant_from_auth_header(event):
    """
    For this example we assume:
    1. event has an Authorization header in the format "Bearer <jwt-token>"
    2. jwt-token payload consists of a "tenant_id" field
    """
    jwt_token = event["headers"]["Authorization"].split(" ")[1]
    tenant_id = jwt.decode(jwt_token, options={"verify_signature": False})["tenant_id"]
    return tenant_id


def generate_dynamodb_policy(tenant_id):
    return {
        "Version": "2012-10-17",
        "Statement": [{
            "Effect": "Allow",
            "Action": ["dynamodb:GetItem", "dynamodb:PutItem", "dynamodb:Query"],
            "Resource": [
                f"arn:aws:dynamodb:{region}:{account_id}:table/OurTable",
                f"arn:aws:dynamodb:{region}:{account_id}:table/OurTable/index/*",
            ],
            "Condition": {
                "ForAllValues:StringLike": {
                    "dynamodb:LeadingKeys": [f"TENANT#{tenant_id}", f"TENANT#{tenant_id}#*"]
                }
            }
        }]
     }
