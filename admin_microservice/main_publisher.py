from admin_microservice.rabbitmq.trial_publisher import TrialPublisher
from pydantic import BaseModel

class TrialItem(BaseModel):
    item_name: str

class Trial(BaseModel):
    name: str
    age: int
    trial_item: TrialItem

def main():
    trial_item = TrialItem(item_name="item1")
    trial = Trial(name="admin", age=20, trial_item=trial_item)
    
    trial_publisher = TrialPublisher()
    trial_publisher.publish(trial)
    print("Main publisher is running")
    print("Publisher is running")
    trial_publisher.close_connection()
    print("Publisher is closed")


# To start the publisher, run this script while in the root of the project directory:
# poetry run python -m admin_microservice.main_publisher
if __name__ == '__main__':
    main()