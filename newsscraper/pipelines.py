# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
import mysql.connector

import boto3





class NewsscraperPipeline:
    def process_item(self, item, spider):
        
        adapter = ItemAdapter(item)
        field_names = adapter.field_names()
        for field_name in field_names:
            if field_name != "description":
                value = adapter.get(field_name)
                adapter[field_name] =value.strip()
        return item
class SaveToMySQLPipline:
    def __init__(self):
        self.conn =mysql.connector.connect(
            host = "localhost",
            user = "root",
            password="",
            database ="news"
        )
        self.cur = self.conn.cursor()
        
        self.cur.execute("""
           CREATE TABLE IF NOT EXISTS news(
            id int NOT NULL auto_increment, 
            title text,
            author text,
            content text,
            description text,
            PRIMARY KEY (id)
        )
        """)
        
        

        
    def process_item(self, item, spider):
        try:
            self.cur.execute("""
                INSERT INTO news (title, author, content, description)
                VALUES (%s, %s, %s, %s)
            """, (
                item["title"],
                item["author"],
                item["content"],
                item["description"]
            ))
            self.conn.commit()
        except mysql.connector.errors.ProgrammingError as e:
            spider.logger.error(f"Error: {e}")
        return item
        
            
    def close_spider(self, spider):

        ## Close cursor & connection to database 
        self.cur.close()
        self.conn.close()
