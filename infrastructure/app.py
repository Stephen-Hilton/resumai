#!/usr/bin/env python3
"""
Skillsnap CDK Application Entry Point

This is the main entry point for the AWS CDK application that deploys
the Skillsnap infrastructure. The application uses a serverless architecture
deployed to us-west-2 region.

Requirements: 17.1, 17.2
"""
import os
import aws_cdk as cdk

from stacks.dynamodb_stack import DynamoDBStack
from stacks.s3_stack import S3Stack
from stacks.cloudfront_stack import CloudFrontStack
from stacks.cognito_stack import CognitoStack
from stacks.api_gateway_stack import ApiGatewayStack
from stacks.lambda_stack import LambdaStack
from stacks.sqs_stack import SQSStack

# Environment configuration for us-west-2 region
env = cdk.Environment(
    account=os.environ.get("CDK_DEFAULT_ACCOUNT"),
    region="us-west-2"
)

app = cdk.App()

# Domain configuration
DOMAIN_NAME = "skillsnap.me"

# 1. DynamoDB Stack - Data persistence layer
dynamodb_stack = DynamoDBStack(
    app, "SkillsnapDynamoDB",
    env=env,
    description="Skillsnap DynamoDB tables for data persistence"
)

# 2. S3 Stack - Static assets and file storage
s3_stack = S3Stack(
    app, "SkillsnapS3",
    env=env,
    description="Skillsnap S3 buckets for static assets and resumes"
)

# 3. CloudFront Stack - CDN and URL routing
cloudfront_stack = CloudFrontStack(
    app, "SkillsnapCloudFront",
    s3_stack=s3_stack,
    domain_name=DOMAIN_NAME,
    env=env,
    description="Skillsnap CloudFront distributions for CDN"
)

# 4. Cognito Stack - Authentication
cognito_stack = CognitoStack(
    app, "SkillsnapCognito",
    domain_name=DOMAIN_NAME,
    env=env,
    description="Skillsnap Cognito user pool for authentication"
)

# 5. SQS Stack - Async processing queues
sqs_stack = SQSStack(
    app, "SkillsnapSQS",
    env=env,
    description="Skillsnap SQS queues for async processing"
)

# 6. Lambda Stack - Compute layer
lambda_stack = LambdaStack(
    app, "SkillsnapLambda",
    dynamodb_stack=dynamodb_stack,
    sqs_stack=sqs_stack,
    resumes_bucket_name=s3_stack.resumes_bucket.bucket_name,
    imports_bucket_name=s3_stack.imports_temp_bucket.bucket_name,
    env=env,
    description="Skillsnap Lambda functions for compute"
)

# 7. API Gateway Stack - REST API
api_gateway_stack = ApiGatewayStack(
    app, "SkillsnapApiGateway",
    cognito_stack=cognito_stack,
    lambda_stack=lambda_stack,
    domain_name=DOMAIN_NAME,
    env=env,
    description="Skillsnap API Gateway REST API"
)

# Add dependencies
lambda_stack.add_dependency(dynamodb_stack)
lambda_stack.add_dependency(sqs_stack)
api_gateway_stack.add_dependency(cognito_stack)
api_gateway_stack.add_dependency(lambda_stack)

# Add Cognito trigger for post-confirmation
cognito_stack.user_pool.add_trigger(
    cdk.aws_cognito.UserPoolOperation.POST_CONFIRMATION,
    lambda_stack.auth_post_confirmation
)

app.synth()
