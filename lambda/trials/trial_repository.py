import boto3
from botocore.exceptions import ClientError

class TrialLimitReached(Exception):
    pass

class TrialRepository:
    def __init__(self, table_name):
        self.table = boto3.resource('dynamodb').Table(table_name)
        self.cap = 1000
        self.quota_pk = "quota_pk"


    # --- quota helpers ---
    def _inc_quota_or_fail(self) -> bool:
        try:
            self.table.update_item(
                Key={'trial_id': self.quota_pk},
                UpdateExpression="ADD trial_count :one",
                ConditionExpression="attribute_not_exists(trial_count) OR trial_count < :cap",
                ExpressionAttributeValues={':one': 1, ':cap': self.cap},
            )
            return True
        except ClientError as e:
            if e.response['Error']['Code'] == 'ConditionalCheckFailedException':
                return False
            raise

    def _dec_quota_best_effort(self) -> None:
        try:
            self.table.update_item(
                Key={'trial_id': self.quota_pk},
                UpdateExpression="ADD trial_count :neg",
                ExpressionAttributeValues={':neg': -1},
            )
        except ClientError:
            pass  # non-fatal

    # --- db API ---
    def create_trial(self, data, enforce_cap=False):
        item = data.model_dump(exclude_none=True)

        if enforce_cap and not self._inc_quota_or_fail():
            raise TrialLimitReached(f"Trial limit {self.cap} reached. Please contact system administrator.")

        try:
            self.table.put_item(
                Item=item,
                ConditionExpression="attribute_not_exists(trial_id)"
            )
            return data.model_dump(mode="json")
        except Exception:
            print("Failed to create trial")
            if enforce_cap:
                print("Decrementing quota due to failure")
                self._dec_quota_best_effort()  # compensate on failure
            raise


    def get_trial(self, trial_id):
        response = self.table.get_item(
            Key={'trial_id': trial_id}
        )
        return response.get('Item')


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
                # Query the item to determine the failure reason
                try:
                    item = self.get_trial(trial_id)
                    if item:

                        if participant_id in item.get('participant_id_set', set()):
                            raise ValueError(f"Participant ID '{participant_id}' already in trial")

                        if update_idx < len(item.get('trial_items', [])):
                            trial_item = item['trial_items'][update_idx]
                            if trial_item.get('retrieved', 0) != 0:
                                raise ValueError(f"Slot at index {update_idx} already taken")

                    raise ValueError(f"Invalid update: trial not found or index out of range")

                except ClientError:
                    raise ValueError("Failed to determine error cause; trial may not exist")
            raise e
