import os
from dotenv import load_dotenv


from trials.trial_repository import TrialRepository

os.environ['AWS_PROFILE'] = 'personalAcc'

load_dotenv()

TABLE_NAME = os.getenv("ENVELOPE_TABLE_DEV")
os.environ["DYNAMODB_TABLE_NAME"] = TABLE_NAME


trial_repository = TrialRepository(os.environ["DYNAMODB_TABLE_NAME"])


item = trial_repository.get_trial("77041e39383b017ad5405cc8ccf2afb93e5d0f0630293104ec22665846dd03ee")

trial_item = item['trial_items'][10]