# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter


import boto3
import uuid





class NewsscraperPipeline:
    def process_item(self, item, spider):
        
        adapter = ItemAdapter(item)
        field_names = adapter.field_names()
        for field_name in field_names:
            if field_name != "description":
                value = adapter.get(field_name)
                adapter[field_name] =value.strip()
        return item
    
class DynamoDBPipeline:
    def __init__(self):
        self.dynamodb = boto3.resource('dynamodb')
        self.table_name = 'ScrapyData'
        self.create_table()
        
    def process_item(self, item, spider):
        try:
            self.dynamodb.Table(self.table_name).put_item(Item={
            "id": str(uuid.uuid4()),
            "title": item["title"],
            "author" : item["author"],
            "description" : item["description"],
            "content": item["content"]
            })
        except Exception as e:
            print(f"An error occurred: {e}")
        return item
        
    def create_table(self):
            try:
                self.table = self.dynamodb.create_table(
                       TableName=self.table_name,
                    KeySchema=[
                        {
                            'AttributeName': 'id',
                            'KeyType': 'HASH'  # Partition key
                        },
                    ],
                    AttributeDefinitions=[
                        {
                            'AttributeName': 'id',
                            'AttributeType': 'S'
                        }
                    ],
                        ProvisionedThroughput={
                            'ReadCapacityUnits': 1,
                            'WriteCapacityUnits': 1
                        }
                    )
                self.table.meta.client.get_waiter('table_exists').wait(TableName=self.table_name)
                print(f"Table {self.table_name} created successfully.")
                
               
            except Exception as e:
                print(f"An error occurred: {e}")
                

                
        
        

    