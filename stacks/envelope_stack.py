from aws_cdk import (
    Stack,
    aws_dynamodb as dynamodb,
    aws_apigateway as apigateway,
    aws_lambda as lambda_,
    aws_s3 as s3
)
from constructs import Construct


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

        # DynamoDB
        trial_table = dynamodb.Table(self, "trial_table",
                                      partition_key=dynamodb.Attribute(
                                          name="trial_id",
                                          type=dynamodb.AttributeType.STRING
                                      ),
                                      billing_mode=dynamodb.BillingMode.PAY_PER_REQUEST,
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
            handler="list_generation.generate_randomization_list.handler",
            code=lambda_.Code.from_asset("lambda"),
            memory_size=4096,
            layers=[layer]
        )

        create_trial = lambda_.Function(
            self, "CreateTrial",
            runtime=lambda_.Runtime.PYTHON_3_10,
            handler="trials.create_trial.handler",
            code=lambda_.Code.from_asset("lambda"),
            environment={"DYNAMODB_TABLE_NAME": trial_table.table_name},
            layers = [layer],
            memory_size=1024
        )

        get_specific_trial = lambda_.Function(self, "GetSpecificGroupList",
                                                   runtime=lambda_.Runtime.PYTHON_3_10,
                                                   handler="trials.get_specific_trial.handler",
                                                   code=lambda_.Code.from_asset("lambda"),
                                                   environment={"DYNAMODB_TABLE_NAME": trial_table.table_name},
                                                   memory_size=1024,
                                                   layers = [layer])

        get_next_trial_item = lambda_.Function(self, "GetNextTrialItem",
                                                    runtime=lambda_.Runtime.PYTHON_3_10,
                                                    handler="trials.get_next_trial_item.handler",
                                                    code=lambda_.Code.from_asset("lambda"),
                                                    environment={"DYNAMODB_TABLE_NAME": trial_table.table_name},
                                                    memory_size=1024,
                                                    layers = [layer])


        say_hello = lambda_.Function(self, "HelloWorld",
                                       runtime=lambda_.Runtime.PYTHON_3_10,
                                       handler="hello_world.handler",
                                       code=lambda_.Code.from_asset("lambda")
                                       )

        trial_table.grant_read_write_data(create_trial)
        trial_table.grant_read_data(get_specific_trial)
        trial_table.grant_read_write_data(get_next_trial_item)

        trials = api.root.add_resource("trials")
        trials.add_method("POST", apigateway.LambdaIntegration(create_trial))

        specific_trial = trials.add_resource("{trial_id}")
        specific_trial.add_method("GET", apigateway.LambdaIntegration(get_specific_trial))

        specific_trial_next = specific_trial.add_resource("next_item")
        specific_trial_next.add_method("POST", apigateway.LambdaIntegration(get_next_trial_item))

        simple_randomizer = api.root.add_resource('simple_randomizer')
        simple_randomizer.add_method("POST", apigateway.LambdaIntegration(generate_randomization_list))

        hello_world = api.root.add_resource('hello_world')
        hello_world.add_method("GET", apigateway.LambdaIntegration(say_hello))

        api_deployment = apigateway.Deployment(self, "APIDeployment20250908a", api=api)
        api_stage = apigateway.Stage(self, f"{env}", deployment=api_deployment, stage_name=env)













