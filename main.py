from boto3 import resource
from boto3.dynamodb.conditions import Attr, Key

from datetime import datetime


demo_table = resource("dynamodb").Table("test_dynamo")



#############################  insert record #############################

def insert():
    print(f'demo_insert')
    response = demo_table.put_item(
        Item={
                'customer_id': 'cus-05', # parition key
                'order_id' : 'ord-5',  # sort key
                'status': 'pending',
                'created_date' : datetime.now().isoformat()
            }
        )
    print(f'Insert response: {response}') 

insert()