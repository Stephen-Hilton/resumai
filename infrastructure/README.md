# Skillsnap Infrastructure

AWS CDK infrastructure for the Skillsnap application.

## Overview

This directory contains the AWS CDK (Cloud Development Kit) code for deploying the Skillsnap serverless infrastructure to AWS. The infrastructure is deployed to the **us-west-2** region.

## Architecture

The infrastructure consists of the following stacks:

- **DynamoDBStack**: All DynamoDB tables for data persistence
- **S3Stack**: S3 buckets for static assets and generated files
- **CloudFrontStack**: CDN distributions and URL rewriting functions
- **CognitoStack**: User authentication with Google OAuth
- **SQSStack**: Async processing queues for generation tasks
- **LambdaStack**: All Lambda functions (Python 3.12 runtime)
- **ApiGatewayStack**: REST API with Cognito authorization

## Prerequisites

- Python 3.12+
- AWS CLI configured with appropriate credentials
- AWS CDK CLI (`npm install -g aws-cdk`)
- Node.js 18+ (for CDK CLI)

## Setup

1. Create and activate a virtual environment:

```bash
cd infrastructure
python3 -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
```

2. Install dependencies:

```bash
pip install -r requirements.txt
```

3. For development, install additional dependencies:

```bash
pip install -r requirements-dev.txt
```

## Useful Commands

- `cdk synth` - Synthesize CloudFormation template
- `cdk diff` - Compare deployed stack with current state
- `cdk deploy` - Deploy stack to AWS
- `cdk destroy` - Remove stack from AWS
- `pytest` - Run unit tests

## Project Structure

```
infrastructure/
├── app.py                 # CDK app entry point
├── cdk.json              # CDK configuration
├── requirements.txt      # Python dependencies
├── requirements-dev.txt  # Development dependencies
├── README.md             # This file
├── stacks/               # CDK stack definitions
│   ├── __init__.py
│   ├── api_gateway_stack.py
│   ├── cloudfront_stack.py
│   ├── cognito_stack.py
│   ├── dynamodb_stack.py
│   ├── lambda_stack.py
│   ├── s3_stack.py
│   └── sqs_stack.py
└── tests/                # Unit and property tests
    └── __init__.py
```

## Environment Variables

The following environment variables are used:

- `CDK_DEFAULT_ACCOUNT`: AWS account ID (auto-detected if not set)
- `CDK_DEFAULT_REGION`: AWS region (defaults to us-west-2)

## Deployment Order

Stacks should be deployed in the following order due to dependencies:

1. DynamoDB Stack
2. S3 Stack
3. CloudFront Stack (depends on S3)
4. Cognito Stack
5. SQS Stack
6. Lambda Stack (depends on DynamoDB, SQS)
7. API Gateway Stack (depends on Cognito, Lambda)

## Requirements Traceability

- **Requirement 17.1**: AWS CDK with Python
- **Requirement 17.2**: Deploy to us-west-2 region
- **Requirement 17.3**: Lambda with Python 3.12 runtime
- **Requirement 17.4**: Serverless architecture for cost-effective scaling
- **Requirement 17.5**: Route53 for DNS and ACM for SSL certificates
