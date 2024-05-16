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
        group_list_table = dynamodb.Table(self, "group_list_table",
                                      partition_key=dynamodb.Attribute(
                                          name="group_list_id",
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
            handler="generate_randomization_list.handler",
            code=lambda_.Code.from_asset("lambda"),
            memory_size=4096,
            layers=[layer]
        )

        create_group_list = lambda_.Function(
            self, "CreateGroupList",
            runtime=lambda_.Runtime.PYTHON_3_10,
            handler="create_group_list.handler",
            code=lambda_.Code.from_asset("lambda"),
            environment={"DYNAMODB_TABLE_NAME": group_list_table.table_name},
            layers = [layer]
        )

        get_specific_group_list = lambda_.Function(self, "GetSpecificGroupList",
                                                   runtime=lambda_.Runtime.PYTHON_3_10,
                                                   handler="get_specific_group_list.handler",
                                                   code=lambda_.Code.from_asset("lambda"),
                                                   environment={"DYNAMODB_TABLE_NAME": group_list_table.table_name},
                                                   memory_size=1024,
                                                   layers = [layer])

        get_next_group_list_item = lambda_.Function(self, "GetNextGroupListItem",
                                                    runtime=lambda_.Runtime.PYTHON_3_10,
                                                    handler="get_next_group_list_item.handler",
                                                    code=lambda_.Code.from_asset("lambda"),
                                                    environment={"DYNAMODB_TABLE_NAME": group_list_table.table_name},
                                                    memory_size=1024,
                                                    layers = [layer])


        say_hello = lambda_.Function(self, "HelloWorld",
                                       runtime=lambda_.Runtime.PYTHON_3_10,
                                       handler="hello_world.handler",
                                       code=lambda_.Code.from_asset("lambda")
                                       )

        group_list_table.grant_read_write_data(create_group_list)
        group_list_table.grant_read_data(get_specific_group_list)
        group_list_table.grant_read_write_data(get_next_group_list_item)

        group_lists = api.root.add_resource("group_lists")
        group_lists.add_method("POST", apigateway.LambdaIntegration(create_group_list))

        specific_group_list = group_lists.add_resource("{group_list_id}")
        specific_group_list.add_method("GET", apigateway.LambdaIntegration(get_specific_group_list))

        specific_group_list_next = specific_group_list.add_resource("next_item")
        specific_group_list_next.add_method("POST", apigateway.LambdaIntegration(get_next_group_list_item))

        simple_randomizer = api.root.add_resource('simple_randomizer')
        simple_randomizer.add_method("POST", apigateway.LambdaIntegration(generate_randomization_list))

        hello_world = api.root.add_resource('hello_world')
        hello_world.add_method("GET", apigateway.LambdaIntegration(say_hello))

        api_deployment = apigateway.Deployment(self, "APIDeployment20240516a", api=api)
        api_stage = apigateway.Stage(self, f"{env}", deployment=api_deployment, stage_name=env)













