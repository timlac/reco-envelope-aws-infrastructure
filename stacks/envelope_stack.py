from aws_cdk import (
    Stack,
    aws_dynamodb as dynamodb,
    aws_apigateway as apigateway,
    aws_lambda as lambda_,
    aws_s3 as s3
)
from constructs import Construct
from aws_cdk.aws_cognito import UserPool


class EnvelopeStack(Stack):

    def __init__(self,
                 scope: Construct,
                 construct_id: str,
                 env: str,
                 **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        # Api Definition
        api = apigateway.RestApi(self,
                                 f"envelope_api-{env}",
                                 default_cors_preflight_options=apigateway.CorsOptions(
                                     allow_origins=apigateway.Cors.ALL_ORIGINS,
                                     allow_methods=apigateway.Cors.ALL_METHODS,
                                     allow_headers=["*"]),
                                 deploy=False
                                 )

        layer = lambda_.LayerVersion(
            self, 'DependencyLayer',
            code=lambda_.Code.from_asset('lambda/layer/my-layer.zip'),
            compatible_runtimes=[lambda_.Runtime.PYTHON_3_10],
            description='A layer containing my Python dependencies'
        )

        generate_randomization_list = lambda_.Function(
            self, "GenerateRandomizationList",
            runtime=lambda_.Runtime.PYTHON_3_10,
            handler="generate_randomization_list.handler",
            code=lambda_.Code.from_asset("lambda"),
            memory_size=2048,
            layers=[layer]
        )

        say_hello = lambda_.Function(self, "HelloWorld",
                                       runtime=lambda_.Runtime.PYTHON_3_10,
                                       handler="hello_world.handler",
                                       code=lambda_.Code.from_asset("lambda")
                                       )

        simple_randomizer = api.root.add_resource('simple_randomizer')
        hello_world = api.root.add_resource('hello_world')

        simple_randomizer.add_method("POST", apigateway.LambdaIntegration(generate_randomization_list))
        hello_world.add_method("GET", apigateway.LambdaIntegration(say_hello))

        api_deployment = apigateway.Deployment(self, "APIDeployment20240511", api=api)
        api_stage = apigateway.Stage(self, f"{env}", deployment=api_deployment, stage_name=env)













