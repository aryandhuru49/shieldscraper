import os
import json
import boto3
from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings
from job_spider import JobSpider

# Setup S3 client
s3 = boto3.client('s3')
RAW_BUCKET = os.environ['RAW_BUCKET']

if __name__ == "__main__":
    try:
        # 1. Setup Scrapy to output JSON
        output_file = "scraped_soccer_stats.json"

        process = CrawlerProcess(settings={
            **get_project_settings(),
            'FEEDS': {
                output_file: {
                    'format': 'json',
                    'overwrite': True
                }
            },
            'LOG_ENABLED': True
        })

        # 2. Run spider
        process.crawl(JobSpider)  
        process.start()

        # 3. After crawling, upload JSON file to S3
        with open(output_file, "rb") as f:
            s3.put_object(
                Bucket=RAW_BUCKET,
                Key=f"scrapes/{output_file}",
                Body=f.read(),
                ContentType='application/json'
            )

        print(f"Successfully scraped and uploaded {output_file} to S3!")

    except Exception as e:
        print(str(e))
        raise
