import boto3


class TrialRepository:

    def __init__(self, table_name):
        self.table = boto3.resource('dynamodb').Table(table_name)

    def create_trial(self, data):
        # Insert validated and parsed data into the DynamoDB table
        self.table.put_item(
            Item=data.dict(),  # Convert Pydantic model to dictionary
            ConditionExpression="attribute_not_exists(trial_id)"
        )

        return data.dict()

    def get_trial(self, trial_id):
        response = self.table.get_item(
            Key={'trial_id': trial_id}
        )
        return response.get('Item')

    def update_list_item(self, trial_id, update_idx, participant_id, retrieved_at, administrator_id):
        self.table.update_item(
            Key={
                'trial_id': trial_id,
            },
            UpdateExpression=f'SET trial_items[{update_idx}].retrieved = :retrievedVal, '
                             f'trial_items[{update_idx}].participant_id = :participantIdVal, '
                             f'trial_items[{update_idx}].retrieved_at = :retrievedAtVal, '
                             f'trial_items[{update_idx}].administrator_id = :administratorIdVal',
            ExpressionAttributeValues={
                ':retrievedVal': 1,
                ':participantIdVal': participant_id,
                ':retrievedAtVal': retrieved_at,
                ':administratorIdVal': administrator_id,
            }
        )
        return update_idx
