# Sealed-envelope randomization AWS infrastructure

AWS CDK application that deploys the serverless backend for generating and storing blocked randomization lists and issuing allocations sequentially. The stack provisions API Gateway, Lambda functions, and a DynamoDB table.

## Requirements

- An AWS account with credentials and a default region configured locally.
- Python 3.10, Node.js, the AWS CLI, and AWS CDK v2.
- Permission to deploy CloudFormation stacks and create or update IAM roles, Lambda functions, API Gateway, DynamoDB, CloudWatch Logs, and CDK assets in S3.

The CDK stack creates the Lambda execution roles and their DynamoDB permissions.

## Environments

The `env` CDK context controls the stack name and API Gateway stage. Supported conventions are:

- `dev`: development stack and `/dev` API stage. This is the default when `env` is omitted.
- `prod`: production stack and `/prod` API stage.

Each environment is deployed as a separate stack with its own API, Lambda functions, and DynamoDB table. There is no staging environment.

## Deploy

Deploy only the environment you need:

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt

# Required once for each AWS account and region
cdk bootstrap

# Development
cdk deploy EnvelopeStack-dev --context env=dev

# Production
cdk deploy EnvelopeStack-prod --context env=prod
```

After deployment, find the invoke URL under **API Gateway > Stages > dev** or **prod** and use it as `REACT_APP_API_URL` in the frontend.

The stack does not host the frontend.

## Access control and debugging

The API allows cross-origin requests and does not configure an authorizer. Trial-data requests require `only_retrieved=1`; unfiltered requests return `403 Forbidden` to prevent disclosure of future allocations.

Full-list retrieval logic remains available for local debugging. It can be re-enabled by removing the `if not only_retrieved` guard in `lambda/trials/get_specific_trial.py`, but this modification should not be used in an unauthenticated public deployment.

## Remove

```bash
# Replace prod with dev when removing the development stack
cdk destroy EnvelopeStack-prod --context env=prod
```

## Release

The version described in the accompanying manuscript is `v1.0.1`. See [GitHub Releases](../../releases) for archived versions.
