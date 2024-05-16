import boto3


class GroupListRepository:

    def __init__(self, table_name):
        self.table = boto3.resource('dynamodb').Table(table_name)

    def create_list(self, data):
        # Insert validated and parsed data into the DynamoDB table
        self.table.put_item(
            Item=data.dict(),  # Convert Pydantic model to dictionary
            ConditionExpression="attribute_not_exists(group_list_id)"
        )

        return data.dict()

    def get_list(self, group_list_id):
        response = self.table.get_item(
            Key={'group_list_id': group_list_id}
        )
        return response.get('Item')

    def update_list_item(self, group_list_id, update_idx, participant_id, retrieved_at):

        self.table.update_item(
            Key={
                'group_list_id': group_list_id,
            },
            UpdateExpression=f'SET group_list_items[{update_idx}].retrieved = :retrievedVal, '
                             f'group_list_items[{update_idx}].participant_id = :participantIdVal, '
                             f'group_list_items[{update_idx}].retrieved_at = :retrievedAtVal',
            ExpressionAttributeValues={
                ':retrievedVal': 1,
                ':participantIdVal': participant_id,
                ':retrievedAtVal': retrieved_at,
            }
        )
        return update_idx

