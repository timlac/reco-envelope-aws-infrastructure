import boto3


class ListRepository:

    def __init__(self, table_name):
        self.table = boto3.resource('dynamodb').Table(table_name)

    def create_list(self, data):
        # Insert validated and parsed data into the DynamoDB table
        self.table.put_item(
            Item=data.dict(),  # Convert Pydantic model to dictionary
            ConditionExpression="attribute_not_exists(group_list_id)"
        )

        return data



