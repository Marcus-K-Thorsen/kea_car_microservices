from modules import FanoutConsumer, BasicDeliver, BasicProperties, BlockingChannel
from pydantic import BaseModel
import json

class TrialItem(BaseModel):
    item_name: str

class Trial(BaseModel):
    name: str
    age: int
    trial_item: TrialItem

class TrialConsumer(FanoutConsumer):
    def __init__(self):
        super().__init__('trial_admin_exchange', 'trial_queue_employee')

    def on_message(self, channel: BlockingChannel, method: BasicDeliver, properties: BasicProperties, body: bytes):
        trial_message: str = body.decode('utf-8')
        print(f"The queue: {self.get_queue_name} received message: {trial_message}")
        channel.basic_ack(delivery_tag=method.delivery_tag)
        
        # Parse the JSON string into a dictionary
        trial_dict: dict = json.loads(trial_message)
        print(f"tiral_dict type: {type(trial_dict)}")
        print(f"tiral_dict: {trial_dict}")
        
        # Create the TrialItem and Trial objects from the dictionary
        trial_item = TrialItem(**trial_dict.get('trial_item'))
        trial = Trial(name=trial_dict.get('name'), age=trial_dict.get('age'), trial_item=trial_item)
        
        print(f"Parsed Trial object: {trial}")
        
    
