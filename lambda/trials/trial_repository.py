import boto3
from botocore.exceptions import ClientError
from trials.custom_errors import ParticipantAlreadyInTrial, SlotAlreadyTaken


class TrialRepository:

    def __init__(self, table_name):
        self.table = boto3.resource('dynamodb').Table(table_name)

    def create_trial(self, data):
        # Insert validated and parsed data into the DynamoDB table
        self.table.put_item(
            Item=data.model_dump(exclude_none=True),  # Convert Pydantic model to dictionary
            ConditionExpression="attribute_not_exists(trial_id)"
        )
        return data.model_dump(mode="json")


    def get_trial(self, trial_id):
        response = self.table.get_item(
            Key={'trial_id': trial_id}
        )
        return response.get('Item')

    # def update_list_item(self, trial_id, update_idx, participant_id, retrieved_at, administrator_id):
    #     self.table.update_item(
    #         Key={
    #             'trial_id': trial_id,
    #         },
    #         UpdateExpression=f'SET trial_items[{update_idx}].retrieved = :retrievedVal, '
    #                          f'trial_items[{update_idx}].participant_id = :participantIdVal, '
    #                          f'trial_items[{update_idx}].retrieved_at = :retrievedAtVal, '
    #                          f'trial_items[{update_idx}].administrator_id = :administratorIdVal',
    #         ExpressionAttributeValues={
    #             ':retrievedVal': 1,
    #             ':participantIdVal': participant_id,
    #             ':retrievedAtVal': retrieved_at,
    #             ':administratorIdVal': administrator_id,
    #         }
    #     )
    #     return update_idx

    def update_list_item(self, trial_id, update_idx, participant_id, retrieved_at, administrator_id):
        try:
            self.table.update_item(
                Key={'trial_id': trial_id},
                UpdateExpression=(
                    f'SET trial_items[{update_idx}].retrieved = :one, '
                    f'trial_items[{update_idx}].participant_id = :pid, '
                    f'trial_items[{update_idx}].retrieved_at = :ts, '
                    f'trial_items[{update_idx}].administrator_id = :admin '
                    'ADD participant_id_set :pidSet'
                ),
                ConditionExpression=(
                    '(attribute_not_exists(participant_id_set) OR NOT contains(participant_id_set, :pid)) '
                    f'AND trial_items[{update_idx}].retrieved = :zero '
                ),
                ExpressionAttributeValues={
                    ':one': 1,
                    ':zero': 0,
                    ':pid': participant_id,
                    ':ts': retrieved_at,
                    ':admin': administrator_id,
                    ':pidSet': {participant_id},  # DynamoDB String Set syntax
                },
                ReturnValues='UPDATED_NEW'
            )
            return update_idx
        except ClientError as e:
            if e.response['Error']['Code'] == 'ConditionalCheckFailedException':
                # Check which condition failed (requires additional logic or DynamoDB Streams for precision)
                raise ValueError("Participant ID already in trial or slot already taken")
            raise e
